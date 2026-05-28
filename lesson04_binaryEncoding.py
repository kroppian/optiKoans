"""
Lesson 04 — Binary Encoding
================================
So far, the optimization problems we have seen used continuous or integer
decision variables — a price, a grid coordinate, a sample from a range.

However, some problems can be represented as strings of binary strings. 
In other words, each candidate is a list of 0s and 1s called a *bit string*.
These will be increasingly relevant as we start learning about genetic 
algorithms. 

In this lesson the running example is the classic *0/1 knapsack*: given a
set of items with known weights and values, decide which items to put in a
bag without exceeding its weight capacity, while maximizing total value.

Each bit in the solution corresponds to one item:
  • 1  means "take the item"
  • 0  means "leave it behind"

A bit string therefore encodes a complete selection of items. The goal is
to find the bit string that maximizes value while staying within capacity.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson04_binaryEncoding.py
"""

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — A bit string represents which items to take
# ---------------------------------------------------------------------------

def test_01_bit_string_selects_items():
    """
    Each position in the bit string corresponds to one item.
    A 1 means "take it", a 0 means "leave it behind".
    Counting the 1s tells you how many items are selected.
    """
    # 8 items are available (indices 0–7)
    bits = [1, 0, 0, 0, 0, 0, 0, 0]      # only item 0 is taken
    assert sum(bits) == FILL_ME_IN       # how many items are selected?

    bits = [1, 0, 1, 0, 1, 0, 0, 0]      # items 0, 2, and 4 are taken
    assert sum(bits) == FILL_ME_IN       # how many items now?

    bits = [1, 1, 1, 0, 1, 1, 0, 0]      # items 0, 1, 2, 4, 5 are taken
    assert sum(bits) == FILL_ME_IN       # how many items now?


# ---------------------------------------------------------------------------
# Koan 02 — Compute total weight from a bit string
# ---------------------------------------------------------------------------

def test_02_total_weight():
    """
    Multiply each bit by the corresponding item weight and sum the results.
    Only items with bit == 1 contribute to the total weight.
    """
    #          item:  0  1  2  3  4  5  6  7
    weights       = [ 2, 5, 3, 7, 1, 4, 6, 3]
    bits          = [ 1, 0, 1, 0, 0, 0, 0, 0]   # take items 0 and 2

    total_weight = sum(b * w for b, w in zip(bits, weights))
    assert total_weight == FILL_ME_IN   # what is 1*2 + 0*5 + 1*3 + … ?


# ---------------------------------------------------------------------------
# Koan 03 — Compute total value from a bit string
# ---------------------------------------------------------------------------

def test_03_total_value():
    """
    Multiply each bit by the corresponding item value and sum the results.
    This is the quantity we want to maximize.
    """
    #          item:  0  1  2  3  4  5  6  7
    values        = [ 4, 7, 5, 9, 2, 6, 8, 4]
    bits          = [ 1, 0, 1, 0, 0, 0, 0, 0]   # same selection as koan 02

    total_value = sum(b * v for b, v in zip(bits, values))
    assert total_value == FILL_ME_IN    # what is 1*4 + 0*7 + 1*5 + … ?


# ---------------------------------------------------------------------------
# Koan 04 — A solution is feasible when it fits in the bag
# ---------------------------------------------------------------------------

def test_04_feasibility():
    """
    A selection is feasible if its total weight does not exceed capacity.
    Infeasible solutions are not valid answers — we must enforce this constraint.
    """
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    capacity = 15

    def total_weight(bits):
        return sum(b * w for b, w in zip(bits, weights))

    bits_a = [1, 1, 1, 0, 1, 1, 0, 0]   # weight = 2+5+3+1+4 = 15
    bits_b = [1, 1, 0, 1, 0, 1, 0, 0]   # weight = 2+5+7+4   = 18

    assert (total_weight(bits_a) <= capacity) == FILL_ME_IN   # is bits_a feasible?
    assert (total_weight(bits_b) <= capacity) == FILL_ME_IN   # is bits_b feasible?


# ---------------------------------------------------------------------------
# Koan 05 — Penalized Objective
# ---------------------------------------------------------------------------

def test_05_penalized_objective():
    """

    How do we handle constraints? One simple approach is to penalize the 
    objective function of infeasible solutions by adding a large number 
    proportional to the magnitude of the constraint violation. In the case
    of the knapsack problem, this would be how much the weight exceeds 
    capacity. This ensures infeasible candidates are always scored worse than 
    any feasible one.

      score = -total_value + max(0, total_weight - capacity) * penalty_weight
    """
    weights        = [2, 5, 3, 7, 1, 4, 6, 3]
    values         = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity       = 15
    penalty_weight = 1000

    def score(bits):
        tw = sum(b * w for b, w in zip(bits, weights))
        tv = sum(b * v for b, v in zip(bits, values))
        return -tv + max(0, tw - capacity) * penalty_weight

    bits_feasible   = [1, 1, 1, 0, 1, 1, 0, 0]   # value=24, weight=15
    bits_infeasible = [1, 1, 0, 1, 0, 1, 0, 0]   # value=26, weight=18

    assert score(bits_feasible)   == FILL_ME_IN   # what is the score?
    assert score(bits_infeasible) == FILL_ME_IN   # what is the score?

    # Lower score is better — which solution does the optimizer prefer?
    assert (score(bits_feasible) < score(bits_infeasible)) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 06 — Implement knapsack_score
# ---------------------------------------------------------------------------

def knapsack_score(bits, weights, values, capacity, penalty_weight=1000):
    """
    Return the GA objective score for a binary knapsack selection.

      score = -total_value + max(0, total_weight - capacity) * penalty_weight

    A feasible solution (total_weight <= capacity) incurs no penalty.
    An infeasible solution incurs a large positive penalty.
    Lower score is always better.

    Replace `pass` with your implementation.
    Hint: use zip(bits, weights) and zip(bits, values).
    """
    pass  # TODO: implement this


def test_06_implement_knapsack_score():
    weights  = [2, 5, 3, 7, 1, 4, 6, 3]
    values   = [4, 7, 5, 9, 2, 6, 8, 4]
    capacity = 15

    # Optimal feasible selection: value=24, weight=15 → no penalty
    assert knapsack_score([1, 1, 1, 0, 1, 1, 0, 0], weights, values, capacity) == -24

    # Infeasible selection: value=26, weight=18, violation=3 → big penalty
    assert knapsack_score([1, 1, 0, 1, 0, 1, 0, 0], weights, values, capacity) == 2974

    # All zeros: value=0, weight=0 → feasible but terrible
    assert knapsack_score([0, 0, 0, 0, 0, 0, 0, 0], weights, values, capacity) == 0

    # Custom penalty weight
    assert knapsack_score([1, 1, 0, 1, 0, 1, 0, 0], weights, values, capacity,
                          penalty_weight=100) == 274
