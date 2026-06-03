"""
Answer-key regression tests for lesson11_multiobjective.py.

Each test mirrors one koan with the correct answer filled in.
All implementations here are independent of the lesson file
so these tests never depend on student progress.
"""

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

_weights  = [2, 5, 3, 7, 1, 4, 6, 3]
_values   = [4, 7, 5, 9, 2, 6, 8, 4]


# ---------------------------------------------------------------------------
# Reference implementations
# ---------------------------------------------------------------------------

def _knapsack_objectives(bits, weights, values):
    total_value  = sum(b * v for b, v in zip(bits, values))
    total_weight = sum(b * w for b, w in zip(bits, weights))
    return (-total_value, total_weight)


class _KnapsackMOO(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=8, n_obj=2,
                         xl=np.zeros(8), xu=np.ones(8))

    def _evaluate(self, x, out, *args, **kwargs):
        bits = x.round().astype(int)
        total_value  = sum(b * v for b, v in zip(bits, _values))
        total_weight = sum(b * w for b, w in zip(bits, _weights))
        out["F"] = [-total_value, total_weight]


def _solve_knapsack_moo(pop_size=100, n_gen=200, seed=1):
    problem   = _KnapsackMOO()
    algorithm = NSGA2(pop_size=pop_size)
    res       = minimize(problem, algorithm, ('n_gen', n_gen), seed=seed, verbose=False)
    return res.X, res.F


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_optimal_objectives():
    assert _knapsack_objectives([1, 1, 1, 0, 1, 1, 0, 0], _weights, _values) == (-24, 15)


def test_koan01_empty_objectives():
    assert _knapsack_objectives([0, 0, 0, 0, 0, 0, 0, 0], _weights, _values) == (0, 0)


def test_koan01_all_ones_objectives():
    assert _knapsack_objectives([1, 1, 1, 1, 1, 1, 1, 1], _weights, _values) == (-45, 31)


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_neither_dominates():
    # (-24, 15) vs (-21, 13): A better on f1, worse on f2 → no dominance
    assert ((-24 <= -21) and (15 <= 13)) == False


def test_koan02_a_dominates_c():
    # (-24, 15) vs (-20, 16): A better on both → A dominates C
    assert ((-24 <= -20) and (15 <= 16)) == True


def test_koan02_pareto_front_size():
    # {(-24,15), (-21,13), (-20,16)}: A dominates C; A and B are non-dominated
    assert 2 == 2


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_evaluate_f_values():
    problem = _KnapsackMOO()
    out = {}
    problem._evaluate(np.array([1, 1, 1, 0, 1, 1, 0, 0], dtype=float), out)
    assert list(out["F"]) == [-24, 15]


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_x_ndim():
    problem   = _KnapsackMOO()
    algorithm = NSGA2(pop_size=50)
    res       = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=False)
    assert res.X.ndim == 2


def test_koan04_f_shape_cols():
    problem   = _KnapsackMOO()
    algorithm = NSGA2(pop_size=50)
    res       = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=False)
    assert res.F.shape[1] == 2


def test_koan04_x_shape_cols():
    problem   = _KnapsackMOO()
    algorithm = NSGA2(pop_size=50)
    res       = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=False)
    assert res.X.shape[1] == 8


def test_koan04_multiple_solutions():
    problem   = _KnapsackMOO()
    algorithm = NSGA2(pop_size=50)
    res       = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=False)
    assert (len(res.X) > 1) == True


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_f_shape_cols():
    _, pareto_F = _solve_knapsack_moo(pop_size=100, n_gen=200, seed=1)
    assert pareto_F.shape[1] == 2


def test_koan05_x_shape_cols():
    pareto_X, _ = _solve_knapsack_moo(pop_size=100, n_gen=200, seed=1)
    assert pareto_X.shape[1] == 8


def test_koan05_multiple_solutions():
    pareto_X, _ = _solve_knapsack_moo(pop_size=100, n_gen=200, seed=1)
    assert (len(pareto_X) > 1) == True


def test_koan05_best_value():
    _, pareto_F = _solve_knapsack_moo(pop_size=100, n_gen=200, seed=1)
    best_value_idx = np.argmin(pareto_F[:, 0])
    assert pareto_F[best_value_idx, 0] <= -24
