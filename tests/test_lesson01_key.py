"""
Answer-key regression tests for lesson01_keeping_constraints.py.

Each test mirrors one koan with the correct answer filled in.
"""


# ---------------------------------------------------------------------------
# Koan 01 — feasibility
# ---------------------------------------------------------------------------

def test_koan01_feasibility_answers():
    def is_feasible(weight, capacity=10):
        return weight <= capacity

    assert is_feasible(8)  == True
    assert is_feasible(10) == True
    assert is_feasible(12) == False


# ---------------------------------------------------------------------------
# Koan 02 — inequality constraint standard form
# ---------------------------------------------------------------------------

def test_koan02_inequality_constraint_answers():
    def g(weight):
        return weight - 10

    assert (g(8)  <= 0) == True
    assert (g(10) <= 0) == True
    assert (g(12) <= 0) == False


# ---------------------------------------------------------------------------
# Koan 03 — equality constraint
# ---------------------------------------------------------------------------

def test_koan03_equality_constraint_answers():
    def h(x):
        return x - 5

    assert h(5)   == 0
    assert h(6)   == 1
    assert h(4.9) == pytest_approx(-0.1)

    assert (h(5) == 0) == True


def pytest_approx(value):
    """Tiny helper so we can compare floats without importing pytest here."""
    import math
    class _Approx:
        def __eq__(self, other):
            return math.isclose(other, value, rel_tol=1e-9, abs_tol=1e-9)
        def __repr__(self):
            return f"≈{value}"
    return _Approx()


# ---------------------------------------------------------------------------
# Koan 04 — violation amount
# ---------------------------------------------------------------------------

def test_koan04_violation_amount_answers():
    def violation(weight, capacity=10):
        return max(0, weight - capacity)

    assert violation(8)  == 0
    assert violation(10) == 0
    assert violation(13) == 3


# ---------------------------------------------------------------------------
# Koan 05 — multiple constraints
# ---------------------------------------------------------------------------

def test_koan05_multiple_constraints_answers():
    def is_feasible(weight, cost):
        return weight <= 10 and cost <= 50

    assert is_feasible(8,  40) == True
    assert is_feasible(12, 40) == False
    assert is_feasible(8,  60) == False
    assert is_feasible(12, 60) == False


# ---------------------------------------------------------------------------
# Koan 06 — reference implementation of penalty
# ---------------------------------------------------------------------------

def _penalty_reference(weight, capacity=10, penalty_weight=1000):
    """Reference solution for the penalty function."""
    return max(0, weight - capacity) * penalty_weight


def test_koan06_penalty_reference():
    assert _penalty_reference(8)  == 0
    assert _penalty_reference(10) == 0
    assert _penalty_reference(15) == 5 * 1000
    assert _penalty_reference(11, capacity=10, penalty_weight=500) == 500


def test_koan06_penalty_feasible_always_zero():
    for w in range(11):  # 0 through 10 are all feasible
        assert _penalty_reference(w) == 0


def test_koan06_penalty_scales_linearly():
    """Each unit over capacity adds penalty_weight to the penalty."""
    for excess in range(1, 6):
        assert _penalty_reference(10 + excess) == excess * 1000
