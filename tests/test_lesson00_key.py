"""
Answer-key regression tests for lesson00_finding_good_answers.py.

Each test mirrors one koan but with the correct answer filled in.
If a koan's logic is ever changed, the matching test here will fail,
alerting you that the answer key needs updating too.

These tests do NOT import the lesson file — they duplicate the koan
logic inline so they remain independent of the student's progress.
"""


# ---------------------------------------------------------------------------
# Koan 01 — objective function returns a number
# ---------------------------------------------------------------------------

def test_koan01_objective_function_answers():
    def f(x):
        return x ** 2

    assert f(0)  == 0
    assert f(3)  == 9
    assert f(-2) == 4


# ---------------------------------------------------------------------------
# Koan 02 — lower is better
# ---------------------------------------------------------------------------

def test_koan02_lower_is_better_answer():
    scores = [9, 4, 1, 0, 1, 4, 9]
    best_score = 0
    assert min(scores) == best_score


# ---------------------------------------------------------------------------
# Koan 03 — finding the best input (argmin)
# ---------------------------------------------------------------------------

def test_koan03_finding_best_input_answer():
    def f(x):
        return (x - 3) ** 2

    candidates = list(range(7))
    best_x = 3
    assert best_x == min(candidates, key=f)


# ---------------------------------------------------------------------------
# Koan 04 — maximization
# ---------------------------------------------------------------------------

def test_koan04_maximization_answer():
    def profit(price):
        return -(price - 5) ** 2 + 25

    candidates = list(range(11))
    best_price = 5
    assert best_price == max(candidates, key=profit)


# ---------------------------------------------------------------------------
# Koan 05 — two-variable objective
# ---------------------------------------------------------------------------

def test_koan05_multi_variable_answers():
    def f(x1, x2):
        return x1 ** 2 + x2 ** 2

    assert f(0, 0) == 0
    assert f(3, 4) == 25

    lower_score_pair = (0, 0)
    candidates = [(0, 0), (3, 4)]
    assert lower_score_pair == min(candidates, key=lambda p: f(*p))


# ---------------------------------------------------------------------------
# Koan 06 — reference implementation of find_minimum
# ---------------------------------------------------------------------------

def _find_minimum_reference(f, candidates):
    """Reference solution students are expected to arrive at."""
    return min(candidates, key=f)


def test_koan06_find_minimum_reference():
    def f(x):
        return (x - 7) ** 2

    assert _find_minimum_reference(f, range(15)) == 7


def test_koan06_find_minimum_works_on_other_inputs():
    """Robustness check: reference solution generalises beyond the koan fixture."""
    def f(x): return abs(x - 42)
    assert _find_minimum_reference(f, range(100)) == 42
