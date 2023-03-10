fancy_names = {
    'abstract-algebra': 'Abstract Algebra',
    'algebra': 'Algebra',
    'algebraic-geometry': 'Algebraic Geometry',
    'algebraic-structures': 'Algebraic Structures',
    'algebraic-topology': 'Algebraic Topology',
    'analysis': 'Analysis',
    'calculus': 'Calculus',
    'combinatorics': 'Combinatorics',
    'complex-analysis': 'Complex Analysis',
    'counting': 'Counting',
    'differential-geometry': 'Differential Geometry',
    'discrete-math': 'Discrete Mathematics',
    'elementary-number-theory': 'Elementary Number Theory',
    'euclidean': 'Euclidean Geometry',
    'foundations': 'Foundations and Logic',
    'functions': 'Functions',
    'geometry': 'Geometry',
    'graph-theory': 'Graph Theory',
    'group-theory': 'Group Theory',
    'linear-algebra': 'Linear Algebra',
    'matrices': 'Matrices',
    'multivariable': 'Multivariable Calculus',
    'number-theory': 'Number Theory',
    'objects': 'Elementary Mathematical Objects',
    'probability': 'Probability',
    'real-analysis': 'Real Analysis',
    'set-theory': 'Set Theory',
    'single-variable': 'Single Variable Calculus',
    'sv-limits-continuity': 'Limits and Continuity',
    'topology': 'Topology',
}


def fancy_namer(name: str) -> str:
    return fancy_names[name] if name in fancy_names else name
