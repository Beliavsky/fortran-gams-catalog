"""Extract explicit INTENT from pinned Fortran declarations, without inferring intent."""
from dataclasses import dataclass, field
import re

from argument_intents import signature_calls, usage_tokens
from argument_declarations import declaration, comments


def split_items(text, delimiter=','):
    items, start, depth, quote, i = [], 0, 0, None, 0
    while i < len(text):
        char=text[i]
        if quote:
            if char==quote:
                if i+1<len(text) and text[i+1]==quote:
                    i+=2;continue
                quote=None
        elif char in "'\"":quote=char
        elif char in '([':depth+=1
        elif char in ')]':depth-=1
        elif char==delimiter and depth==0:
            items.append(text[start:i].strip());start=i+1
        i+=1
    return items+[text[start:].strip()]


def strip_comment(line):
    quote=None;i=0
    while i<len(line):
        char=line[i]
        if quote:
            if char==quote:
                if i+1<len(line) and line[i+1]==quote:i+=2;continue
                quote=None
        elif char in "'\"":quote=char
        elif char=='!':return line[:i]
        i+=1
    return line


def statements(text, fixed=False):
    """Yield logical statements and physical ranges, including continuations."""
    pending='';start=0;last=0;continued=False
    for number,line in enumerate(text.splitlines(),1):
        if not line.strip() or line.lstrip().startswith('#'):continue
        if fixed:
            if line[0] in 'cC*!':continue
            body=strip_comment(line[6:] if len(line)>6 else '')
            continuation=len(line)>5 and line[5] not in ' 0\t'
            if not body.strip():continue
            if pending and not continuation:
                for part in split_items(pending,';'):
                    if part:yield start,last,part
                pending=''
            if not pending:start=number
            pending+=' '+body.strip();last=number
        else:
            body=strip_comment(line).strip()
            if not body:continue
            if not pending:start=number
            separator='' if continued and body.startswith('&') else ' '
            pending+=separator+body.lstrip('&').rstrip('&');last=number
            continued=body.endswith('&')
            if not continued:
                for part in split_items(pending,';'):
                    if part:yield start,last,part
                pending=''
    if pending:
        for part in split_items(pending,';'):
            if part:yield start,last,part


@dataclass
class Scope:
    name:str
    dummies:list
    start:int
    end:int
    declarations:dict=field(default_factory=dict)
    types:dict=field(default_factory=dict)
    optional:set=field(default_factory=set)
    details:dict=field(default_factory=dict)


class ScopeList(list):
    def __init__(self):
        super().__init__();self.bindings={}


