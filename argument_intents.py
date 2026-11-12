"""Optional, source-reviewed argument annotations for usage signatures."""
from html import escape
import re

INTENTS = {'in', 'out', 'inout'}


def argument_tokens(signature):
    """Tokenize only the call's argument region, excluding quoted literals."""
    first, last = signature.find('('), signature.rfind(')')
    if first < 0 or last <= first:
        return []
    tokens = []
    pattern = r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"|[A-Za-z][A-Za-z0-9_]*"
    for match in re.finditer(pattern, signature[first+1:last]):
        if match.group()[0] not in "'\"":
            tokens.append((first+1+match.start(), first+1+match.end(), match.group()))
    return tokens


def validate_arguments(procedure, evidence_paths):
    arguments = procedure.get('arguments')
    if arguments is None:
        return
    if (not isinstance(arguments, list) or not arguments or
            procedure.get('role') not in {'public-entry-point', 'public-adapter'} or
            not procedure.get('signature')):
        raise ValueError('Argument intents need a callable usage signature.')
    names = {name.casefold() for _, _, name in argument_tokens(procedure['signature'])}
    seen = set()
    for arg in arguments:
        if not isinstance(arg, dict):
            raise ValueError('Argument annotations must be objects.')
        name = arg.get('name', '')
        if (not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name) or
                name.casefold() in seen or name.casefold() not in names or arg.get('intent') not in INTENTS):
            raise ValueError('Invalid, duplicate or absent argument intent annotation.')
        seen.add(name.casefold())
        start, end = arg.get('line_start'), arg.get('line_end')
        if (arg.get('path') not in evidence_paths or type(start) is not int or type(end) is not int or
                start < 1 or end < start or not any(
                    d['path'] == arg['path'] and d['line_start'] <= start <= end <= d['line_end']
                    for d in procedure.get('declarations', []))):
            raise ValueError('Argument intents must link to recorded argument declarations.')


def signature_markup(procedure):
    """Preserve literal signature text and escape every fragment independently."""
    signature = procedure['signature']
    intents = {arg['name'].casefold(): arg['intent'] for arg in procedure.get('arguments', [])}
    parts, previous = [], 0
    for start, end, name in argument_tokens(signature):
        intent = intents.get(name.casefold())
        if intent not in INTENTS:
            continue
        parts.append(escape(signature[previous:start]))
        label = escape(name+': intent('+intent+')', quote=True)
        parts.append(f'<span class="argument-intent" data-argument-intent="{intent}" '
                     f'tabindex="0" role="note" title="{label}" aria-label="{label}">{escape(name)}</span>')
        previous = end
    parts.append(escape(signature[previous:]))
    return ''.join(parts)
