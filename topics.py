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


def differentiation_topics(project):
    """Use explicit catalog curation, not incidental words or GitHub topics."""
    curated = set(project.get('local', {}).get('topics', []))
    if 'automatic-differentiation' not in curated:
        return []
    return sorted(curated.intersection(DIFFERENTIATION_TOPICS))
