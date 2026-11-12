"""Conservative source declaration/comment capture; no inferred Fortran attributes."""
import re


def declaration(statement):
    """Return entity list for declaration/attribute statements, including F77."""
    match = re.match(r'^(?:double\s*precision|double\s*complex|integer|real|complex|logical|character|type|class|procedure|external|dimension|allocatable|pointer|optional|target|value|contiguous|intent)\b\s*(?:\([^)]*\)|\*\s*(?:\([^)]*\)|\d+))?', statement, re.I)
    if not match:
        if '::' in statement and re.search(r'\bintent\s*\(',statement,re.I):return statement.split('::',1)[1]
        return None
    if '::' in statement: return statement.split('::', 1)[1]
    tail = statement[match.end():].strip()
    if not tail or tail.startswith(','): return None
    return tail


def comments(lines, first, last, fixed=False):
    """Attach trailing comments and adjacent explicit FORD comment blocks."""
    result = []
    def add(number, text, kind):
        text=re.sub(r'^[!>*|<#]+\s?', '', text.strip()).strip()
        if text: result.append({'text':text,'kind':kind,'line_start':number,'line_end':number})
    for i in range(first-1,last):
        line=lines[i];quote=None;j=0
        while j<len(line):
            char=line[j]
            if quote:
                if char==quote:
                    if j+1<len(line) and line[j+1]==quote:j+=2;continue
                    quote=None
            elif char in "'\"":quote=char
            elif char=='!':add(i+1,line[j+1:],'trailing');break
            j+=1
    # Preceding documentation must use a preceding-doc marker. Ordinary prose
    # may be a heading for several declarations and is deliberately not guessed.
    before=[];i=first-2
    while i>=0 and re.match(r'^\s*!(?:>|\|)',lines[i]):
        before.append(i);i-=1
    for i in reversed(before):add(i+1,lines[i].lstrip()[1:],'preceding')
    i=last
    if i<len(lines) and re.match(r'^\s*!(?:!|\*)',lines[i]):
        while i<len(lines) and re.match(r'^\s*!',lines[i]) and lines[i].strip()!='!':
            if re.match(r'^\s*![>|]',lines[i]):break
            add(i+1,lines[i].lstrip()[1:],'following');i+=1
    return result
