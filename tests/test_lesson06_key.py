"""
Answer-key regression tests for lesson06_mutation.py.

Each test mirrors one koan with the correct answer filled in.
mutate is implemented here independently of the lesson file
so these tests never depend on student progress.
"""

import random


# ---------------------------------------------------------------------------
# Reference implementations (answers to koans 01 and 06)
# ---------------------------------------------------------------------------

def _flip_bit(bit):
    assert bit in (0, 1), f"flip_bit expects 0 or 1, got {bit!r}"
    return 1 - bit


def _mutate(bits, mutation_rate):
    return [_flip_bit(b) if random.random() < mutation_rate else b for b in bits]


# ---------------------------------------------------------------------------
# Koan 01
# ---------------------------------------------------------------------------

def test_koan01_flip_bit():
    assert _flip_bit(1) == 0
    assert _flip_bit(0) == 1


def test_koan01_flip_bit_rejects_invalid():
    import pytest
    with pytest.raises(AssertionError):
        _flip_bit(2)


# ---------------------------------------------------------------------------
# Koan 02
# ---------------------------------------------------------------------------

def test_koan02_random_trial():
    random.seed(0)
    draw = random.random()
    assert (draw < 0.5) == False


# ---------------------------------------------------------------------------
# Koan 03
# ---------------------------------------------------------------------------

def test_koan03_mutate_a_genome():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(0)
    mutated = [_flip_bit(b) if random.random() < 0.5 else b for b in genome]
    assert mutated == [1, 0, 0, 1, 1, 1, 1, 1]


# ---------------------------------------------------------------------------
# Koan 04
# ---------------------------------------------------------------------------

def test_koan04_length_is_preserved():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(0)
    mutated = [_flip_bit(b) if random.random() < 0.5 else b for b in genome]
    assert len(mutated) == 8


# ---------------------------------------------------------------------------
# Koan 05
# ---------------------------------------------------------------------------

def test_koan05_rate_one_flips_everything():
    genome  = [1, 0, 1, 0, 1, 0, 1, 0]
    mutated = [_flip_bit(b) if random.random() < 1.0 else b for b in genome]
    assert mutated == [0, 1, 0, 1, 0, 1, 0, 1]


# ---------------------------------------------------------------------------
# Koan 06
# ---------------------------------------------------------------------------

def test_koan06_mutate_deterministic():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(0)
    assert _mutate(genome, 0.5) == [1, 0, 0, 1, 1, 1, 1, 1]


def test_koan06_mutate_rate_extremes():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    assert _mutate(genome, 1.0) == [0, 1, 0, 1, 0, 1, 0, 1]
    assert _mutate(genome, 0.0) == genome


def test_koan06_mutate_preserves_length():
    genome = [1, 0, 1, 0, 1, 0, 1, 0]
    random.seed(7)
    assert len(_mutate(genome, 0.25)) == len(genome)
