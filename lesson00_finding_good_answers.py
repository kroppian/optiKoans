"""
Lesson 00 — Finding the best in problems 
=================================
The heart of optimization is finding the best answer to a problem. 

To do that, we need three things:
  1. A set of possible answers (the search space)
  2. A way to score each answer (the objective function)
  3. A rule for what "best" means — usually the lowest or highest score

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and 
Copilot will not help you here. These tools strengthen the expert, 
but weaken the learner. Be a critical thinker. Comb through documentation, 
learn the tools of the trade. Only then, once you have mastered optimization, 
you may wield these tools. 

To follow the path to optimization enlightenment, replace every FILL_ME_IN with 
the correct value, and implement every function that has a `pass` body.

Run your progress with:
    python optiKoans lesson00_finding_good_answers.py
"""

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — An objective function maps a solution to a score
# ---------------------------------------------------------------------------

def test_01_objective_function_returns_a_number():
    """An objective function takes a candidate solution and returns a number."""

    def f(x):
        return x ** 2

    assert f(0) == 0   # What is f(0)?
    assert f(3) == 9   # What is f(3)?
    assert f(-2) == 4  # What is f(-2)?


# ---------------------------------------------------------------------------
# Koan 02 — Lower is better (minimization)
# ---------------------------------------------------------------------------

def test_02_lower_is_better():
    """
    In minimization problems we want the smallest score.
    Given a list of scores, which one is best?
    """
    scores = [9, 4, 1, 0, 1, 4, 9]

    best_score = 0  # What is the minimum score in this list?
    assert min(scores) == best_score


# ---------------------------------------------------------------------------
# Koan 03 — The input that produces the best score
# ---------------------------------------------------------------------------

def test_03_finding_the_best_input():
    """
    We don't just care about the score — we care about the *input* that
    produced it. That input is called the optimum (or argmin).
    """

    def f(x):
        return (x - 3) ** 2   # this function is minimized at x = 3

    candidates = list(range(7))   # [0, 1, 2, 3, 4, 5, 6]

    best_x = 3  # Which x gives the lowest f(x)?
    assert best_x == min(candidates, key=f)


# ---------------------------------------------------------------------------
# Koan 04 — Maximization is flipped minimization
# ---------------------------------------------------------------------------

def test_04_maximization():
    """
    Sometimes we want the *highest* score (e.g. profit, accuracy).
    Maximizing f(x) is the same as minimizing -f(x).
    """

    def profit(price):
        return -(price - 5) ** 2 + 25   # peaks at price = 5

    candidates = list(range(11))   # prices 0 through 10

    best_price = 5  # Which price maximizes profit?
    assert best_price == max(candidates, key=profit)


# ---------------------------------------------------------------------------
# Koan 05 — Two variables, one score
# ---------------------------------------------------------------------------

def test_05_multi_variable_objective():
    """
    Objective functions can take more than one variable.
    Here, f(x1, x2) = x1^2 + x2^2 is minimized when both x1 and x2 are zero.
    """

    def f(x1, x2):
        return x1 ** 2 + x2 ** 2

    assert f(0, 0) == 0   # What is f(0, 0)?
    assert f(3, 4) == 25   # What is f(3, 4)?

    # Which (x1, x2) pair gives a lower score?
    lower_score_pair = (0, 0)  # Replace with (0, 0) or (3, 4)
    candidates = [(0, 0), (3, 4)]
    assert lower_score_pair == min(candidates, key=lambda p: f(*p))


# ---------------------------------------------------------------------------
# Koan 06 — Implement your own search  
# ---------------------------------------------------------------------------

def find_minimum(f, candidates):
    """
    Return the candidate x from `candidates` that minimizes f(x).

    Replace `pass` with your implementation.
    Hint: Python's built-in min() accepts a key= argument.
    """
    
    return min(candidates, key=f)


def test_06_implement_find_minimum():
    def f(x):
        return (x - 7) ** 2

    result = find_minimum(f, range(15))
    assert result == 7, (
        "find_minimum should return the x that makes f(x) smallest"
    )
