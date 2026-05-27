# Optimization Koans

Optimization Koans teaches you how to find the best answers to hard problems
— one small exercise at a time. Inspired by [Ruby Koans](https://www.rubykoans.com/),
each lesson is a Python file full of tests that fail until you fill them in.

## What You Will Learn

| Lesson | Topic |
|--------|-------|
| `lesson00_finding_good_answers.py` | Objective functions, minimization, search |
| `lesson01_keeping_constraints.py` | Feasibility, inequality and equality constraints |
| `lesson02_bruteForce.py` | Exhaustive search, Cartesian product, curse of dimensionality |

---

## Setup

**1. Install [Anaconda](https://www.anaconda.com/download) or Miniconda**, then create
the project environment:

```bash
conda env create -f environment.yml
conda activate optikoans
```

**2. Verify the install:**

```bash
python optiKoans.py
```

~~You should see a progress table with all koans listed as `0/N`.~~ (WIP)

---

## How to Use

### Work through a lesson

Open a lesson file (e.g. `lesson00_finding_good_answers.py`) in your editor.
Read the comments, then replace every `FILL_ME_IN` with the correct value and
implement every function that has a `pass` body.

Test your progress on that lesson:

```bash
python optiKoans.py lesson00_finding_good_answers.py
```

Pytest will tell you exactly which koan failed and what it expected.
Fix it, save, and re-run. Repeat until all tests in the file pass.

### Check your global progress

```bash
python optiKoans.py
```

~~This prints a progress bar for every lesson and re-runs the first lesson that still has failing koans, so you always know exactly where to focus.~~ (WIP)

---

## The Rules

1. **Only edit lesson files.** Don't change `conftest.py` or the runner.
2. **Replace `FILL_ME_IN`** with a value (number, boolean, tuple, …).
3. **Replace `pass`** with a real implementation.
4. **Don't hard-code the expected value** from the test assertion — understand
   *why* the answer is correct.

---

## Project Structure

```
Optimization-Koans/
├── optiKoans.py                # runner (python optiKoans.py)
├── environment.yml             # Anaconda environment
├── conftest.py                 # shared test helpers (do not edit)
├── lesson00_finding_good_answers.py
├── lesson01_keeping_constraints.py
└── lesson02_bruteForce.py
```
