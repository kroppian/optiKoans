"""
Answer-key regression tests for lesson08_geneticAlgorithm.py.

Each test mirrors one koan with the correct answer filled in.
All GA components are implemented here independently of the lesson file
so these tests never depend on student progress.
"""

import random


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

_weights  = [2, 5, 3, 7, 1, 4, 6, 3]
_values   = [4, 7, 5, 9, 2, 6, 8, 4]
_capacity = 15


# ---------------------------------------------------------------------------
# Reference implementations
# ---------------------------------------------------------------------------

def _initialize_population(pop_size, genome_length):
    return [[random.randint(0, 1) for _ in range(genome_length)] for _ in range(pop_size)]


def _objective(bits, weights, values):
    return -sum(b * v for b, v in zip(bits, values))


def _penalty(bits, weights, capacity, penalty_weight=1000):
    return max(0, sum(b * w for b, w in zip(bits, weights)) - capacity) * penalty_weight


def _tournament_select(population, scores):
    i, j = random.sample(range(len(population)), 2)
    winner = i if scores[i] <= scores[j] else j
    return population[winner]


def _crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]


def _mutate(bits, mutation_rate):
    return [1 - b if random.random() < mutation_rate else b for b in bits]


def _run_ga(weights, values, capacity, pop_size=50, n_generations=50,
            mutation_rate=0.125, seed=0):
    random.seed(seed)
    genome_length = len(weights)
    population = _initialize_population(pop_size, genome_length)
    scores = [_objective(ind, weights, values) + _penalty(ind, weights, capacity)
              for ind in population]
    n_elites = pop_size // 10
    for _ in range(n_generations):
        # Elitism: carry forward the best n_elites individuals unchanged
        elite_pairs = sorted(zip(scores, population))[:n_elites]
        elites = [ind for _, ind in elite_pairs]
        # Selection: two rounds of shuffle-and-pair tournaments → mating pool of N
        mating_pool = []
        for _round in range(2):
            combined = list(zip(population, scores))
            random.shuffle(combined)
            for k in range(0, pop_size, 2):
                (ind1, sc1), (ind2, sc2) = combined[k], combined[k + 1]
                mating_pool.append(ind1 if sc1 <= sc2 else ind2)
        # Reproduction: fill (pop_size - n_elites) child slots from shuffled mating pool
        random.shuffle(mating_pool)
        children = []
        k = 0
        while len(children) < pop_size - n_elites:
            c1, c2 = _crossover(mating_pool[k], mating_pool[k + 1])
            children.append(_mutate(c1, mutation_rate))
            if len(children) < pop_size - n_elites:
                children.append(_mutate(c2, mutation_rate))
            k += 2
        population = elites + children
        scores = [_objective(ind, weights, values) + _penalty(ind, weights, capacity)
                  for ind in population]
    _, best_ind = min(zip(scores, population))
    return best_ind


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_population_length():
    random.seed(0)
    pop = _initialize_population(pop_size=10, genome_length=8)
    assert len(pop) == 10


def test_koan01_genome_length():
    random.seed(0)
    pop = _initialize_population(pop_size=10, genome_length=8)
    assert len(pop[0]) == 8


def test_koan01_all_bits_valid():
    random.seed(0)
    pop = _initialize_population(pop_size=10, genome_length=8)
    assert all(b in (0, 1) for ind in pop for b in ind) == True


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_objective_optimal():
    assert _objective([1, 1, 1, 0, 1, 1, 0, 0], _weights, _values) == -24


def test_koan02_objective_empty():
    assert _objective([0, 0, 0, 0, 0, 0, 0, 0], _weights, _values) == 0


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_penalty_feasible():
    assert _penalty([1, 1, 1, 0, 1, 1, 0, 0], _weights, _capacity) == 0


def test_koan03_penalty_infeasible():
    assert _penalty([1, 1, 0, 1, 0, 1, 0, 0], _weights, _capacity) == 3000


def test_koan03_penalty_custom_weight():
    assert _penalty([1, 1, 0, 1, 0, 1, 0, 0], _weights, _capacity, penalty_weight=100) == 300


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_tournament_select_winner():
    pop2  = [[1, 1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 1, 0, 1]]
    scr2  = [-24, -21]
    winner = _tournament_select(pop2, scr2)
    assert winner == [1, 1, 1, 0, 1, 1, 0, 0]


def test_koan04_tournament_select_length():
    pop2  = [[1, 1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 1, 0, 1]]
    scr2  = [-24, -21]
    winner = _tournament_select(pop2, scr2)
    assert len(winner) == 8


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_crossover_children():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    random.seed(0)
    child1, child2 = _crossover(parent1, parent2)
    assert child1 == [1, 0, 1, 1, 0, 1, 0, 1]
    assert child2 == [0, 1, 0, 0, 1, 0, 1, 0]


def test_koan05_crossover_length():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    random.seed(0)
    child1, child2 = _crossover(parent1, parent2)
    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_mutate_deterministic():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(0)
    mutated = _mutate(genome, 0.5)
    assert mutated == [1, 0, 0, 1, 1, 1, 1, 1]


def test_koan06_mutate_length():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(0)
    mutated = _mutate(genome, 0.5)
    assert len(mutated) == len(genome)


def test_koan06_mutate_rate_extremes():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    assert _mutate(genome, 1.0) == [0, 1, 0, 1, 0, 1, 0, 1]
    assert _mutate(genome, 0.0) == genome


# ---------------------------------------------------------------------------
# Koan 07
# ---------------------------------------------------------------------------

def test_koan07_run_ga_finds_optimal():
    result = _run_ga(_weights, _values, _capacity, pop_size=50, n_generations=50,
                     mutation_rate=0.125, seed=0)
    assert result == [1, 1, 1, 0, 1, 1, 0, 0]


def test_koan07_run_ga_robust_across_seeds():
    for seed in [1, 7, 42, 99]:
        result = _run_ga(_weights, _values, _capacity, pop_size=50, n_generations=50,
                         mutation_rate=0.125, seed=seed)
        assert result == [1, 1, 1, 0, 1, 1, 0, 0], f"seed={seed} failed"
