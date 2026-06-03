"""
Answer-key regression tests for lesson10_parallelization.py.

Each test mirrors one koan with the correct answer filled in.
All implementations here are independent of the lesson file
so these tests never depend on student progress.
"""

import math
from multiprocessing.pool import ThreadPool

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

def _rastrigin(x):
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)


# ---------------------------------------------------------------------------
# Reference implementations
# ---------------------------------------------------------------------------

class _ParallelRastriginProblem(Problem):
    def __init__(self, n_var=5, n_workers=4):
        super().__init__(n_var=n_var, n_obj=1,
                         xl=np.full(n_var, -5.12),
                         xu=np.full(n_var,  5.12))
        self.n_workers = n_workers

    def _evaluate(self, X, out, *args, **kwargs):
        with ThreadPool(self.n_workers) as pool:
            results = pool.map(_rastrigin, X)
        out["F"] = np.array(results).reshape(-1, 1)


def _solve_rastrigin_parallel(n_var=5, pop_size=100, n_gen=200, seed=1, n_workers=4):
    problem   = _ParallelRastriginProblem(n_var=n_var, n_workers=n_workers)
    algorithm = GA(pop_size=pop_size, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', n_gen),
                         seed=seed, verbose=False)
    return res.X, res.F[0]


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------
# TODO make this one test to make it flow like the main Koan
def test_koan01_full_shape():
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert X.shape == (3, 3)


def test_koan01_pop_size_dimension():
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert X.shape[0] == 3


def test_koan01_n_var_dimension():
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert X.shape[1] == 3


def test_koan01_first_row():
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert list(X[0]) == [1, 2, 3]


def test_koan01_f_values():
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert [sum(x) for x in X] == [6, 15, 24]


def test_koan01_output_shape():
    assert np.array([6, 15, 24]).reshape(-1, 1).shape == (3, 1)


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_serial():
    assert list(map(abs, [-3, 1, -4, 1, -5])) == [3, 1, 4, 1, 5]


def test_koan02_parallel():
    with ThreadPool(2) as pool:
        assert list(pool.map(abs, [-3, 1, -4, 1, -5])) == [3, 1, 4, 1, 5]


def test_koan02_agree():
    serial = list(map(abs, [-3, 1, -4, 1, -5]))
    with ThreadPool(2) as pool:
        parallel = list(pool.map(abs, [-3, 1, -4, 1, -5]))
    assert (serial == parallel) == True


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_output_shape():
    problem = _ParallelRastriginProblem(n_var=5, n_workers=2)
    out = {}
    problem._evaluate(np.zeros((3, 5)), out)
    assert out["F"].shape == (3, 1)


def test_koan03_value_at_origin():
    problem = _ParallelRastriginProblem(n_var=5, n_workers=2)
    out = {}
    problem._evaluate(np.zeros((3, 5)), out)
    assert out["F"][0, 0] == 0.0


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_solution_length():
    best_x, _ = _solve_rastrigin_parallel(
        n_var=5, pop_size=100, n_gen=200, seed=1, n_workers=4
    )
    assert len(best_x) == 5


def test_koan04_near_optimal():
    _, best_f = _solve_rastrigin_parallel(
        n_var=5, pop_size=100, n_gen=200, seed=1, n_workers=4
    )
    assert best_f < 10.0
