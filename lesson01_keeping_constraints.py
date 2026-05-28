"""
Lesson 02 — Brute Force Optimization
======================================
The simplest optimization strategy: try every possible candidate,
score each one, and keep the best.

Brute force *guarantees* finding the global optimum — but only
when the search space is small enough to enumerate completely.

As the number of variables grows, the search space explodes:
with k choices per variable and n variables there are k^n candidates.
This is called the *curse of dimensionality*.

Understanding brute force matters because:
  1. It sets the baseline every smarter method must beat
  2. It reveals why real-world optimization algorithms exist
  3. It is the right tool when the search space is genuinely small

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson02_bruteForce.py
"""

from itertools import product

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — Brute force evaluates every candidate
# ---------------------------------------------------------------------------

def test_01_brute_force_evaluates_all():
    """
    Brute force works by calling f on every candidate in the search space
    and returning the one with the lowest score.
    """
    calls = []

    def f(x):
        calls.append(x)
        return (x - 4) ** 2   # minimum at x = 4

    candidates = range(0, 10)
    best = min(candidates, key=f)

    assert len(calls) == 10 # How many candidates were evaluated?
    assert best       == 4  # Which x minimises (x − 4)²?


# ---------------------------------------------------------------------------
# Koan 02 — Generating a 2-D search space
# ---------------------------------------------------------------------------

def test_02_grid_search_space():
    """
    For two variables, the search space is the Cartesian product of each
    variable's candidate values.  itertools.product builds it for you.
    """
    x1_values = [0, 1, 2]       # 3 choices for x1
    x2_values = [0, 1, 2, 3]    # 4 choices for x2
    space = list(product(x1_values, x2_values))

    assert len(space) == 12   # How many (x1, x2) pairs are there?
    assert space[0]   == (0, 0)   # What is the very first pair?
    assert space[-1]  == (2, 3)   # What is the very last pair?


# ---------------------------------------------------------------------------
# Koan 03 — Brute force over a 2-D space
# ---------------------------------------------------------------------------

def test_03_brute_force_2d():
    """
    Brute force generalizes to any number of variables: try every
    (x1, x2) pair and keep the one that minimises f.
    """

    def f(x1, x2):
        return (x1 - 1) ** 2 + (x2 - 2) ** 2   # minimum at (1, 2)

    space = product(range(5), range(5))   # x1, x2 ∈ {0, 1, 2, 3, 4}
    best = min(space, key=lambda p: f(*p))

    assert best == (1, 2)   # What (x1, x2) pair minimises f?


# ---------------------------------------------------------------------------
# Koan 04 — The search space grows exponentially
# ---------------------------------------------------------------------------

def test_04_exponential_growth():
    """
    With k choices per variable and n variables, there are k^n candidates.
    This 'curse of dimensionality' is why brute force breaks for large problems.
    """
    # 1 variable, 10 choices each → how many candidates?
    assert len(list(product(range(10), repeat=1))) == 10

    # 2 variables, 10 choices each → how many candidates?
    assert len(list(product(range(10), repeat=2))) == 100

    # 3 variables, 10 choices each → how many candidates?
    assert len(list(product(range(10), repeat=3))) == 1000


# ---------------------------------------------------------------------------
# Koan 05 — Brute force with a feasibility filter
# ---------------------------------------------------------------------------

def test_05_brute_force_with_constraint():
    """
    When a constraint exists, brute force first filters for feasible
    candidates, then minimises over that subset.
    """

    def f(x1, x2):
        return x1 + x2   # minimise total

    def is_feasible(x1, x2):
        return x1 + x2 >= 5   # constraint: sum must be at least 5

    all_candidates = list(product(range(6), range(6)))
    feasible = [(x1, x2) for x1, x2 in all_candidates if is_feasible(x1, x2)]
    best = min(feasible, key=lambda p: f(*p))

    assert len(feasible) == 21   # How many candidates are feasible?
    assert best          == (0,5)   # Which feasible pair minimises f?


# ---------------------------------------------------------------------------
# Koan 06 — Implement brute_force_minimize
# ---------------------------------------------------------------------------

def brute_force_minimize(f, x1_min, x1_max, x2_min, x2_max):
    """
    Return the (x1, x2) pair that minimises f over the integer grid
    x1 ∈ [x1_min, x1_max] and x2 ∈ [x2_min, x2_max] (both ends inclusive).

    Replace `pass` with your implementation.
    Hint: build the search space with product(range(...), range(...)).
    """
    
    space = product(range(x1_min, x1_max), range(x2_min, x2_max))   # x1, x2 ∈ {0, 1, 2, 3, 4}
    best = min(space, key=lambda p: f(p))
    return best


def test_06_implement_brute_force_minimize():
    def f(pair):
        x1, x2 = pair
        return (x1 - 2) ** 2 + (x2 - 3) ** 2   # minimum at (2, 3)

    result = brute_force_minimize(f, 0, 5, 0, 5)
    assert result == (2, 3), (
        "brute_force_minimize should return the (x1, x2) pair that makes f smallest"
    )
