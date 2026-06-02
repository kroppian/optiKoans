"""
Lesson 07 — Genetic Algorithms Part 3: Tournament Selection
============================================================
Time to start putting things together! Moving forward, we're going to be 
optimizing *populations* of solutions, instead of just one or two solutions. 
Genetic algorithm will typically have tens or hundreds of members of a 
popluation, which will be gradually evolved over many generations. Having so many 
solutions, which are initially generated at random in a Monte Carlo simluation, 
allows us to increase our odds of finding optimal solutions, while keeping a 
diverse set of solutions to avoid local optima. 

The main pressure that drives a popluation to increasingly better solutions 
is selection. Good solutions are chosen, recombined, mutated, and they 
and their children cotinue to the next generation. Bad solutions are left in 
the fossil record. But how do we select the appropriate solutions for survival? 
Simply always choosing the best n individuals would cause the population to
converge to a single solution too early — we would lose the diversity that
makes the GA powerful. *Tournament selection* balances selection pressure
with diversity: randomly pick two individuals and let the better one win.
The winner enters the mating pool. Repeat until the pool is full.

Because the draw is random, even a mediocre individual occasionally enters
a tournament it can win, keeping the population from converging too early.
The infeasible individual is a natural exception — its large
objective value, penalized by because of its infeasibility, means it loses 
every possible tournament without any special
logic, so the penalty from Lesson 04 doubles as a selection barrier. However,
if we have many infeasible solutions (e.g., half of the popluation is 
infeasible), they may survive the selection. This allows the algorithm to 
explore largely infeasible spaces and stumble upon optimal solutions, while 
still penalizing infeasibility overall.

Selecting two individuals at a time is called *binary tournament selection*.
Larger tournaments apply more selection pressure (the best wins more often);
smaller tournaments preserve more diversity.

Work through each koan below by yourself. Claude, Gemini, ChatGPT, and
Copilot will not help you here. These tools strengthen the expert,
but weaken the learner. Be a critical thinker. Comb through documentation,
learn the tools of the trade. Only then, once you have mastered optimization,
you may wield these tools.

Run your progress with:
    python optiKoans.py lesson07_selection.py
"""

import random

from conftest import FILL_ME_IN


# Knapsack population fixture (scores computed with penalty_weight=1000)
population = [
    [1, 1, 1, 0, 1, 1, 0, 0],   # score =  -24  (optimal    — weight=15, value=24)
    [1, 0, 1, 0, 1, 1, 0, 1],   # score =  -21  (feasible   — weight=13, value=21)
    [1, 1, 0, 1, 0, 1, 0, 0],   # score = 2974  (infeasible — weight=18, penalty kicks in)
    [0, 0, 0, 0, 0, 0, 0, 0],   # score =    0  (picks nothing)
]
scores = [-24, -21, 2974, 0]


# ---------------------------------------------------------------------------
# Koan 01 — Population structure
# ---------------------------------------------------------------------------

def test_01_population_structure():
    """
    A population is a list of individuals. Each individual is a bit string,
    and each has a corresponding score in the `scores` list.
    """
    assert len(population) == 4   # how many individuals in this population?
    assert population[0]   == [1, 1, 1, 0, 1, 1, 0, 0]   # what is the first individual?


# ---------------------------------------------------------------------------
# Koan 02 — Finding the best individual
# ---------------------------------------------------------------------------

def test_02_finding_the_best():
    """
    In minimization, the best individual has the lowest score.
    `min(scores)` gives the best score; `scores.index(...)` locates it.
    """
    best_score = min(scores)
    assert best_score == -24                            # what is the lowest score?
    assert population[scores.index(best_score)] == population[0]  # which individual has it?


# ---------------------------------------------------------------------------
# Koan 03 — Tournament: optimal vs infeasible
# ---------------------------------------------------------------------------

