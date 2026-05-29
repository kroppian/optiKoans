"""
Answer-key regression tests for lesson07_selection.py.

Each test mirrors one koan with the correct answer filled in.
tournament_select is implemented here independently of the lesson file
so these tests never depend on student progress.
"""

import random


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

_population = [
    [1, 1, 1, 0, 1, 1, 0, 0],   # score =  -24
    [1, 0, 1, 0, 1, 1, 0, 1],   # score =  -21
    [1, 1, 0, 1, 0, 1, 0, 0],   # score = 2974  (infeasible)
    [0, 0, 0, 0, 0, 0, 0, 0],   # score =    0
]
_scores = [-24, -21, 2974, 0]


# ---------------------------------------------------------------------------
# Reference implementation
# ---------------------------------------------------------------------------

def _tournament_select(population, scores):
    i, j = random.sample(range(len(population)), 2)
    winner = i if scores[i] <= scores[j] else j
    return population[winner]


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_population_structure():
    assert len(_population) == 4
    assert _population[0] == [1, 1, 1, 0, 1, 1, 0, 0]


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_finding_the_best():
    best_score = min(_scores)
    assert best_score == -24
    assert _population[_scores.index(best_score)] == [1, 1, 1, 0, 1, 1, 0, 0]


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_tournament_optimal_vs_infeasible():
    i, j = 0, 2
    winner = i if _scores[i] <= _scores[j] else j
    assert winner == 0


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_tournament_suboptimal_vs_zeros():
    i, j = 1, 3
    winner = i if _scores[i] <= _scores[j] else j
    assert winner == 1


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_infeasible_always_loses():
    assert (min(-24, 2974) < 2974) == True
    assert (min(-21, 2974) < 2974) == True
    assert (min(  0, 2974) < 2974) == True


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_tournament_select_deterministic():
    # seed=0 → sample picks [3, 1]: scores[3]=0 vs scores[1]=-21 → index 1 wins
    random.seed(0)
    assert _tournament_select(_population, _scores) == [1, 0, 1, 0, 1, 1, 0, 1]


def test_koan06_tournament_select_length():
    random.seed(0)
    winner = _tournament_select(_population, _scores)
    assert len(winner) == 8


def test_koan06_infeasible_never_wins():
    random.seed(42)
    winners = [_tournament_select(_population, _scores) for _ in range(200)]
    assert [1, 1, 0, 1, 0, 1, 0, 0] not in winners
