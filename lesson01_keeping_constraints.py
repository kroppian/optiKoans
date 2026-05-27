"""
Lesson 01 — Keeping Constraints
=================================
The real world is defined by constraints. A bridge can only hold so
much weight. A budget has a limit. A schedule has deadlines.

*Constraints* define which solutions are *feasible* (allowed) and which
are *infeasible* (not allowed). Optimization finds the best feasible
solution.

There are two main kinds:
  • Inequality constraint  g(x) ≤ 0   (e.g., weight ≤ capacity)
  • Equality constraint    h(x) = 0   (e.g., budget spent exactly)

Work through each koan. Replace FILL_ME_IN and implement any `pass` body.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and 
Copilot will not help you here. These tools strengthen the expert, 
but weaken the learner. Be a critical thinker. Comb through documentation, 
learn the tools of the trade. Only then, once you have mastered optimization, 
you may wield these tools. 

Run your progress with:
    python optiKoans.py lesson01_keeping_constraints.py
"""

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — Is a solution feasible?
# ---------------------------------------------------------------------------

def test_01_feasibility():
    """
    A solution is *feasible* if it satisfies all constraints.
    Here the only rule is: weight must not exceed the capacity of 10.
    """

    def is_feasible(weight, capacity=10):
        return weight <= capacity

    assert is_feasible(8)  == FILL_ME_IN   # Is a weight of 8 feasible?
    assert is_feasible(10) == FILL_ME_IN   # Is a weight of 10 feasible?
    assert is_feasible(12) == FILL_ME_IN   # Is a weight of 12 feasible?


# ---------------------------------------------------------------------------
# Koan 02 — Inequality constraints written in standard form  g(x) ≤ 0
# ---------------------------------------------------------------------------

def test_02_inequality_constraint_standard_form():
    """
    Textbooks write inequality constraints as  g(x) ≤ 0.
    The constraint "weight ≤ 10" becomes  g(x) = weight - 10 ≤ 0.
    A solution is feasible when g(x) ≤ 0.
    """

    def g(weight):
        return weight - 10   # feasible when g(weight) <= 0

    assert (g(8)  <= 0) == FILL_ME_IN   # Is weight=8  feasible?
    assert (g(10) <= 0) == FILL_ME_IN   # Is weight=10 feasible?
    assert (g(12) <= 0) == FILL_ME_IN   # Is weight=12 feasible?


# ---------------------------------------------------------------------------
# Koan 03 — Equality constraints  h(x) = 0
# ---------------------------------------------------------------------------

def test_03_equality_constraint():
    """
    An equality constraint forces a solution to hit an exact value.
    h(x) = x - 5 = 0 means x must equal exactly 5.
    """

    def h(x):
        return x - 5   # feasible only when h(x) == 0

    assert h(5)   == FILL_ME_IN   # What is h(5)?
    assert h(6)   == FILL_ME_IN   # What is h(6)?
    assert h(4.9) == FILL_ME_IN   # What is h(4.9)?

    # Is x=5 a feasible solution for this equality constraint?
    assert (h(5) == 0) == FILL_ME_IN   # True or False?


# ---------------------------------------------------------------------------
# Koan 04 — How much does a violation cost?
# ---------------------------------------------------------------------------

def test_04_violation_amount():
    """
    When a constraint is violated, we can measure *how much* it's violated.
    This is called the constraint violation amount.
    For equality consraints, a violation would be any value greater than or 
    less than 0 (i.e., any number not 0)
    For inequality constraints, traditionally a violation would be any value 
    greater than 0. 0 or negative values, on the other hand, are feasible.
    """

    def violation(weight, capacity=10):
        return max(0, weight - capacity)   # 0 if feasible, positive if not

    assert violation(8)  == FILL_ME_IN   # How much does weight=8  violate?
    assert violation(10) == FILL_ME_IN   # How much does weight=10 violate?
    assert violation(13) == FILL_ME_IN   # How much does weight=13 violate?


# ---------------------------------------------------------------------------
# Koan 05 — Multiple constraints must all be satisfied
# ---------------------------------------------------------------------------

def test_05_multiple_constraints():
    """
    A solution must satisfy *every* constraint to be feasible.
    Here: weight ≤ 10 AND cost ≤ 50.
    """

    def is_feasible(weight, cost):
        return weight <= 10 and cost <= 50

    assert is_feasible(8,  40) == FILL_ME_IN   # weight OK, cost OK
    assert is_feasible(12, 40) == FILL_ME_IN   # weight over, cost OK
    assert is_feasible(8,  60) == FILL_ME_IN   # weight OK, cost over
    assert is_feasible(12, 60) == FILL_ME_IN   # both over


# ---------------------------------------------------------------------------
# Koan 06 — Implement a penalty function   (function-implementation koan)
# ---------------------------------------------------------------------------

def penalty(weight, capacity=10, penalty_weight=1000):
    """
    Return the penalty for a constraint violation.

    Rules:
      • If weight <= capacity: penalty is 0  (solution is feasible)
      • Otherwise: penalty = (amount of violation) * penalty_weight

    Replace `pass` with your implementation.
    """
    pass  # TODO: implement this


def test_06_implement_penalty():
    assert penalty(8)  == 0,        "weight=8  is feasible — penalty should be 0"
    assert penalty(10) == 0,        "weight=10 is exactly at capacity — still 0"
    assert penalty(15) == 5 * 1000, "weight=15 exceeds capacity by 5 — penalty is 5000"
    assert penalty(11, capacity=10, penalty_weight=500) == 500
