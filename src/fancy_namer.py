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
    'differential-geometry': 'Differential Geometry',
    'discrete-math': 'Discrete Mathematics',
    'elementary-number-theory': 'Elementary Number Theory',
    'foundations': 'Foundations and Logic',
    'functions-limits-continuity': 'Functions, Limits, and Continuity',
    'geometry': 'Geometry',
    'graph-theory': 'Graph Theory',
    'group-theory': 'Group Theory',
    'linear-algebra': 'Linear Algebra',
    'matrices': 'Matrices',
    'multivariable': 'Multivariable Calculus',
    'number-theory': 'Number Theory',
    'probability': 'Probability',
    'real-analysis': 'Real Analysis',
    'set-theory': 'Set Theory',
    'single-variable': 'Single Variable Calculus',
    'topology': 'Topology',
}


def fancy_namer(name: str) -> str:
    return fancy_names[name] if name in fancy_names else name
