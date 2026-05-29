"""
Lesson 06 — Genetic Algorithms Part 2: Mutation
=================================================
So far, we have learned two building blocks of genetic algorithms: 
a Monte Carlo generation of random points, which we can then 
recombine the best solutions of with crossover to (hopefully) create
better solutions. However, what happens when every individual in the population 
has a 0 in position 3? No amount of crossover can ever produce a 1 there —
the population is stuck, and optimization halts. 

*Mutation* fixes this. After crossover, each bit in a child is
independently flipped with a small probability called the *mutation rate*.
This injects fresh genetic diversity, letting the search escape local
optima and explore parts of the space the population has never visited.

The mutation rate is a trade-off:
  • Too low  → population converges on an local optima prematurely, can get stuck
  • Too high → search becomes random, ignores what was already learned

A typical rate for an 8-bit genome is 1/8 ≈ 0.125 (flip roughly one bit).

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson06_mutation.py
"""

import random

from conftest import FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 01 — Implement flip_bit
# ---------------------------------------------------------------------------

def flip_bit(bit):
    """
    Flip a single binary bit: 1 → 0, 0 → 1.
    Raises AssertionError if bit is not exactly 0 or 1 — this protects
    the rest of the GA from accidentally processing corrupted genomes.

    Replace `pass` with your implementation.
    Hint: assert bit in (0, 1), then return 1 - bit.
    """

    assert bit in (0, 1), f"flip_bit expects 0 or 1, got {bit!r}"

    pass  # TODO: implement this


def test_01_flip_bit():
    """flip_bit converts 1 to 0 and 0 to 1. Any other input raises AssertionError."""
    assert flip_bit(1) == FILL_ME_IN   # flip a 1 → ?
    assert flip_bit(0) == FILL_ME_IN   # flip a 0 → ?


# ---------------------------------------------------------------------------
# Koan 02 — A random draw decides whether each bit flips
# ---------------------------------------------------------------------------

def test_02_random_trial():
    """
    For each bit, we draw a random number in [0, 1). If that draw is below
    the mutation rate, the bit flips; otherwise it stays the same.
    A higher mutation rate means a greater chance of flipping.
    """
    random.seed(0)
    draw = random.random()   # first draw with seed 0

    rate = 0.5
    assert (draw < rate) == FILL_ME_IN   # does this draw trigger a flip?


# ---------------------------------------------------------------------------
# Koan 03 — Applying mutation to a full genome
# ---------------------------------------------------------------------------

def test_03_mutate_a_genome():
    """
    Run a random trial for every bit in the genome.
    With seed=0 and rate=0.5, only some bits flip — trace the draws to see which.
    """
    genome = [1, 0, 1, 0, 1, 0, 1, 0]

    random.seed(0)
    mutated = [flip_bit(b) if random.random() < 0.5 else b for b in genome]

    assert mutated == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 04 — Mutation preserves genome length
# ---------------------------------------------------------------------------

def test_04_length_is_preserved():
    """
    Flipping individual bits never adds or removes bits, so the mutated
    genome is always the same length as the original.
    """
    genome = [1, 0, 1, 0, 1, 0, 1, 0]

    random.seed(0)
    mutated = [flip_bit(b) if random.random() < 0.5 else b for b in genome]

    assert len(mutated) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 05 — Rate 1.0 flips every bit
# ---------------------------------------------------------------------------

def test_05_rate_one_flips_everything():
    """
    When mutation rate is 1.0, every draw satisfies (draw < 1.0) because
    random.random() always returns a value strictly less than 1.
    Every bit flips — the result is the bitwise complement of the genome.
    """
    genome  = [1, 0, 1, 0, 1, 0, 1, 0]
    mutated = [flip_bit(b) if random.random() < 1.0 else b for b in genome]

    assert mutated == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 06 — Implement mutate
# ---------------------------------------------------------------------------

def mutate(bits, mutation_rate):
    """
    Return a new bit string where each bit has been independently flipped
    with probability `mutation_rate`.

    This function does NOT set a random seed — the caller is responsible
    for seeding before calling mutate() to get reproducible results.

    Replace `pass` with your implementation.
    Hint: use a list comprehension with random.random() and flip_bit.
    """
    pass  # TODO: implement this


def test_06_implement_mutate():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]

    # With seed=0 and rate=0.5, we get a specific deterministic result
    random.seed(0)
    mutated = mutate(genome, 0.5)
    assert mutated == [1, 0, 0, 1, 1, 1, 1, 1]
    assert len(mutated) == len(genome)

    # Rate=1.0 flips every bit regardless of seed
    assert mutate(genome, 1.0) == [0, 1, 0, 1, 0, 1, 0, 1]

    # Rate=0.0 flips nothing regardless of seed
    assert mutate(genome, 0.0) == genome
