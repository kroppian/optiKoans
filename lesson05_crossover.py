"""
Lesson 05 — Genetic Algorithms Part 1: Crossover
========================
Monte Carlo drew candidates *independently* — each sample had no memory of
what worked before. Moving forward, we're going to explore concepts of genetic
algorithms, which use similar stochastic processes with a memory component. 
Genetic algorithms work by evolving an initial random "population" of 
solutions (i.e., a single Monte Carlo simulation) into increasingly better
solutions. This works by mimicking natural selection: nature's great optimizer.


In natural selection, the key reproduction operator is *crossover* (also called 
recombination). In binary optimization, two parent bit strings are split at a 
randomly chosen *crossover point* and their tails are swapped, producing two 
children that each inherit part of each parent's solution.

Why does this help?  Suppose parent1 has found a great selection of items
for positions 0–3, and parent2 has found a great selection for positions 4–7.
Crossover at point 4 produces a child that inherits *both* good halves — a
solution that neither parent could produce alone.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson05_crossover.py
"""

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — Splitting a bit string at the crossover point
# ---------------------------------------------------------------------------

def test_01_splitting_at_crossover_point():
    """
    A crossover point divides a bit string into a *head* (bits before the
    point) and a *tail* (bits from the point onward). Python's slice
    notation makes this easy: genome[:point] and genome[point:].
    """
    genome = [1, 0, 1, 1, 0, 1, 0, 0]
    point  = 4

    assert genome[:point] == [1, 0, 1, 1]   # what is the head?
    assert genome[point:] == [0, 1, 0, 0]  # what is the tail?


# ---------------------------------------------------------------------------
# Koan 02 — First child: head from parent1, tail from parent2
# ---------------------------------------------------------------------------

def test_02_first_child():
    """
    Child1 inherits the *head* of parent1 and the *tail* of parent2.
    It keeps parent1's item choices for the early positions and
    parent2's choices for the later ones.
    """
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    point   = 4

    child1 = parent1[:point] + parent2[point:]
    assert child1 == [1, 0, 1, 1, 1, 0, 1, 1]


# ---------------------------------------------------------------------------
# Koan 03 — Second child: head from parent2, tail from parent1
# ---------------------------------------------------------------------------

def test_03_second_child():
    """
    Child2 is the mirror image: head from parent2, tail from parent1.
    Together, child1 and child2 cover both combinations of the two halves.
    """
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    point   = 4

    child2 = parent2[:point] + parent1[point:]
    assert child2 == [0, 1, 0, 0, 0, 1, 0, 0]


# ---------------------------------------------------------------------------
# Koan 04 — Children are always the same length as their parents
# ---------------------------------------------------------------------------

def test_04_children_preserve_length():
    """
    Swapping tails never changes the total number of bits: the head shrinks
    by exactly as many bits as the tail grows, so length is preserved.
    """
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    point   = 7 

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    assert len(child1) == 8
    assert len(child2) == 8


# ---------------------------------------------------------------------------
# Koan 05 — Boundary case: crossover at point 0
# ---------------------------------------------------------------------------

def test_05_crossover_at_zero():
    """
    When point is 0, the head slice is empty, so child1 is made entirely
    from parent2's bits — it is a copy of parent2.
    """
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    point   = 0

    child1 = parent1[:point] + parent2[point:]
    assert child1 == [0, 1, 0, 0, 1, 0, 1, 1]   # which parent does child1 equal at point=0?


# ---------------------------------------------------------------------------
# Koan 06 — Implement crossover
# ---------------------------------------------------------------------------

def crossover(parent1, parent2, point):
    """
    Return (child1, child2) produced by single-point crossover at `point`.

    child1 takes its head from parent1 and its tail from parent2.
    child2 takes its head from parent2 and its tail from parent1.

    Replace `pass` with your implementation.
    Hint: use list slicing with [:point] and [point:], and the + operator.
    """
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return (child1, child2)


def test_06_implement_crossover():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    point   = 4

    child1, child2 = crossover(parent1, parent2, point)

    assert child1 == [1, 0, 1, 1, 1, 0, 1, 1]
    assert child2 == [0, 1, 0, 0, 0, 1, 0, 0]
    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)

    # At point=0: child1 is a copy of parent2, child2 is a copy of parent1
    c1, c2 = crossover(parent1, parent2, 0)
    assert c1 == parent2
    assert c2 == parent1
