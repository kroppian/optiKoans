"""
Answer-key regression tests for lesson05_crossover.py.

Each test mirrors one koan with the correct answer filled in.
crossover is implemented here independently of the lesson file
so these tests never depend on student progress.
"""


# ---------------------------------------------------------------------------
# Reference implementation (answer to koan 06)
# ---------------------------------------------------------------------------

def _crossover(parent1, parent2, point):
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_splitting_answers():
    genome = [1, 0, 1, 1, 0, 1, 0, 0]
    point  = 4
    assert genome[:point] == [1, 0, 1, 1]
    assert genome[point:]  == [0, 1, 0, 0]


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_first_child_answer():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    child1  = parent1[:4] + parent2[4:]
    assert child1 == [1, 0, 1, 1, 1, 0, 1, 1]


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_second_child_answer():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    child2  = parent2[:4] + parent1[4:]
    assert child2 == [0, 1, 0, 0, 0, 1, 0, 0]


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_children_preserve_length():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    child1  = parent1[:4] + parent2[4:]
    child2  = parent2[:4] + parent1[4:]
    assert len(child1) == 8
    assert len(child2) == 8


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_crossover_at_zero():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    child1  = parent1[:0] + parent2[0:]
    assert child1 == [0, 1, 0, 0, 1, 0, 1, 1]
    assert child1 == parent2


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_crossover_basic():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]

    child1, child2 = _crossover(parent1, parent2, 4)
    assert child1 == [1, 0, 1, 1, 1, 0, 1, 1]
    assert child2 == [0, 1, 0, 0, 0, 1, 0, 0]
    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)


def test_koan06_crossover_boundary():
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]

    c1, c2 = _crossover(parent1, parent2, 0)
    assert c1 == parent2
    assert c2 == parent1


def test_koan06_crossover_all_points():
    """Reference solution preserves length and content at every crossover point."""
    parent1 = [1, 0, 1, 1, 0, 1, 0, 0]
    parent2 = [0, 1, 0, 0, 1, 0, 1, 1]
    for point in range(len(parent1) + 1):
        c1, c2 = _crossover(parent1, parent2, point)
        assert len(c1) == len(parent1)
        assert len(c2) == len(parent2)
        assert c1[:point] == parent1[:point]
        assert c1[point:]  == parent2[point:]
        assert c2[:point] == parent2[:point]
        assert c2[point:]  == parent1[point:]
