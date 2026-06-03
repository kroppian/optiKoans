"""
Lesson 10 — Parallel Objective Evaluation
==========================================
A genetic algorithm evaluates every individual in the population once per
generation. With a population of 100 and 200 generations that is 20,000
calls to your objective function. If each call takes a millisecond the GA
finishes in 20 seconds. If each call takes a second — a physics simulation,
a trained neural network, a call to external software — the same run takes
five and a half hours.

pymoo gives you direct control over this through the base `Problem` class.
Unlike `ElementwiseProblem`, which calls `_evaluate(self, x, out)` once per
solution, `Problem` calls `_evaluate(self, X, out)` *once per generation*,
handing you the entire population as a 2D matrix:

    X.shape == (pop_size, n_var)

You receive every solution at once and can dispatch them however you like —
serial loop, thread pool, process pool, GPU batch — then pack results back:

    out["F"] = np.array(results).reshape(-1, 1)   # shape (pop_size, n_obj)

In this lesson you will:
  1. Understand the shape contract of Problem._evaluate.
  2. Learn how ThreadPool.map parallelizes a function call.
  3. Implement ParallelRastriginProblem using Problem and ThreadPool.
  4. Wire everything together into a parallel solve function.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson10_parallelization.py
"""

import math
from multiprocessing.pool import ThreadPool

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Rastrigin helper — provided; used inside _evaluate to score one solution
# ---------------------------------------------------------------------------

def rastrigin(x):
    """Return the Rastrigin function value at point x (a sequence of floats)."""
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)


# ---------------------------------------------------------------------------
# Koan 01 — The shape contract of Problem._evaluate
# ---------------------------------------------------------------------------

def test_01_evaluate_shapes():
    """
    When pymoo calls Problem._evaluate, it passes the full population as a
    2D numpy array X of shape (pop_size, n_var). Each row is one solution.

    Your _evaluate must fill out["F"] with a 2D array of shape
    (pop_size, n_obj). Use reshape(-1, 1) to go from a flat list of
    scalar objectives to the required column-vector shape.

    Trace through the example below to understand both shapes.

    # TODO I noticed that the example objective functions for Koan 1 and 2. Use x_1 + x_2^2 + x_3^3 as the objective function, and introduce the assumption 
    
    """
    # TODO Change this to four solutions, three variables each. Change this for all of the other koans 
    X = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])   # 3 solutions, 3 variables each

    assert X.shape         == FILL_ME_IN   # (pop_size, n_var)
    assert X.shape[0]      == FILL_ME_IN   # number of solutions in this batch
    assert X.shape[1]      == FILL_ME_IN   # number of variables per solution
    assert list(X[0])      == FILL_ME_IN   # first solution (first row)

    # Compute one scalar objective per solution, then reshape for out["F"]
    f_values = [sum(x) for x in X]  
    assert f_values == FILL_ME_IN          # list of scalar objectives

    F = np.array(f_values).reshape(-1, 1)
    assert F.shape == FILL_ME_IN           # required shape for out["F"]


# ---------------------------------------------------------------------------
# Koan 02 — ThreadPool.map
# ---------------------------------------------------------------------------

def test_02_threadpool_map():
    """
    ThreadPool.map(f, X) is a concurrent drop-in for list(map(f, X)):
    it calls f on every element of X in parallel and returns results
    in the same order as the input.

    A ThreadPool uses OS threads, so it works on Windows without any
    import-guard and handles any callable without pickling.

    # TODO see feedback for test 01
    """
    serial   = list(map(abs, [-3, 1, -4, 1, -5]))
    with ThreadPool(2) as pool:
        parallel = list(pool.map(abs, [-3, 1, -4, 1, -5]))

    assert serial               == FILL_ME_IN   # result of applying abs serially
    assert parallel             == FILL_ME_IN   # same input, run concurrently
    assert (serial == parallel) == FILL_ME_IN   # do they agree?


# ---------------------------------------------------------------------------
# Koan 03 — Implement ParallelRastriginProblem
# ---------------------------------------------------------------------------

class ParallelRastriginProblem(Problem):
    """
    A pymoo Problem that evaluates the Rastrigin function in parallel.

    Because we subclass Problem (not ElementwiseProblem), pymoo calls
    _evaluate once per generation with the full population matrix X of
    shape (pop_size, n_var). We dispatch each row to a thread pool and
    pack the results into out["F"] of shape (pop_size, 1).

    Replace each `pass` with your implementation.

    Hints:
      __init__ — initializes the problem
      _evaluate — evaluates the objectives and constraints
  """

    def __init__(self, n_var=5, n_workers=4):
        pass  # TODO: implement this

    def _evaluate(self, X, out, *args, **kwargs):
        pass  # TODO: implement this


def test_03_parallel_rastrigin_problem():
    """
    Call _evaluate directly with three solutions at the global minimum.
    Every solution scores 0, and the output must have the required shape.
    """
    problem = ParallelRastriginProblem(n_var=5, n_workers=2)
    X   = np.zeros((3, 5))   # 3 solutions, all at the origin
    out = {}
    problem._evaluate(X, out)
    assert out["F"].shape == (3, 1)   # one objective per solution, column shape
    assert out["F"][0, 0] == 0.0      # Rastrigin at origin is 0


# ---------------------------------------------------------------------------
# Koan 04 — Solve with parallel evaluation
# ---------------------------------------------------------------------------

def solve_rastrigin_parallel(n_var=5, pop_size=100, n_gen=200, seed=1, n_workers=4):
    """
    Minimize the Rastrigin function using pymoo's GA with parallel objective
    evaluation inside _evaluate. Return (best_x, best_f).

    Because the ThreadPool lives inside _evaluate as a context manager,
    no explicit cleanup is needed here.

    Replace `pass` with your implementation.
    Hints:
      - Initialize the problem
      - Initialize the GA
      - Call minimize
      - Return res.X and res.F[0]
    """
    pass  # TODO: implement this


def test_04_solve_parallel():
    """
    The parallel solver must reach the same quality solution as the serial
    solver from lesson09: parallelization is transparent to the algorithm.
    """
    best_x, best_f = solve_rastrigin_parallel(
        n_var=5, pop_size=100, n_gen=200, seed=1, n_workers=4
    )
    assert len(best_x) == 5    # one value per variable
    assert best_f < 10.0       # near-optimal (global minimum is 0)
