"""
optiKoans — runner for Optimization Koans.

Usage:
    python optiKoans.py                             # global progress across all lessons
    python optiKoans.py lesson00_finding_good_answers.py   # run a single lesson
"""

import os
import sys
import glob as _glob

import pytest

# ── Windows UTF-8 fix ──────────────────────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))


def _lesson_files():
    return sorted(_glob.glob(os.path.join(ROOT, "lesson*.py")))


class _Counter:
    """Pytest plugin that tallies passed and failed tests."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1


def _count(filepath):
    """Return (passed, failed) for a lesson file by running pytest silently."""
    counter = _Counter()
    pytest.main(
        [filepath, "--rootdir", str(ROOT), "-p", "no:terminal"],
        plugins=[counter],
    )
    return counter.passed, counter.failed


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

BAR_WIDTH = 16
CYAN  = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD  = "\033[1m"


def _bar(passed, total):
    if total == 0:
        return "." * BAR_WIDTH
    filled = round(BAR_WIDTH * passed / total)
    return "#" * filled + "." * (BAR_WIDTH - filled)


def _print_progress(results):
    total_passed = sum(p for _, p, _ in results)
    total_koans  = sum(p + f for _, p, f in results)

    first_failing = next(
        (name for name, p, f in results if f > 0),
        None,
    )

    divider = "-" * 62
    print()
    print(f"  {BOLD}Path to Enlightenment{RESET}")
    print(f"  {divider}")

    for name, passed, failed in results:
        total   = passed + failed
        bar     = _bar(passed, total)
        status  = f"{GREEN}v{RESET}" if failed == 0 and total > 0 else " "
        pointer = f"  {CYAN}<-- you are here{RESET}" if name == first_failing else ""
        label   = os.path.splitext(name)[0]
        print(f"  {label:<42}  {bar}  {passed:>2}/{total:<2}  {status}{pointer}")

    print(f"  {divider}")
    print(f"  Total: {total_passed} / {total_koans} koans complete")
    print()

    print(f"total passed: {total_passed}")
    print(f"total koans:  {total_koans}")

    if total_passed != total_koans:
        print(f"You have not yet reached enlightenment. Breathe.")
        print(f"Be joyful that there is more to learn.")

    return first_failing


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def _run_single(filepath):
    if not os.path.isabs(filepath):
        filepath = os.path.join(ROOT, filepath)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    sys.stdout.flush()
    exit_code = pytest.main(
        [filepath, "-v", "--tb=short", "--rootdir", str(ROOT)],
    )

    if exit_code != 0:
        print(f"\n{CYAN}You have not yet reached enlightenment. Breathe.")
        print(f"Be joyful that there is more to learn.{RESET}")

    sys.exit(exit_code)


def _run_all():
    files = _lesson_files()
    if not files:
        print("No lesson files found.")
        sys.exit(0)

    results = []
    for filepath in files:
        name = os.path.basename(filepath)
        passed, failed = _count(filepath)
        results.append((name, passed, failed))

    first_failing = _print_progress(results)

    if first_failing:
        filepath = os.path.join(ROOT, first_failing)
        print(f"  Running {first_failing} ...\n")
        sys.stdout.flush()
        pytest.main(
            [filepath, "-v", "--tb=short", "--rootdir", str(ROOT)],
        )
        sys.exit(1)
    else:
        print(f"  {GREEN}{BOLD}All koans complete. You have reached enlightenment.{RESET}")
        sys.stdout.flush()
        sys.exit(0)


def main():
    args = sys.argv[1:]
    if args:
        _run_single(args[0])
    else:
        _run_all()


if __name__ == "__main__":
    main()
