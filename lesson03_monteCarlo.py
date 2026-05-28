"""
Lesson 03 — Monte Carlo Optimization
=======================================
Brute force guarantees finding the optimum, but only by exhausting every
candidate. For large search spaces that becomes prohibitively expensive.

Monte Carlo optimization takes a different approach: sample candidates
*at random* and keep the best one found. It is faster than brute force
because it doesn't search the whole space — it trades the guarantee of
optimality for speed.

Running a Monte Carlo algorithm has two key decisions to watch out for:
  1. Reproducibility — setting a *random seed* makes stochastic results
     repeatable, which is essential for testing and debugging.
  2. Budget — more samples means more of the space is explored, and the
     best result found likely gets closer to the true optimum.

Monte Carlo does not *learn* from the candidates it has already tried.
Each new sample is drawn independently, with no memory of what worked
before. That limitation motivates the next step: genetic algorithms, which
steer the random search by favouring regions that produced good scores.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson03_monteCarlo.py
"""

import random

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — Sampling integers at random
# ---------------------------------------------------------------------------

def test_01_sampling_integers():
    """
    random.randint(a, b) draws one integer uniformly at random from [a, b],
    both ends inclusive. Setting a seed makes the draw repeatable.
    """
    random.seed(0)
    draw = random.randint(0, 9)

    assert 0 <= draw <= FILL_ME_IN       # What is the largest possible value?
    assert isinstance(draw, FILL_ME_IN)  # What Python type does randint return?


# ---------------------------------------------------------------------------
# Koan 02 — Seeds make stochastic results reproducible
# ---------------------------------------------------------------------------

def test_02_seeds_make_results_reproducible():
    """
    Without a seed, two runs of the same sampling code produce different
    results. The same seed always produces the same sequence — essential
    for reproducible experiments and for writing tests of random methods.
    """
    def best_of_ten(seed):
        random.seed(seed)
        return min(random.randint(0, 99) for _ in range(10))

    assert (best_of_ten(42) == best_of_ten(42)) == FILL_ME_IN  # Same seed?
    assert (best_of_ten(42) == best_of_ten(7))  == FILL_ME_IN  # Different seed?


# ---------------------------------------------------------------------------
# Koan 03 — Seed selection: any integer works, results vary
# ---------------------------------------------------------------------------

def test_03_seed_selection():
    """
    Seeds can be any integer — 0, 42, 99999. The choice of seed doesn't
    make the algorithm better or worse; it determines *which* candidates
    are drawn. Run the same budget with a few different seeds to observe
    how much results vary with a small sample count.
    """
    def f(x):
        return (x - 50) ** 2   # minimum at x = 50

    def best_of_five(seed):
        random.seed(seed)
        return min((random.randint(0, 99) for _ in range(5)), key=f)

    results = [best_of_five(seed) for seed in [0, 1, 2]]

    # Do all three seeds produce the same best result?
    assert (results[0] == results[1] == results[2]) == FILL_ME_IN

    # What is the best result found across all three seeds?
    assert min(results, key=f) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 04 — Best of N random samples
# ---------------------------------------------------------------------------

def test_04_best_of_n_samples():
    """
    Monte Carlo scores each random candidate and keeps the best.
    Run this code yourself to see which sample lands closest to the optimum.
    """
    def f(x):
        return (x - 50) ** 2   # minimum at x = 50

    random.seed(0)
    samples = [random.randint(0, 99) for _ in range(10)]
    best = min(samples, key=f)

    assert best == FILL_ME_IN   # Which sample minimises f?


# ---------------------------------------------------------------------------
# Koan 05 — Increasing the budget to find the exact optimum
# ---------------------------------------------------------------------------

def test_05_increasing_budget_to_find_optimum():
    """
    With enough samples, Monte Carlo will eventually draw the exact optimum.
    The trade-off: more samples means better quality but more compute time.
    Try each budget below and find the smallest one that lands on x=50.
    """
    def f(x):
        return (x - 50) ** 2   # true optimum at x = 50, decision space is [0, 99]

    def best_of_n(n):
        random.seed(0)
        return min((random.randint(0, 99) for _ in range(n)), key=f)

    assert (best_of_n(10)  == 50) == FILL_ME_IN   # Best result with    10 samples?
    assert (best_of_n(50)  == 50) == FILL_ME_IN   # Best result with    50 samples?
    assert (best_of_n(200) == 50) == FILL_ME_IN   # Best result with   200 samples?

    # What is the smallest budget above that first hits the exact optimum?
    assert best_of_n(FILL_ME_IN) == 50


# ---------------------------------------------------------------------------
# Koan 06 — 2-D Monte Carlo sampling
# ---------------------------------------------------------------------------

def test_06_2d_monte_carlo():
    """
    Monte Carlo extends naturally to multiple variables: sample each
    variable independently and score the resulting pair.
    """
    def f(x1, x2):
        return (x1 - 3) ** 2 + (x2 - 4) ** 2   # minimum at (3, 4)

    random.seed(2)
    samples = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(20)]
    best = min(samples, key=lambda p: f(*p))

    assert best == FILL_ME_IN   # Which (x1, x2) pair minimises f?


# ---------------------------------------------------------------------------
# Koan 07 — Implement monte_carlo_minimize
# ---------------------------------------------------------------------------

def monte_carlo_minimize(f, x1_min, x1_max, x2_min, x2_max, n_samples, seed):
    """
    Return the (x1, x2) pair that approximately minimises f using random sampling.

    Draw n_samples random (x1, x2) pairs and return the one with the lowest
    f score.

    Parameters
    ----------
    f              : callable — takes (x1, x2), returns a float score
    x1_min, x1_max : int — inclusive bounds for x1
    x2_min, x2_max : int — inclusive bounds for x2
    n_samples      : int — number of random candidates to evaluate
    seed           : int — random seed for reproducibility

    Replace `pass` with your implementation.
    Hint: call random.seed(seed), then draw n_samples (x1, x2) pairs using
    random.randint for each variable.
    """
    pass  # TODO: implement this


def test_07_implement_monte_carlo_minimize():
    calls = []

    def f(pair):
        calls.append(pair)
        x1, x2 = pair
        return (x1 - 5) ** 2 + (x2 - 5) ** 2

    result = monte_carlo_minimize(f, 0, 9, 0, 9, n_samples=50, seed=0)

    assert len(calls) == FILL_ME_IN   # How many candidates should be evaluated?
    assert result == min(list(calls), key=f)
