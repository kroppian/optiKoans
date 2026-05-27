"""
Regression tests for the optiKoans platform.

Tests the FILL_ME_IN sentinel, the _count() parser, the _bar() formatter,
and the runner's exit-code behaviour. These have nothing to do with lesson
content and should always pass regardless of which koans a student has solved.

Run with:
    pytest tests/test_platform.py -v
"""

import os
import sys
import subprocess

import pytest

# Make optiKoans importable from the project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from optiKoans import _bar, _count, BAR_WIDTH  # noqa: E402
from conftest import FILL_ME_IN                  # noqa: E402

PYTHON = sys.executable
RUNNER = os.path.join(ROOT, "optiKoans.py")


# ---------------------------------------------------------------------------
# FILL_ME_IN sentinel
# ---------------------------------------------------------------------------

def test_fill_me_in_raises_assertion_error_right_side():
    """FILL_ME_IN on the right side of == should raise AssertionError."""
    with pytest.raises(AssertionError, match="Fill in the blank"):
        assert 5 == FILL_ME_IN


def test_fill_me_in_raises_assertion_error_left_side():
    """FILL_ME_IN on the left side of == should also raise AssertionError."""
    with pytest.raises(AssertionError):
        assert FILL_ME_IN == 5


def test_fill_me_in_repr():
    assert repr(FILL_ME_IN) == "FILL_ME_IN"


def test_fill_me_in_is_not_equal_to_anything():
    """__ne__ always returns True so FILL_ME_IN != x never silently passes."""
    assert FILL_ME_IN != 0
    assert FILL_ME_IN != ""
    assert FILL_ME_IN != None  # noqa: E711


# ---------------------------------------------------------------------------
# _bar() progress-bar formatter
# ---------------------------------------------------------------------------

def test_bar_all_empty():
    assert _bar(0, 6) == "." * BAR_WIDTH


def test_bar_all_full():
    assert _bar(6, 6) == "#" * BAR_WIDTH


def test_bar_half():
    bar = _bar(8, 16)
    assert bar.count("#") == bar.count(".")


def test_bar_zero_total():
    """Should not raise ZeroDivisionError."""
    assert _bar(0, 0) == "." * BAR_WIDTH


def test_bar_only_contains_expected_chars():
    bar = _bar(3, 10)
    assert all(c in "#." for c in bar)
    assert len(bar) == BAR_WIDTH


# ---------------------------------------------------------------------------
# _count() output parser
# ---------------------------------------------------------------------------

def test_count_all_pass(tmp_path):
    lesson = tmp_path / "lesson99_all_pass.py"
    lesson.write_text(
        "def test_a(): assert 1 == 1\n"
        "def test_b(): assert 2 == 2\n"
        "def test_c(): assert True\n"
    )
    passed, failed = _count(str(lesson))
    assert passed == 3
    assert failed == 0


def test_count_all_fail(tmp_path):
    lesson = tmp_path / "lesson99_all_fail.py"
    lesson.write_text(
        "def test_a(): assert 1 == 2\n"
        "def test_b(): assert False\n"
    )
    passed, failed = _count(str(lesson))
    assert passed == 0
    assert failed == 2


def test_count_mixed(tmp_path):
    lesson = tmp_path / "lesson99_mixed.py"
    lesson.write_text(
        "def test_ok():  assert True\n"
        "def test_bad(): assert False\n"
    )
    passed, failed = _count(str(lesson))
    assert passed == 1
    assert failed == 1


def test_count_empty_file_returns_zeros(tmp_path):
    lesson = tmp_path / "lesson99_empty.py"
    lesson.write_text("# no tests here\n")
    passed, failed = _count(str(lesson))
    assert passed == 0
    assert failed == 0


# ---------------------------------------------------------------------------
# Runner exit codes
# ---------------------------------------------------------------------------

def test_single_file_exits_1_when_koans_unsolved():
    """Unsolved lesson file → exit code 1."""
    r = subprocess.run(
        [PYTHON, RUNNER, "lesson00_finding_good_answers.py"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    assert r.returncode == 1


def test_missing_file_exits_1():
    """Non-existent file → exit code 1."""
    r = subprocess.run(
        [PYTHON, RUNNER, "lesson99_does_not_exist.py"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    assert r.returncode == 1


def test_global_run_exits_nonzero_when_unsolved():
    """Global run with unsolved koans should exit non-zero."""
    r = subprocess.run(
        [PYTHON, RUNNER],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    assert r.returncode != 0
