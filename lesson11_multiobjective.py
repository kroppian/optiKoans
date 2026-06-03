"""
Lesson 11 — Multiobjective Optimization
========================================
In lessons 04 through 08 you solved the knapsack problem by combining value
and weight into a single penalized score:

    score = −total_value + max(0, total_weight − capacity) × penalty_weight

That formulation hides a tradeoff inside `penalty_weight`. A large penalty
favors light, feasible solutions; a small penalty lets heavy, high-value
solutions survive. Every choice of penalty_weight encodes a preference you
may not have consciously made.

*Multiobjective optimization* (MOO) makes the tradeoff explicit. Instead of
collapsing two competing goals into one number, you optimize them
simultaneously and return a *Pareto front*: the set of solutions where you
cannot improve one objective without worsening another.

For the knapsack we expose two objectives:

    f1 = −total_value   (minimize → maximize value)
    f2 =  total_weight  (minimize → prefer lighter solutions)

No single solution is "best" — a high-value solution is necessarily heavier.
The Pareto front shows the full spectrum of tradeoffs and lets the
decision-maker choose based on their actual preference.

pymoo's NSGA-II algorithm finds Pareto fronts the same way its GA finds a
single optimum. The API change is minimal: swap `GA` for `NSGA2`, set
`n_obj=2`, and read a matrix of solutions instead of a single vector.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson11_multiobjective.py
"""

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Knapsack fixture — same 8-item instance used in lessons 04–08
# ---------------------------------------------------------------------------

weights  = [2, 5, 3, 7, 1, 4, 6, 3]
values   = [4, 7, 5, 9, 2, 6, 8, 4]
capacity = 15   # kept as a reference point; not enforced as a hard constraint


# ---------------------------------------------------------------------------
# Helper — provided; used throughout the lesson
# ---------------------------------------------------------------------------

def knapsack_objectives(bits, weights, values):
    """Return (−total_value, total_weight) for a bit string.

    These are the two objectives NSGA-II minimizes:
      - minimizing −total_value  is equivalent to maximizing value
      - minimizing total_weight  prefers lighter selections
    """
    total_value  = sum(b * v for b, v in zip(bits, values))
    total_weight = sum(b * w for b, w in zip(bits, weights))
    return (-total_value, total_weight)


# ---------------------------------------------------------------------------
# Koan 01 — Two objectives
# ---------------------------------------------------------------------------

def test_01_two_objectives():
    """
    Instead of a single penalized score, MOO tracks both objectives
    separately. Trace through three extreme selections to see the range
    of values each objective can take.

    The lesson-08 optimal selection maximizes value within the weight limit.
    Picking nothing is trivially light but worthless.
    Picking everything is the most valuable but also the heaviest.
    """
    # Lesson-08 optimal: value=24, weight=15
    assert knapsack_objectives([1, 1, 1, 0, 1, 1, 0, 0], weights, values) == FILL_ME_IN

    # Pick nothing: value=0, weight=0
    assert knapsack_objectives([0, 0, 0, 0, 0, 0, 0, 0], weights, values) == FILL_ME_IN

    # Pick everything: value=45, weight=31
    assert knapsack_objectives([1, 1, 1, 1, 1, 1, 1, 1], weights, values) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 02 — Pareto dominance
# ---------------------------------------------------------------------------

def test_02_pareto_dominance():
    """
    Solution A *dominates* solution B when A is no worse than B on every
    objective AND strictly better on at least one.

    The *Pareto front* is the set of solutions that no other solution
    dominates — these are the genuinely optimal tradeoffs.

    Work through the three comparisons below. Each uses the
    dominance check for two objectives (f1, f2) where lower is better:

        A dominates B  iff  A.f1 <= B.f1  and  A.f2 <= B.f2
                            (with at least one strict inequality)

    Useful shortcut: if both conditions hold, A is at least as good on
    both objectives; and because the values differ, at least one must
    be strictly better.
    """
    # A = (-24, 15): value=24, weight=15  (lesson-08 optimal)
    # B = (-21, 13): value=21, weight=13  (lighter but less valuable)
    # A has better f1 (-24 < -21) but worse f2 (15 > 13) → neither dominates
    assert ((-24 <= -21) and (15 <= 13)) == FILL_ME_IN   # does A dominate B?

    # A = (-24, 15): value=24, weight=15
    # C = (-20, 16): value=20, weight=16  (worse on both)
    # A has better f1 (-24 < -20) AND better f2 (15 < 16) → A dominates C
    assert ((-24 <= -20) and (15 <= 16)) == FILL_ME_IN   # does A dominate C?

    # The Pareto front of {A=(-24,15), B=(-21,13), C=(-20,16)}:
    # A dominates C, so C is excluded. A and B are mutually non-dominated.
    # How many solutions are on the Pareto front?
    assert FILL_ME_IN == 2