def scopes(text,path):
    result=ScopeList();stack=[];generic=None
    if path.lower().endswith(('.md','.rst','.txt','.json','.toml','.c','.cpp','.h','.sh','.py')):
        return result
    source_lines=text.splitlines()
    last_line=len(source_lines)
    fixed=path.lower().endswith(('.f','.for','.ftn','.f77'))
    if fixed:
        free_heads=sum(bool(re.match(r'^ {0,5}(module|submodule|subroutine|function)\b',strip_comment(line),re.I))
                       for line in text.splitlines())
        fixed_heads=sum(bool(re.match(r'^ {6,}(subroutine|function)\b',strip_comment(line),re.I))
                        for line in text.splitlines())
        if free_heads>fixed_heads:fixed=False
    for first,last,statement in statements(text,fixed):
        source_statement=statement
        statement=re.sub(r'\$\{.*?\}\$', 'zztemplate',statement)
        statement=re.sub(r'\)(?=(?:function|subroutine)\b)',') ',statement,flags=re.I)
        lower=statement.lower().strip()
        interface=re.match(r'^interface\s+([a-z][a-z0-9_]*)\s*$',lower)
        if interface:generic=interface[1]
        if re.match(r'^end\s*interface\b',lower):generic=None
        if generic and re.match(r'^module\s+procedure\b',lower):
            for target in lower.split('procedure',1)[1].strip().lstrip(':').split(','):
                result.bindings.setdefault(generic,[]).append((target.strip(),None))
        if re.match(r'^procedure\b',lower) and '::' in lower:
            passed=re.search(r'\bpass\s*\(\s*(\w+)\s*\)',lower)
            for entity in split_items(lower.split('::',1)[1]):
                binding=re.match(r'(\w+)\s*(?:=>\s*(\w+))?',entity)
                if binding:
                    result.bindings.setdefault(binding[1],[]).append((binding[2] or binding[1],
                        passed[1] if passed else False if 'nopass' in lower else None))
        if re.match(r'^end\s*(subroutine|function)\b',lower) or lower=='end':
            if stack:stack.pop().end=last
            continue
        head=re.match(r'^(?:(?:[a-z][a-z0-9_]*)(?:\s*\([^)]*\)|\s*\*\s*\d+)?\s+)*?'
                      r'(subroutine|function)\s+([a-z][a-z0-9_]*)(?:\s*\(([^)]*)\))?',lower)
        if head:
            item=Scope(head[2], [a.strip().lower() for a in split_items(head[3] or '') if a.strip()],
                       first,last_line)
            result.append(item);stack.append(item);continue
        if not stack:continue
        scope=stack[-1]
        type_match=re.match(r'^(class|type)\s*\(\s*([a-z][a-z0-9_]*)\s*\)',lower)
        if type_match and '::' in lower:
            for entity in split_items(lower.split('::',1)[1]):
                name=re.match(r'([a-z][a-z0-9_]*)',entity)
                if name:scope.types[name[1]]=type_match[2]
        if 'optional' in lower and '::' in lower:
            scope.optional.update(m[1].lower() for entity in split_items(lower.split('::',1)[1])
                                  if (m:=re.match(r'\s*(\w+)',entity)))
        entities=declaration(source_statement)
        if entities is not None:
            shared=split_items(entities)
            for entity in shared:
                name=re.match(r'\s*([a-z][a-z0-9_]*)',entity,re.I)
                if name and name[1].lower() in scope.dummies:
                    scope.details.setdefault(name[1].lower(),[]).append({
                        'text':source_statement.strip(),'path':path,'line_start':first,'line_end':last,
                        'shared':len(shared)>1,
                        'comments':[{**c,'path':path} for c in comments(source_lines,first,last,fixed)]})
        typed=re.match(r'^(integer\b|real\b|complex\b|logical\b|character\b|double\s+precision\b|type\s*\(|class\s*\(|procedure\s*\(|intent\s*\()',lower)
        macro=re.match(r'^[A-Z][A-Z0-9_]*\s*,',statement.strip()) or lower.startswith('zztemplate')
        if not typed and not macro:continue
        intent=re.search(r'\bintent\s*\(\s*(in\s*out|out|in)\s*\)',lower)
        if not intent:continue
        suffix=statement.split('::',1)[1] if '::' in statement else statement[intent.end():]
        for entity in split_items(suffix):
            name=re.match(r'\s*([a-z][a-z0-9_]*)',entity,re.I)
            if name and name[1].lower() in scope.dummies:
                scope.declarations.setdefault(name[1].lower(),[]).append({
                    'intent':re.sub(r'\s+','',intent[1]), 'path':path,'line_start':first,'line_end':last})
    return result


def choose_scope(procedure,call,documents):
    candidates=[]
    name=call['name'].split('%')[-1].lower()
    aliases={target for items in documents.values() for target,_ in getattr(items,'bindings',{}).get(name,[])}
    actual_names={name.lower() for _,start,end,name in usage_tokens(procedure)
                  if call['start']<=start<end<=call['end']}
    actual_count=len(split_items(procedure['signature'][call['start']:call['end']]))
    # Prefer the actual routine identified by this procedure record, then the
    # implementation named in its declaration links (generic/type-bound APIs).
    for order,reference in enumerate([{'path':procedure['path'],'line_start':procedure['line_start'],
                                      'line_end':procedure['line_start']},*procedure['declarations']]):
        for scope in documents.get(reference['path'],[]):
            if (scope.start<=reference['line_start']<=scope.end or
                    reference['line_start']<=scope.start<=reference['line_end']):
                direct=(order==0 and len(signature_calls(procedure['signature']))<=1)
                score=(len(actual_names.intersection(scope.dummies)),
                       int(actual_count==len(scope.dummies)-(1 if '%' in call['name'] else 0)),int(direct),int(scope.name==name),
                       int(scope.name in aliases or scope.name.startswith(name)),-order,-(scope.end-scope.start))
                candidates.append((score,scope))
    for items in documents.values():
        for scope in items:
            if scope.name==name or scope.name in aliases:
                candidates.append(((len(actual_names.intersection(scope.dummies)),
                    int(actual_count==len(scope.dummies)-(1 if '%' in call['name'] else 0)),0,int(scope.name==name),1,-100000,
                    -(scope.end-scope.start)),scope))
    if not candidates:
        matches=[scope for items in documents.values() for scope in items if scope.name==name or scope.name in aliases]
        if len(matches)==1:return matches[0]
        return None
    return max(candidates,key=lambda pair:pair[0])[1]