def test_03_tournament_optimal_vs_infeasible():
    """
    Two contestants enter: index 0 (score=−24) vs index 2 (score=2974).
    The tournament rule: the contestant with the lower score wins.
    """
    i, j = 0, 2
    winner = i if scores[i] <= scores[j] else j
    assert winner == 0    # which index wins this tournament?


# ---------------------------------------------------------------------------
# Koan 04 — Tournament: suboptimal vs all-zeros
# ---------------------------------------------------------------------------

def test_04_tournament_suboptimal_vs_zeros():
    """
    Two contestants enter: index 1 (score=−21) vs index 3 (score=0).
    Even a solution that is not optimal beats a solution that picks nothing.
    """
    i, j = 1, 3
    winner = i if scores[i] <= scores[j] else j
    assert winner == 1  # which index wins this tournament?


# ---------------------------------------------------------------------------
# Koan 05 — Infeasible always loses
# ---------------------------------------------------------------------------

def test_05_infeasible_always_loses():
    """
    The infeasible individual's penalty score (2974) is larger than any
    feasible individual's score. In every possible match-up with a 
    feasible solution, it will loose. 
    We can verify: `min(other_score, 2974) < 2974` is always True.
    """
    # Does infeasible lose to the optimal (score=−24)?
    assert (min(-24, 2974) < 2974) == True    # True or False?
    # Does infeasible lose to the suboptimal (score=−21)?
    assert (min(-21, 2974) < 2974) == True    # True or False?
    # Does infeasible lose to the all-zeros (score=0)?
    assert (min(  0, 2974) < 2974) == True    # True or False?


# ---------------------------------------------------------------------------
# Koan 06 — Implement tournament_select_matchup
# ---------------------------------------------------------------------------

def tournament_select_matchup(population, scores):
    """
    Run a single 2-individual binary tournament.

    Choose two distinct indices at random from the population using
    random.sample. Compare their scores and return the bit string of
    the individual with the lower score (better in minimization).

    This function does NOT set a random seed — the caller is responsible
    for seeding before calling tournament_select_matchup() for reproducible results.

    Replace `pass` with your implementation.
    Hint: use random.sample(range(len(population)), 2) to pick two indices.
    """
    i, j = random.sample(range(len(population)), 2)
    winner = i if scores[i] <= scores[j] else j
    return population[winner]


def test_06_implement_tournament_select_matchup():
    # With only 2 individuals, both are always drawn — the better one always wins.
    # No seed needed: the lower-score individual wins regardless of draw order.
    pop2  = [[1, 1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 1, 0, 1]]
    scr2  = [-24, -21]
    winner = tournament_select_matchup(pop2, scr2)
    assert winner == [1, 1, 1, 0, 1, 1, 0, 0]    # score -24 beats score -21
    assert len(winner) == 8


# ---------------------------------------------------------------------------
# Koan 07 — Implement tournament_select
# ---------------------------------------------------------------------------

def tournament_select(population, scores, n):
    """
    Build a mating pool of n individuals by running n independent
    binary tournaments. Each call to tournament_select_matchup adds one winner.

    This function does NOT set a random seed — the caller is responsible
    for seeding before calling tournament_select() for reproducible results.

    Replace `pass` with your implementation.
    Hint: use a list comprehension that calls tournament_select_matchup n times.
    """
    selected = [tournament_select_matchup(population, scores) for _ in range(n)]
    
    return selected


def test_07_implement_tournament_select():
    """
    Selection pressure: the mean score of the selected pool should be
    lower (better) than the mean score of the original population, because
    good individuals win tournaments more often than bad ones.
    """
    mean_original = sum(scores) / len(scores)   # = (-24 + -21 + 2974 + 0) / 4 = 732.25

    random.seed(0)
    selected = tournament_select(population, scores, n=200)
    selected_scores = [scores[population.index(w)] for w in selected]
    mean_selected = sum(selected_scores) / len(selected_scores)

    assert len(selected) == 200                  # must return exactly n individuals
    assert mean_selected < mean_original         # selection pressure improves the pool
