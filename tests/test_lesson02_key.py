"""
Answer-key regression tests for lesson02_bruteForce.py.

Each test mirrors one koan with the correct answer filled in.
brute_force_minimize is implemented here independently of the lesson file
so these tests never depend on student progress.
"""

from itertools import product


# ---------------------------------------------------------------------------
# Reference implementation (answer to koan 06)
# ---------------------------------------------------------------------------

def _brute_force_minimize(f, x1_min, x1_max, x2_min, x2_max):
    space = product(range(x1_min, x1_max + 1), range(x2_min, x2_max + 1))
    return min(space, key=f)


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_evaluates_all_answers():
    calls = []

    def f(x):
        calls.append(x)
        return (x - 4) ** 2

    best = min(range(0, 10), key=f)

    assert len(calls) == 10
    assert best == 4


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_grid_search_space_answers():
    space = list(product([0, 1, 2], [0, 1, 2, 3]))

    assert len(space) == 12
    assert space[0]   == (0, 0)
    assert space[-1]  == (2, 3)


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_brute_force_2d_answer():
    def f(x1, x2):
        return (x1 - 1) ** 2 + (x2 - 2) ** 2

    best = min(product(range(5), range(5)), key=lambda p: f(*p))

    assert best == (1, 2)


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_exponential_growth_answers():
    assert len(list(product(range(10), repeat=1))) == 10
    assert len(list(product(range(10), repeat=2))) == 100
    assert len(list(product(range(10), repeat=3))) == 1000


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_constraint_answers():
    def f(x1, x2):
        return x1 + x2

    def is_feasible(x1, x2):
        return x1 + x2 >= 5

    all_candidates = list(product(range(6), range(6)))
    feasible = [(x1, x2) for x1, x2 in all_candidates if is_feasible(x1, x2)]
    best = min(feasible, key=lambda p: f(*p))

    assert len(feasible) == 21
    assert best == (0, 5)


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_implementation():
    def f(pair):
        x1, x2 = pair
        return (x1 - 2) ** 2 + (x2 - 3) ** 2

    assert _brute_force_minimize(f, 0, 5, 0, 5) == (2, 3)
