"""
Lesson 09 — Using a Library: Optimization with pymoo
=====================================================
Over the last five lessons you built every component of a genetic algorithm by hand:
binary encoding, a penalized objective, crossover, mutation, tournament selection,
and finally the full GA loop. That ground-up understanding was the point — you now
know *why* each piece exists.

Now meet pymoo: a Python library that does all of that for you. Instead of writing
the GA loop, you define a *Problem* class that describes what you want to minimize.
pymoo handles the rest — population management, selection, crossover, mutation,
termination — through a clean three-step API:

  1. Define a Problem  — subclass ElementwiseProblem, set variable bounds,
                         implement _evaluate to compute the objective.
  2. Choose an Algorithm — GA, Differential Evolution, PSO, NSGA-II, ...
  3. Call minimize()    — returns a Result object with the best solution.

The test problem: the Rastrigin function.
-----------------------------------------
The Rastrigin function is a classic benchmark for evolutionary algorithms.
It has *many* local minima arranged on a regular grid, which causes gradient-based
methods to get stuck immediately. A GA's population-based search escapes these
traps and reliably finds the global minimum.

For n variables in [-5.12, 5.12]:

    f(x) = 10n + sum(x_i^2 - 10 cos(2 pi x_i))

The global minimum is at x = [0, 0, ..., 0] with f = 0.
Every integer grid point is a *local* minimum — the GA must navigate around them
to reach the true optimum.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson09_pymoo.py
"""

import math

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Rastrigin function — provided; read it carefully before filling in koan 01
# ---------------------------------------------------------------------------

def rastrigin(x):
    """Return the Rastrigin function value at point x (a sequence of floats)."""
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)


# ---------------------------------------------------------------------------
# Koan 01 — The Rastrigin function
# ---------------------------------------------------------------------------

def test_01_rastrigin():
    """
    Trace through `rastrigin` at a few key points to build intuition.

    The global minimum is at the origin where f = 0. Every integer grid point
    is a local minimum whose value equals the count of non-zero coordinates.
    """
    assert rastrigin([0, 0])  == 0.0  # global minimum in 2D
    assert rastrigin([1, 0])  == 1.0  # one step away from origin
    assert rastrigin([1, 1])  == 2.0  # two steps away from origin
    assert rastrigin([0] * 5) == 0.0   # global minimum in 5D


# ---------------------------------------------------------------------------
# Koan 02 — Define the Problem class
# ---------------------------------------------------------------------------

class RastriginProblem(ElementwiseProblem):
    """
    A pymoo problem that minimizes the Rastrigin function over `n_var`
    continuous variables, each bounded in [-5.12, 5.12].

    Replace each `pass` with your implementation.

    Hints:
      __init__ — call super().__init__ with n_var=n_var, n_obj=1,
                 xl=np.full(n_var, -5.12), xu=np.full(n_var, 5.12)
      _evaluate — compute rastrigin(x) and assign it to out["F"]
    """

    def __init__(self, n_var=5):
        super().__init__(
            n_var = n_var,
            n_obj = 1,
            xl = np.full(n_var, -5.12),
            xu = np.full(n_var, 5.12)
        )

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = rastrigin(x)


def test_02_rastrigin_problem():
    problem = RastriginProblem(n_var=5)
    assert problem.n_var == 5   # number of decision variables
    assert problem.n_obj == 1   # number of objectives
    assert problem.xl[0] == -5.12   # lower bound on each variable
    assert problem.xu[0] == 5.12  # upper bound on each variable


# ---------------------------------------------------------------------------
# Koan 03 — Evaluate the problem directly
# ---------------------------------------------------------------------------

def test_03_evaluate():
    """
    pymoo calls _evaluate internally during optimization. Here you call it
    by hand to see exactly what it does: it writes the objective value into
    the `out` dictionary under the key "F".
    """
    problem = RastriginProblem(n_var=5)
    out = {}
    problem._evaluate(np.zeros(5), out)
    assert out["F"] == FILL_ME_IN   # Rastrigin value at the origin


# ---------------------------------------------------------------------------
# Koan 04 — Run the GA and read the result
# ---------------------------------------------------------------------------

def test_04_run_and_read():
    """
    minimize() returns a Result object. The two most important attributes:
      res.X — the best solution found (numpy array of length n_var)
      res.F — the objective value(s) of that solution (array of length n_obj)
    """
    problem   = RastriginProblem(n_var=5)
    algorithm = GA(pop_size=100, eliminate_duplicates=True)
    res       = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)

    assert len(res.X)         == FILL_ME_IN   # one value per decision variable
    assert len(res.F)         == FILL_ME_IN   # one value per objective
    assert (res.F[0] < 10.0) == FILL_ME_IN   # did the GA find a good solution?


# ---------------------------------------------------------------------------
# Koan 05 — Solve Rastrigin
# ---------------------------------------------------------------------------

def solve_rastrigin(n_var=5, pop_size=200, n_gen=500, seed=1):
    """
    Use pymoo's GA to minimize the Rastrigin function over `n_var` variables.
    Return (best_x, best_f) where:
      best_x — numpy array of length n_var (the best solution found)
      best_f — float (the objective value at best_x)

    Replace `pass` with your implementation.
    Hints:
      - Create a RastriginProblem(n_var=n_var)
      - Create GA(pop_size=pop_size, eliminate_duplicates=True)
      - Call minimize with termination=('n_gen', n_gen), seed=seed, verbose=False
      - Return res.X and res.F[0]
    """
    pass  # TODO: implement this


def test_05_solve_rastrigin():
    """
    With pop_size=200 and 500 generations the GA finds a solution
    extremely close to the global minimum f = 0.
    """
    best_x, best_f = solve_rastrigin(n_var=5, pop_size=200, n_gen=500, seed=1)
    assert len(best_x) == 5   # one value per variable
    assert best_f < 1.0       # very close to the global minimum of 0
