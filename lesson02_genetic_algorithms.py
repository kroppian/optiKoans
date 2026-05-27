"""
Lesson 02 — Genetic Algorithms
================================
A genetic algorithm (GA) is an optimization method inspired by natural
selection. Instead of testing one solution at a time, it works with a
*population* of candidates and evolves them over many *generations*.

Each generation:
  1. Evaluate every candidate (compute its objective score)
  2. Select the best candidates to be "parents"
  3. Create new candidates via crossover (combine two parents)
  4. Randomly mutate some candidates to explore new areas
  5. Replace the old population with the new one

We'll use **pymoo** — a Python framework built for this kind of optimization.

Work through each koan. Replace FILL_ME_IN and implement any `pass` body.

Run your progress with:
    python optiKoans.py lesson02_genetic_algorithms.py
"""

import numpy as np

from conftest import FILL_ME_IN
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize


# ---------------------------------------------------------------------------
# Koan 01 — A population is a matrix of candidate solutions
# ---------------------------------------------------------------------------

def test_01_population_shape():
    """
    In pymoo a population is a 2-D NumPy array:
      • rows  = individual candidates
      • columns = decision variables (the numbers we're optimizing)
    """
    population = np.random.rand(20, 3)   # 20 candidates, 3 variables each

    assert population.shape[0] == FILL_ME_IN   # How many candidates?
    assert population.shape[1] == FILL_ME_IN   # How many variables per candidate?


# ---------------------------------------------------------------------------
# Koan 02 — Evaluating every candidate in the population
# ---------------------------------------------------------------------------

def test_02_evaluate_population():
    """
    To run a GA we must score every candidate.
    Here f(x) = sum of squares — the Sphere function.
    """

    def f(x):
        return np.sum(x ** 2)

    population = np.array([
        [1.0, 0.0],   # candidate 0
        [0.0, 0.0],   # candidate 1
        [1.0, 1.0],   # candidate 2
    ])

    scores = [f(ind) for ind in population]

    assert scores[0] == FILL_ME_IN   # f([1, 0]) = ?
    assert scores[1] == FILL_ME_IN   # f([0, 0]) = ?
    assert scores[2] == FILL_ME_IN   # f([1, 1]) = ?


# ---------------------------------------------------------------------------
# Koan 03 — Define a Problem for pymoo
# ---------------------------------------------------------------------------
#
# pymoo needs you to describe your problem by subclassing Problem and
# implementing _evaluate.  _evaluate receives:
#   X   — the population matrix  (shape: pop_size × n_var)
#   out — a dict; set out["F"] to the objective scores (shape: pop_size × 1)
#
# Implement SphereProblem._evaluate below, then the test will verify it.

class SphereProblem(Problem):
    """Minimize f(x) = sum(x²) for x in [-5, 5]²."""

    def __init__(self):
        super().__init__(n_var=2, n_obj=1, xl=-5.0, xu=5.0)

    def _evaluate(self, X, out, *args, **kwargs):
        # TODO: compute the sum of squares for each row of X and store in out["F"]
        # Hint: np.sum(X ** 2, axis=1, keepdims=True)
        pass


def test_03_implement_sphere_problem():
    prob = SphereProblem()
    X = np.array([
        [0.0, 0.0],   # row 0 — should score 0
        [1.0, 1.0],   # row 1 — should score 2
        [3.0, 4.0],   # row 2 — should score 25
    ])
    out = {}
    prob._evaluate(X, out)

    assert "F" in out, "_evaluate must set out['F']"
    assert out["F"].shape == (3, 1), "out['F'] should have shape (n_candidates, 1)"
    np.testing.assert_allclose(out["F"][0][0], 0.0)
    np.testing.assert_allclose(out["F"][1][0], 2.0)
    np.testing.assert_allclose(out["F"][2][0], 25.0)


# ---------------------------------------------------------------------------
# Koan 04 — Run the GA and inspect the result
# ---------------------------------------------------------------------------
#
# Note: complete koan 03 before working on this one — the GA needs a working
# SphereProblem._evaluate to find the minimum.

def test_04_run_ga_and_find_minimum():
    """
    Set the GA's population size and number of generations, then let it run.
    The Sphere function has a global minimum of 0 at x = [0, 0].
    """
    pop_size   = FILL_ME_IN   # How many candidates per generation? Try 30 or 50.
    n_gen      = FILL_ME_IN   # How many generations to evolve? Try 50 or 100.

    prob      = SphereProblem()
    algorithm = GA(pop_size=pop_size)
    result    = minimize(
        prob,
        algorithm,
        termination=("n_gen", n_gen),
        seed=42,
        verbose=False,
    )

    # result.F holds the best objective value found
    assert result.F[0] < 0.5, (
        f"The GA found {result.F[0]:.4f} but expected something close to 0. "
        "Try increasing pop_size or n_gen."
    )


# ---------------------------------------------------------------------------
# Koan 05 — Reading the full result   (fill-in koan)
# ---------------------------------------------------------------------------

def test_05_reading_the_result():
    """
    After minimize() finishes, the result object contains:
      result.X  — the best solution found (decision variables)
      result.F  — the objective value of that solution
    """
    prob      = SphereProblem()
    algorithm = GA(pop_size=50)
    result    = minimize(
        prob,
        algorithm,
        termination=("n_gen", 100),
        seed=7,
        verbose=False,
    )

    # How many decision variables does the best solution have?
    assert result.X.shape[0] == FILL_ME_IN

    # How many objectives does this problem have?
    assert result.F.shape[0] == FILL_ME_IN

    # Is the best score less than 1.0?
    assert (result.F[0] < 1.0) == FILL_ME_IN
