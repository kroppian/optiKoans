"""
Answer-key regression tests for lesson09_pymoo.py.

Each test mirrors one koan with the correct answer filled in.
All implementations here are independent of the lesson file
so these tests never depend on student progress.
"""

import math

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


# ---------------------------------------------------------------------------
# Fixture / helper
# ---------------------------------------------------------------------------

def _rastrigin(x):
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)


# ---------------------------------------------------------------------------
# Reference implementations
# ---------------------------------------------------------------------------

class _RastriginProblem(ElementwiseProblem):
    def __init__(self, n_var=5):
        super().__init__(n_var=n_var, n_obj=1,
                         xl=np.full(n_var, -5.12),
                         xu=np.full(n_var,  5.12))

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = _rastrigin(x)


def _solve_rastrigin(n_var=5, pop_size=200, n_gen=500, seed=1):
    problem   = _RastriginProblem(n_var=n_var)
    algorithm = GA(pop_size=pop_size, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', n_gen),
                         seed=seed, verbose=False)
    return res.X, res.F[0]


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_global_minimum_2d():
    assert _rastrigin([0, 0]) == 0


def test_koan01_local_minimum_one_step():
    assert _rastrigin([1, 0]) == 1


def test_koan01_local_minimum_two_steps():
    assert _rastrigin([1, 1]) == 2


def test_koan01_global_minimum_5d():
    assert _rastrigin([0] * 5) == 0


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_n_var():
    assert _RastriginProblem(n_var=5).n_var == 5


def test_koan02_n_obj():
    assert _RastriginProblem(n_var=5).n_obj == 1


def test_koan02_lower_bound():
    assert _RastriginProblem(n_var=5).xl[0] == -5.12


def test_koan02_upper_bound():
    assert _RastriginProblem(n_var=5).xu[0] == 5.12


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_evaluate_at_origin():
    problem = _RastriginProblem(n_var=5)
    out = {}
    problem._evaluate(np.zeros(5), out)
    assert out["F"] == 0.0


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_solution_length():
    problem   = _RastriginProblem(n_var=5)
    algorithm = GA(pop_size=100, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)
    assert len(res.X) == 5


def test_koan04_objective_length():
    problem   = _RastriginProblem(n_var=5)
    algorithm = GA(pop_size=100, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)
    assert len(res.F) == 1


def test_koan04_near_optimal():
    problem   = _RastriginProblem(n_var=5)
    algorithm = GA(pop_size=100, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)
    assert res.F[0] < 10.0


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_solution_length():
    best_x, _ = _solve_rastrigin(n_var=5, pop_size=200, n_gen=500, seed=1)
    assert len(best_x) == 5


def test_koan05_near_optimal():
    _, best_f = _solve_rastrigin(n_var=5, pop_size=200, n_gen=500, seed=1)
    assert best_f < 1.0
