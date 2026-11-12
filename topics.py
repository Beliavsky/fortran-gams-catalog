"""Curated discovery facets; these do not create GAMS or verification claims."""

DIFFERENTIATION_TOPICS = {
    'automatic-differentiation': 'Automatic differentiation (all)',
    'forward-mode': 'Forward mode',
    'reverse-mode': 'Reverse mode',
    'higher-derivatives': 'Higher derivatives / Hessians',
    'sparse-jacobians': 'Sparse Jacobians',
    'matrix-derivatives': 'Matrix derivatives',
    'source-transformation': 'Source transformation / helpers',
}

EXPRESSION_TOPICS = {
    'expression-parser': 'Expression parsers (all)',
    'scalar-evaluation': 'Scalar evaluation',
    'array-evaluation': 'Vector / matrix evaluation',
    'complex-evaluation': 'Complex arithmetic',
    'custom-functions': 'User-defined functions / callbacks',
    'parser-derivatives': 'Derivatives of parsed expressions',
    'expression-code-generation': 'Fortran code generation',
    'reusable-parser': 'Callable parser library',
    'calculator-cli': 'Command-line calculator / interpreter',
}

DISCOVERY_TOPICS = {**DIFFERENTIATION_TOPICS, **EXPRESSION_TOPICS}


def differentiation_topics(project):
    """Use explicit catalog curation, not incidental words or GitHub topics."""
    curated = set(project.get('local', {}).get('topics', []))
    if 'automatic-differentiation' not in curated:
        return []
    return sorted(curated.intersection(DIFFERENTIATION_TOPICS))


def expression_topics(project):
    """Keep parser capabilities separate from unrelated uses of similar tags."""
    curated = set(project.get('local', {}).get('topics', []))
    if 'expression-parser' not in curated:
        return []
    return sorted(curated.intersection(EXPRESSION_TOPICS))


def discovery_topics(project):
    return sorted(set(differentiation_topics(project) + expression_topics(project)))
