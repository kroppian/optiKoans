"""
Lesson 08 — Putting It All Together: The Genetic Algorithm
===========================================================
Over the last four lessons you built every piece of a genetic algorithm:

  Lesson 04 — binary encoding and penalized objectives
  Lesson 05 — single-point crossover
  Lesson 06 — bit-flip mutation
  Lesson 07 — tournament selection

Now you assemble those pieces into a complete GA that reliably finds 
near-optimal (or sometimes globally optimal!) solution to the knapsack problem —
a solution neither brute force nor Monte Carlo can match within a reasonable 
compute budget.

The GA loop:
  1. *Initialize* a random population of N bit strings of length d.
  2. *Evaluate* every individual: objective + constraint penalty .
  3. Choose best 10% of the solutions to automatically go to next generation
  3. *Select* parents to form the mating pool with N members
  4. *Recombine* a randomly selected pair of two members of the mating pool
  5. *Mutate* each child to maintain diversity at a certain rate
  6. Repeat steps 4 and 5 until you have a new population of size N
  7. If you've hit the stopping criteria, go to step 8, else go to step 2
  8. Choose the bes solution from the population


Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson08_geneticAlgorithm.py
"""

import random

from conftest import FILL_ME_IN


weights  = [2, 5, 3, 7, 1, 4, 6, 3]
values   = [4, 7, 5, 9, 2, 6, 8, 4]
capacity = 15


# ---------------------------------------------------------------------------
# Koan 01 — Initialize a population
# ---------------------------------------------------------------------------

def initialize_population(pop_size, genome_length):
    """
    Return a list of `pop_size` random bit strings, each of length `genome_length`.

    Each bit string is a list of 0s and 1s drawn independently and uniformly
    at random. The caller seeds the RNG before calling this function.

    Replace `pass` with your implementation.
    Hint: use a nested list comprehension with random.randint(0, 1).
    """
    pass  # TODO: implement this


def test_01_initialize_population():
    random.seed(0)
    pop = initialize_population(pop_size=10, genome_length=8)

    assert len(pop) == FILL_ME_IN                                     # how many individuals?
    assert len(pop[0]) == FILL_ME_IN                                  # how long is each genome?
    assert all(b in (0, 1) for ind in pop for b in ind) == FILL_ME_IN  # all bits valid?
    all_bits = [b for ind in pop for b in ind]
    assert (0 in all_bits) == FILL_ME_IN   # does 0 appear? (not all-ones)
    assert (1 in all_bits) == FILL_ME_IN   # does 1 appear? (not all-zeros)


# ---------------------------------------------------------------------------
# Koan 02 — Objective function
# ---------------------------------------------------------------------------

def objective(bits, weights, values):
    """
    Return the objective value for minimization.

    The knapsack problem maximizes total item value. Because this GA
    minimizes, return the *negative* of the total value of selected items.

    Replace `pass` with your implementation.
    Hint: use sum(b * v for b, v in zip(bits, values)), then negate.
    """
    pass  # TODO: implement this


def test_02_objective():
    # Optimal selection picks items worth 24 total
    assert objective([1, 1, 1, 0, 1, 1, 0, 0], weights, values) == FILL_ME_IN
    # Empty selection has zero value
    assert objective([0, 0, 0, 0, 0, 0, 0, 0], weights, values) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 03 — Constraint penalty
# ---------------------------------------------------------------------------

def penalty(bits, weights, capacity, penalty_weight=1000):
    """
    Return the penalty for violating the weight constraint.

    Compute the total weight of selected items. If it exceeds `capacity`,
    the penalty is proportional to the excess:
        max(0, total_weight - capacity) * penalty_weight
    A feasible solution incurs zero penalty.

    Replace `pass` with your implementation.
    """
    pass  # TODO: implement this


def test_03_penalty():
    # Optimal selection: weight=15, capacity=15 → no violation
    assert penalty([1, 1, 1, 0, 1, 1, 0, 0], weights, capacity) == FILL_ME_IN
    # Infeasible selection: weight=18, excess=3 → penalty = 3 × 1000
    assert penalty([1, 1, 0, 1, 0, 1, 0, 0], weights, capacity) == FILL_ME_IN
    # Same infeasible selection with a smaller penalty weight
    assert penalty([1, 1, 0, 1, 0, 1, 0, 0], weights, capacity, penalty_weight=100) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 04 — Tournament selection
# ---------------------------------------------------------------------------

