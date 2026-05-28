"""
Answer-key regression tests for lesson04_binaryEncoding.py.

Each test mirrors one koan with the correct answer filled in.
knapsack_score is implemented here independently of the lesson file
so these tests never depend on student progress.
"""


# ---------------------------------------------------------------------------
# Reference implementation (answer to koan 06)
# ---------------------------------------------------------------------------

def _knapsack_score(bits, weights, values, capacity, penalty_weight=1000):
    total_weight = sum(b * w for b, w in zip(bits, weights))
    total_value  = sum(b * v for b, v in zip(bits, values))
    return -total_value + max(0, total_weight - capacity) * penalty_weight


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_bit_string_selects_items():
    assert sum([1, 0, 0, 0, 0, 0, 0, 0]) == 1
    assert sum([1, 0, 1, 0, 1, 0, 0, 0]) == 3
    assert sum([1, 1, 1, 0, 1, 1, 0, 0]) == 5


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_total_weight():
    weights = [2, 5, 3, 7, 1, 4, 6, 3]
    bits    = [1, 0, 1, 0, 0, 0, 0, 0]
    total_weight = sum(b * w for b, w in zip(bits, weights))
    assert total_weight == 5


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_total_value():
    values = [4, 7, 5, 9, 2, 6, 8, 4]
    bits   = [1, 0, 1, 0, 0, 0, 0, 0]
    total_value = sum(b * v for b, v in zip(bits, values))
    assert total_value == 9


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_feasibility():
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    capacity = 15

    def total_weight(bits):
        return sum(b * w for b, w in zip(bits, weights))

    assert (total_weight([1, 1, 1, 0, 1, 1, 0, 0]) <= capacity) == True
    assert (total_weight([1, 1, 0, 1, 0, 1, 0, 0]) <= capacity) == False


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_penalised_score():
    weights        = [2, 5, 3, 7, 1, 4, 6, 3]
    values         = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity       = 15
    penalty_weight = 1000

    def score(bits):
        tw = sum(b * w for b, w in zip(bits, weights))
        tv = sum(b * v for b, v in zip(bits, values))
        return -tv + max(0, tw - capacity) * penalty_weight

    assert score([1, 1, 1, 0, 1, 1, 0, 0]) == -24
    assert score([1, 1, 0, 1, 0, 1, 0, 0]) == 2974
    assert (score([1, 1, 1, 0, 1, 1, 0, 0]) < score([1, 1, 0, 1, 0, 1, 0, 0])) == True


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_knapsack_score_feasible():
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    values   = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity = 15

    assert _knapsack_score([1, 1, 1, 0, 1, 1, 0, 0], weights, values, capacity) == -24
    assert _knapsack_score([0, 0, 0, 0, 0, 0, 0, 0], weights, values, capacity) == 0


def test_koan06_knapsack_score_infeasible():
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    values   = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity = 15

    assert _knapsack_score([1, 1, 0, 1, 0, 1, 0, 0], weights, values, capacity) == 2974
    assert _knapsack_score([1, 1, 0, 1, 0, 1, 0, 0], weights, values, capacity,
                           penalty_weight=100) == 274


def test_koan06_knapsack_score_feasible_always_beats_infeasible():
    """Any feasible solution should score better than any infeasible one
    when penalty_weight is large enough."""
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    values   = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity = 15

    best_feasible  = _knapsack_score([1, 1, 1, 0, 1, 1, 0, 0], weights, values, capacity)
    worst_infeasible = _knapsack_score([1, 1, 1, 1, 1, 1, 1, 1], weights, values, capacity)
    assert best_feasible < worst_infeasible
