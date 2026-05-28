"""
Answer-key regression tests for lesson03_monteCarlo.py.

Each test mirrors one koan with the correct answer filled in.
monte_carlo_minimize is implemented here independently of the lesson file
so these tests never depend on student progress.
"""

import random


# ---------------------------------------------------------------------------
# Reference implementation (answer to koan 06)
# ---------------------------------------------------------------------------

def _monte_carlo_minimize(f, x1_min, x1_max, x2_min, x2_max, n_samples, seed):
    random.seed(seed)
    samples = [
        (random.randint(x1_min, x1_max), random.randint(x2_min, x2_max))
        for _ in range(n_samples)
    ]
    return min(samples, key=f)


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_sampling_integers_answers():
    random.seed(0)
    draw = random.randint(0, 9)
    assert 0 <= draw <= 9
    assert isinstance(draw, int)


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_seeds_answers():
    def best_of_ten(seed):
        random.seed(seed)
        return min(random.randint(0, 99) for _ in range(10))

    assert (best_of_ten(42) == best_of_ten(42)) == True
    assert (best_of_ten(42) == best_of_ten(7))  == False


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_best_of_n_samples_answer():
    def f(x):
        return (x - 50) ** 2

    random.seed(0)
    samples = [random.randint(0, 99) for _ in range(10)]
    best = min(samples, key=f)
    assert best == 49


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_more_samples_answers():
    def f(x):
        return (x - 50) ** 2

    random.seed(0)
    best_10 = min((random.randint(0, 99) for _ in range(10)), key=f)
    random.seed(0)
    best_1000 = min((random.randint(0, 99) for _ in range(1000)), key=f)

    assert abs(best_10   - 50) == 1
    assert abs(best_1000 - 50) == 0


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_2d_monte_carlo_answer():
    def f(x1, x2):
        return (x1 - 3) ** 2 + (x2 - 4) ** 2

    random.seed(2)
    samples = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(20)]
    best = min(samples, key=lambda p: f(*p))
    assert best == (2, 4)


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_implementation_evaluates_n_samples():
    calls = []

    def f(pair):
        calls.append(pair)
        x1, x2 = pair
        return (x1 - 5) ** 2 + (x2 - 5) ** 2

    result = _monte_carlo_minimize(f, 0, 9, 0, 9, n_samples=50, seed=0)

    assert len(calls) == 50
    assert result == min(list(calls), key=f)