def inspect(procedure,documents,details=None):
    """Return annotations and a review result, preserving unresolved aliases."""
    signature=procedure['signature'];calls=signature_calls(signature)
    operator=procedure['procedure'].lower().startswith(('operator(', 'assignment('))
    if operator and not calls:calls=[{'name':procedure['procedure'],'start':0,'end':len(signature)}]
    annotations=[];issues=[];checked=[]
    for index,call in enumerate(calls):
        scope=choose_scope(procedure,call,documents)
        if scope is None:
            issues.append(f"{call['name']}: no matching Fortran declaration scope");continue
        checked.append({'path':next(path for path,items in documents.items() if any(s is scope for s in items)),
                        'procedure':scope.name,'line_start':scope.start,'line_end':scope.end})
        visible=[(name,start,end) for ci,start,end,name in usage_tokens(procedure) if ci==index]
        actuals=split_items(signature[call['start']:call['end']].replace('&','').replace('\n',' '))
        dummies=list(scope.dummies)
        binding_pass=[passed for items in documents.values() for target,passed in getattr(items,'bindings',{}).get(call['name'].split('%')[-1].lower(),[])
                      if target==scope.name]
        # A passed object is not displayed among the actual arguments. Only
        # remove it when its declared type matches the recorded derived type.
        if '%' in call['name'] and len(actuals)==len(dummies)-1:
            visible_names={name.lower() for name,_,_ in visible}
            passed=[dummy for dummy in dummies if dummy not in visible_names and
                    scope.types.get(dummy)==procedure.get('derived_type','').lower()]
            explicit={value for value in binding_pass if isinstance(value,str)}
            if len(explicit)==1 and next(iter(explicit)) in dummies:dummies.remove(next(iter(explicit)))
            elif len(passed)==1:dummies.remove(passed[0])
        positional={}
        if operator:
            operand_names=[name for name,_,_ in visible]
            if len(operand_names)==len(dummies):positional={name.lower():dummy for name,dummy in zip(operand_names,dummies)}
        else:
            for position,actual in enumerate(actuals):
                plain=actual.strip().strip('[]').strip()
                keyword=re.match(r'^([a-z][a-z0-9_]*)\s*=\s*([a-z][a-z0-9_]*)$',plain,re.I)
                if keyword:
                    if keyword[1].lower() in dummies:positional[keyword[2].lower()]=keyword[1].lower()
                elif re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',plain) and position<len(dummies):
                    # Exact names take priority; positional aliases are safe only
                    # for a full, non-elliptical list with matching arity.
                    if len(actuals)==len(dummies) or all(d in scope.optional for d in dummies[len(actuals):]):positional[plain.lower()]=dummies[position]
        for name,_,_ in visible:
            key=name.lower()
            dummy=positional.get(key) or (key if key in dummies else None)
            if dummy is None:
                # Keywords are not actual values and a quoted/constant actual
                # does not receive a name annotation.
                if re.search(r'\b'+re.escape(name)+r'\s*=',signature[call['start']:call['end']],re.I):continue
                issues.append(f"{call['name']}: displayed argument {name} not matched to a dummy");continue
            if details is not None and scope.details.get(dummy):
                record={'name':name,'declarations':scope.details[dummy]}
                if scope.name != call['name'].split('%')[-1].lower():record['implementation']=scope.name
                if len(calls)>1:record['call_index']=index
                if dummy!=key:record['dummy']=dummy
                if not any(a['name'].lower()==key and a.get('call_index',0)==index for a in details):details.append(record)
            declarations=scope.declarations.get(dummy,[])
            if not declarations:continue  # Unspecified stays unspecified.
            if len({d['intent'] for d in declarations})!=1:
                issues.append(f"{call['name']}: conditional/conflicting intents for {name}");continue
            annotation={'name':name,**declarations[0]}
            if len(calls)>1:annotation['call_index']=index
            if dummy!=key:annotation['dummy']=dummy
            if not any(a['name'].lower()==key and a.get('call_index',0)==index for a in annotations):annotations.append(annotation)
    if not calls:issues.append('No callable expression found in the usage line')
    return annotations,{'status':'partial' if issues else 'checked',
                        'sources':checked,'issues':list(dict.fromkeys(issues))}