def tournament_select_matchup(population, scores):
    """
    Return the winner of a 2-individual binary tournament.

    Pick two distinct indices at random with random.sample and return
    the individual whose score is lower (better for minimization).

    The caller manages seeding.

    Replace `pass` with your implementation.
    Hint: use random.sample(range(len(population)), 2) to pick two indices.
    """
    pass  # TODO: implement this


def test_04_tournament_select_matchup():
    # With exactly 2 individuals, both are always drawn — the better one always wins.
    pop2  = [[1, 1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 1, 0, 1]]
    scr2  = [-24, -21]
    winner = tournament_select_matchup(pop2, scr2)
    assert winner == FILL_ME_IN    # which individual has the lower score?
    assert len(winner) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 05 — Crossover
# ---------------------------------------------------------------------------

def crossover(parent1, parent2):
    """
    Return (child1, child2) produced by single-point crossover.

    Choose a random crossover point in [1, len(parent1) - 1] using
    random.randint, then swap tails:
      child1 = parent1[:point] + parent2[point:]
      child2 = parent2[:point] + parent1[point:]

    Unlike lesson 05, the crossover point is chosen inside this function.
    The caller manages seeding.

    Replace `pass` with your implementation.
    """
    pass  # TODO: implement this


def test_05_crossover():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]

    # With seed=0, random.randint(1, 7) = 7 → only the last bit is swapped
    random.seed(0)
    child1, child2 = crossover(parent1, parent2)
    assert child1 == FILL_ME_IN
    assert child2 == FILL_ME_IN
    assert len(child1) == FILL_ME_IN
    assert len(child2) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 06 — Mutation
# ---------------------------------------------------------------------------

def mutate(bits, mutation_rate):
    """
    Return a new bit string where each bit has been independently flipped
    with probability `mutation_rate`.

    The caller manages seeding.

    Replace `pass` with your implementation.
    Hint: use a list comprehension; flip with `1 - b` when random.random() < mutation_rate.
    """
    pass  # TODO: implement this


def test_06_mutate():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]

    # Deterministic result with seed=0, rate=0.5
    random.seed(0)
    mutated = mutate(genome, 0.5)
    assert mutated == FILL_ME_IN
    assert len(mutated) == FILL_ME_IN

    # Rate=1.0 flips every bit regardless of seed
    assert mutate(genome, 1.0) == FILL_ME_IN
    # Rate=0.0 flips nothing regardless of seed
    assert mutate(genome, 0.0) == FILL_ME_IN


# ---------------------------------------------------------------------------
# Koan 07 — Run the genetic algorithm
# ---------------------------------------------------------------------------

def run_ga(weights, values, capacity, pop_size=50, n_generations=50,
           mutation_rate=0.125, seed=0):
    """
    Run a genetic algorithm to minimize the penalized knapsack objective.
    Returns the best individual from the final generation.

    pop_size must be even (individuals are paired for selection and crossover).

    Pseudocode — fill in each step:
      1. Seed the RNG with `seed`
      2. Initialize a population of pop_size random bit strings
         (genome_length = len(weights))
      3. Evaluate every individual:
             score = objective(ind, weights, values)
                   + penalty(ind, weights, capacity)
      4. Set n_elites = pop_size // 10
      5. For each generation:
           a. Elitism — identify and preserve the best individuals:
                  Sort individuals by score and take the top n_elites as elites

           b. Selection — build a mating pool of pop_size winners:
                  Do the following twice:
                      Randomly shuffle the current population (keeping scores aligned)
                      Walk through the shuffled list in adjacent pairs
                      For each pair, the individual with the lower score wins
                      Add each winner to the mating pool

           c. Reproduction — fill (pop_size - n_elites) child slots:
                  Randomly shuffle the mating pool and walk through adjacent pairs
                  For each pair, apply crossover to produce two children, then mutate each
                  Stop once you have enough children to fill the generation
                  population = elites + children

           d. Re-evaluate the new population (same formula as step 3)

      6. Return the best individual from the final population:
             _, best_ind = min(zip(scores, population))
             return best_ind
    """
    pass  # TODO: implement this


def test_07_run_ga():
    """
    With 10% elitism, the GA reliably finds the optimal knapsack solution.
    Optimal: [1,1,1,0,1,1,0,0] — weight=15, value=24, score=−24.
    """
    result = run_ga(weights, values, capacity, pop_size=50, n_generations=50,
                    mutation_rate=0.125, seed=0)
    assert result == [1, 1, 1, 0, 1, 1, 0, 0]