# ---------------------------------------------------------------------------
# Koan 03 — Implement KnapsackMOO
# ---------------------------------------------------------------------------

class KnapsackMOO(ElementwiseProblem):
    """
    A pymoo problem that evaluates two knapsack objectives independently.

    Because we subclass ElementwiseProblem, pymoo calls _evaluate once per
    solution (one row of the population at a time). Variables are continuous
    in [0, 1]; round them to the nearest integer inside _evaluate to recover
    binary item selections.

    Replace each `pass` with your implementation.

    Hints:
      __init__  — call super().__init__ with n_var=8, n_obj=2,
                  xl=np.zeros(8), xu=np.ones(8)
      _evaluate — bits = x.round().astype(int)
                  compute total_value and total_weight from bits
                  set out["F"] = [-total_value, total_weight]
    """

    def __init__(self):
        pass  # TODO: implement this

    def _evaluate(self, x, out, *args, **kwargs):
        pass  # TODO: implement this


def test_03_knapsack_moo_problem():
    """
    Call _evaluate directly with the lesson-08 optimal bit string.
    The two objectives should be (-24, 15): value=24, weight=15.
    """
    problem = KnapsackMOO()
    out = {}
    problem._evaluate(np.array([1, 1, 1, 0, 1, 1, 0, 0], dtype=float), out)
    assert list(out["F"]) == FILL_ME_IN   # [−value, weight] for the optimal selection


# ---------------------------------------------------------------------------
# Koan 04 — NSGA-II result shape
# ---------------------------------------------------------------------------

def test_04_result_shape():
    """
    In lesson 09, GA returned a single best solution:
      res.X  — a 1D vector of length n_var
      res.F  — a 1D array of length 1 (one objective)

    NSGA-II returns the *entire Pareto front*:
      res.X  — a 2D matrix, one row per Pareto-optimal solution
      res.F  — a 2D matrix, one row per solution, one column per objective

    Trace through the shapes below. A quick run (n_gen=50) is used here
    so the test finishes fast; you will use more generations in koan 05.
    """
    problem   = KnapsackMOO()
    algorithm = NSGA2(pop_size=50)
    res       = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=False)

    assert res.X.ndim      == FILL_ME_IN   # is res.X a 1D vector or a 2D matrix?
    assert res.F.shape[1]  == FILL_ME_IN   # how many objective columns?
    assert res.X.shape[1]  == FILL_ME_IN   # how many variable columns?
    assert (len(res.X) > 1) == FILL_ME_IN  # does NSGA-II return more than one solution?


# ---------------------------------------------------------------------------
# Koan 05 — Solve and read the Pareto front
# ---------------------------------------------------------------------------

def solve_knapsack_moo(pop_size=100, n_gen=200, seed=1):
    """
    Minimize both knapsack objectives simultaneously using NSGA-II.
    Return (pareto_X, pareto_F) where:
      pareto_X — 2D array of Pareto-optimal bit strings, shape (n_pareto, 8)
      pareto_F — 2D array of objective pairs,            shape (n_pareto, 2)

    Replace `pass` with your implementation.
    Hints:
      - Initialize KnapsackMOO()
      - Initialize NSGA2(pop_size=pop_size)
      - Call minimize(problem, algorithm, ('n_gen', n_gen), seed=seed, verbose=False)
      - Return res.X and res.F
    """
    pass  # TODO: implement this


def test_05_solve():
    """
    The Pareto front should contain multiple solutions representing the
    full value-vs-weight tradeoff. The best value on the front should
    be at least as good as the lesson-08 single-objective optimal (−24).
    """
    pareto_X, pareto_F = solve_knapsack_moo(pop_size=100, n_gen=200, seed=1)

    assert pareto_F.shape[1]   == FILL_ME_IN    # two objectives per solution
    assert pareto_X.shape[1]   == FILL_ME_IN    # eight variables per solution
    assert (len(pareto_X) > 1) == FILL_ME_IN    # multiple Pareto-optimal solutions

    # The solution with the lowest −value (highest item value) on the front
    # should match or beat the lesson-08 optimal of value=24 (f1=−24).
    best_value_idx = np.argmin(pareto_F[:, 0])
    assert pareto_F[best_value_idx, 0] <= -24
