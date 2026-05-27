"""
Answer-key regression tests for lesson02_genetic_algorithms.py.

Each test mirrors one koan with the correct answer filled in.
The SphereProblem reference implementation is defined here independently
of the lesson file so these tests never depend on the student's progress.
"""

import numpy as np
import numpy.testing as npt
import pytest

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize


# ---------------------------------------------------------------------------
# Reference implementation of SphereProblem (answer to koan 03)
# ---------------------------------------------------------------------------

class _SphereProblemRef(Problem):
    """Correct implementation of SphereProblem used by the answer-key tests."""

    def __init__(self):
        super().__init__(n_var=2, n_obj=1, xl=-5.0, xu=5.0)

    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = np.sum(X ** 2, axis=1, keepdims=True)


# ---------------------------------------------------------------------------
# Koan 01 — population shape
# ---------------------------------------------------------------------------

def test_koan01_population_shape_answers():
    population = np.random.rand(20, 3)
    assert population.shape[0] == 20
    assert population.shape[1] == 3


# ---------------------------------------------------------------------------
# Koan 02 — evaluating the population
# ---------------------------------------------------------------------------

def test_koan02_evaluate_population_answers():
    def f(x):
        return np.sum(x ** 2)

    population = np.array([
        [1.0, 0.0],
        [0.0, 0.0],
        [1.0, 1.0],
    ])
    scores = [f(ind) for ind in population]

    assert scores[0] == 1.0
    assert scores[1] == 0.0
    assert scores[2] == 2.0


# ---------------------------------------------------------------------------
# Koan 03 — _evaluate reference implementation
# ---------------------------------------------------------------------------

def test_koan03_evaluate_sets_F():
    prob = _SphereProblemRef()
    X = np.array([[0.0, 0.0], [1.0, 1.0], [3.0, 4.0]])
    out = {}
    prob._evaluate(X, out)

    assert "F" in out
    assert out["F"].shape == (3, 1)
    npt.assert_allclose(out["F"][0][0], 0.0)
    npt.assert_allclose(out["F"][1][0], 2.0)
    npt.assert_allclose(out["F"][2][0], 25.0)


def test_koan03_evaluate_batch_size_one():
    prob = _SphereProblemRef()
    out = {}
    prob._evaluate(np.array([[3.0, 4.0]]), out)
    npt.assert_allclose(out["F"][0][0], 25.0)


# ---------------------------------------------------------------------------
# Koan 04 — run the GA (pop_size=50, n_gen=100 converges reliably)
# ---------------------------------------------------------------------------

def test_koan04_ga_converges_with_reference_pop50_gen100():
    prob      = _SphereProblemRef()
    algorithm = GA(pop_size=50)
    result    = minimize(prob, algorithm, termination=("n_gen", 100),
                         seed=42, verbose=False)
    assert result.F[0] < 0.5, (
        f"GA with pop_size=50, n_gen=100 should converge near 0; got {result.F[0]:.4f}"
    )


@pytest.mark.parametrize("pop_size,n_gen", [(30, 50), (50, 100)])
def test_koan04_valid_parameter_choices(pop_size, n_gen):
    """Both suggested parameter pairs should satisfy the koan threshold."""
    prob      = _SphereProblemRef()
    algorithm = GA(pop_size=pop_size)
    result    = minimize(prob, algorithm, termination=("n_gen", n_gen),
                         seed=42, verbose=False)
    assert result.F[0] < 0.5


# ---------------------------------------------------------------------------
# Koan 05 — reading the result
# ---------------------------------------------------------------------------

def test_koan05_result_shape_answers():
    prob      = _SphereProblemRef()
    algorithm = GA(pop_size=50)
    result    = minimize(prob, algorithm, termination=("n_gen", 100),
                         seed=7, verbose=False)

    assert result.X.shape[0] == 2   # n_var decision variables
    assert result.F.shape[0] == 1   # n_obj objectives
    assert (result.F[0] < 1.0) == True
