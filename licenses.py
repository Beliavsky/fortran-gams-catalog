"""Conservative discovery groups for recorded license terms, not legal compatibility."""
import re

LICENSE_GROUPS = {
    'permissive': 'Permissive',
    'weak-copyleft': 'Weak copyleft',
    'strong-copyleft': 'Strong copyleft',
    'custom-mixed': 'Custom or mixed terms',
    'unclear': 'Unclear or not yet reviewed',
}


def license_reviewed(project):
    return bool(project.get('local', {}).get('license', {}).get('evidence'))


def license_group(project):
    data = project.get('license') or {}
    expression = data.get('spdx_expression') or data.get('label') or ''
    if (not expression or expression.upper() in {'NONE', 'UNKNOWN', 'NOASSERTION', 'LICENSE'}
            or re.match(r'^(?:No |Not specified)', expression, re.I)):
        return 'unclear'
    aliases = {'BSD-3': 'BSD-3-Clause', 'BSD3': 'BSD-3-Clause',
               'BSD 3-Clause License': 'BSD-3-Clause', 'Apache': 'Apache-2.0'}
    expression = aliases.get(expression, expression)
    tokens = re.findall(r'\(|\)|[^\s()]+', expression)
    position = 0

    def atom():
        nonlocal position
        if position >= len(tokens):
            raise ValueError('Missing license')
        token = tokens[position]
        position += 1
        if token in {'AND', 'OR', 'WITH', ')'}:
            raise ValueError('Expected license identifier')
        if token == '(':
            result = combine('OR')
            if position >= len(tokens) or tokens[position] != ')':
                raise ValueError('Missing parenthesis')
            position += 1
            return result
        if token in {'MIT', 'ISC', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause',
                     'BSD-2-Clause-Patent', 'BSD-3-Clause-Open-MPI', 'BSL-1.0', 'CC0-1.0', 'Unlicense'}:
            return 'permissive'
        if re.fullmatch(r'LGPL-(?:2\.0|2\.1|3\.0)(?:-only|-or-later)?', token) or token in {'MPL-2.0', 'EPL-1.0', 'EPL-2.0', 'CECILL-C'}:
            return 'weak-copyleft'
        if re.fullmatch(r'(?:A?GPL)-(?:2\.0|3\.0)(?:-only|-or-later)?', token) or token in {'CECILL-2.0', 'CECILL-2.1'}:
            return 'strong-copyleft'
        return 'custom-mixed'

    def combine(operator):
        nonlocal position
        value = combine('AND') if operator == 'OR' else atom()
        while position < len(tokens) and tokens[position] == operator:
            position += 1
            other = combine('AND') if operator == 'OR' else atom()
            order = ['permissive', 'weak-copyleft', 'strong-copyleft', 'custom-mixed']
            value = order[(min if operator == 'OR' else max)(order.index(value), order.index(other))]
        return value

    try:
        result = combine('OR')
        return result if position == len(tokens) else 'custom-mixed'
    except ValueError:
        return 'custom-mixed'
