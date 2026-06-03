Optimization Koans is a Ruby-Koans-inspired Python project teaching undergraduate students optimization through fill-in-the-blank exercises with immediate pytest feedback.

**Why:** Make optimization accessible by guiding students koan-by-koan. Inspired by https://www.rubykoans.com/

---

## Environment

- **Conda env name:** `optikoans`
- **Miniconda location:** `C:\Users\i-kropp\AppData\Local\miniconda3`
- **Python interpreter:** `C:\Users\i-kropp\AppData\Local\miniconda3\envs\optikoans\python.exe`
- **Create env:** `conda env create -f environment.yml` (from project root)
- **Key packages:** python 3.11, pytest 9.0.3, numpy, scipy, matplotlib
- **Run tests:** `& "C:\Users\i-kropp\AppData\Local\miniconda3\envs\optikoans\python.exe" -m pytest tests/ --tb=short`

---

## Project Structure

```
Optimization-Koans/
├── optiKoans.py                  # CLI runner (python optiKoans.py [file])
├── conftest.py                   # FILL_ME_IN sentinel (auto-loaded by pytest)
├── environment.yml               # Anaconda env named "optikoans"
├── lesson00_finding_good_answers.py
├── lesson01_keeping_constraints.py
├── lesson02_bruteForce.py
├── lesson03_monteCarlo.py
├── lesson04_binaryEncoding.py
├── lesson05_crossover.py
├── lesson06_mutation.py
├── lesson07_selection.py
├── lesson08_geneticAlgorithm.py
├── lesson09_pymoo.py
├── lesson10_parallelization.py
└── tests/
    ├── test_platform.py          # runner + sentinel regression tests
    ├── test_lesson00_key.py      # answer key for lesson 00
    ├── test_lesson01_key.py      # answer key for lesson 01
    ├── test_lesson02_key.py      # answer key for lesson 02
    ├── test_lesson03_key.py      # answer key for lesson 03
    ├── test_lesson04_key.py      # answer key for lesson 04
    ├── test_lesson05_key.py      # answer key for lesson 05
    ├── test_lesson06_key.py      # answer key for lesson 06
    ├── test_lesson07_key.py      # answer key for lesson 07
    ├── test_lesson08_key.py      # answer key for lesson 08
    ├── test_lesson09_key.py      # answer key for lesson 09
    └── test_lesson10_key.py      # answer key for lesson 10
```

---

## Runner Commands

- `python optiKoans.py` — global progress table, then re-runs first failing lesson (exits 1 if any koans unsolved, 0 if all complete)
- `python optiKoans.py lesson00_finding_good_answers.py` — single file verbose run

**Regression suite:**
- `pytest tests/` — runs 124 regression tests (answer keys + platform tests); all should pass on a clean checkout
- Do NOT run bare `pytest` (no args) — it will try to collect lesson files too

---

## optiKoans.py Runner Internals

- Uses `pytest.main()` directly (no subprocess) — replaced subprocess in a refactoring session
- `_count(filepath)` uses a `_Counter` pytest plugin class with `pytest_runtest_logreport` hook to tally pass/fail silently (`-p no:terminal`)
- `_run_single()` and `_run_all()` call `pytest.main([filepath, "-v", "--tb=short", ...])` for interactive output
- `sys.exit()` called with pytest's `ExitCode` (int subclass), so exit codes propagate correctly
- Windows UTF-8 fix: `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` at module top — keep it

---

## FILL_ME_IN Sentinel (conftest.py)

```python
class _FillMeIn:
    def __repr__(self): return "FILL_ME_IN"
    def __eq__(self, other): raise AssertionError("\n\n  Fill in the blank!\n  Replace FILL_ME_IN with your answer and try again.\n")
    def __ne__(self, other): return True   # prevents default __ne__ from raising
    def __hash__(self): return id(self)
FILL_ME_IN = _FillMeIn()
```

- `__eq__` raises `AssertionError` → pytest shows as FAILED (not ERROR)
- `__ne__` returns True → `assert FILL_ME_IN != x` passes silently
- Students import: `from conftest import FILL_ME_IN`

---

## Koan Design Conventions

- **Fill-in koans:** `assert computed == FILL_ME_IN` — student fills in the expected value
- **Boolean fill-ins:** `assert (expr) == FILL_ME_IN` — student fills in `True` or `False`
- **Implementation koans:** stub has `pass` body; test calls the function and checks output
- Koan numbering: `test_01_`, `test_02_`, ... so pytest runs them in order
- Lesson files use `from conftest import FILL_ME_IN` (not a fixture — a module-level import)
- **American English spelling:** minimize, maximize, optimize, penalize, recognize (not -ise)
- **Seed convention:** top-level GA functions take a `seed` parameter; operator helpers (`mutate`, `tournament_select`, `crossover`) do NOT — the caller manages random state
- **Side-effect trap:** never write `assert result == min(calls, key=f)` when `f` appends to `calls` — use `min(list(calls), key=f)` to iterate over a snapshot

---

## Lesson Progression

Planned arc: brute force → stochastic search → guided stochastic (GA) → gradient-based

- `lesson00` — objective functions, minimization, argmin, implement `find_minimum`
- `lesson01` — feasibility, inequality/equality constraints, violations, implement `penalty`
- `lesson02` — exhaustive search, `itertools.product`, curse of dimensionality, implement `brute_force_minimize(f, x1_min, x1_max, x2_min, x2_max)`
- `lesson03` — random sampling, seeds, budget vs quality trade-off, implement `monte_carlo_minimize(f, x1_min, x1_max, x2_min, x2_max, n_samples, seed)`
- `lesson04` — binary encoding; 8-item knapsack as running example; bit strings, weight/value from `zip`, feasibility, penalized objective; implement `knapsack_score(bits, weights, values, capacity, penalty_weight=1000)`
- `lesson05` — GA Part 1: single-point crossover; why crossover recombines good partial solutions; slice syntax; boundary cases; implement `crossover(parent1, parent2, point) → (child1, child2)`
- `lesson06` — GA Part 2: bit-flip mutation; why mutation maintains diversity; `flip_bit(bit)` helper (asserts 0 or 1); mutation rate trade-off; implement `mutate(bits, mutation_rate)` — no seed, caller manages state
- `lesson07` — GA Part 3: tournament selection; binary tournament; `tournament_select_matchup(population, scores)` returns the winner of one 2-way draw; `tournament_select(population, scores, n)` builds a mating pool of n winners; mean-score test confirms selection pressure
- `lesson08` — GA Part 4: the complete GA; students re-implement all components from scratch (initialize population, objective, penalty, tournament matchup, crossover with internal random point, mutation); final `run_ga` uses 10% elitism + two-round shuffle-and-pair selection; finds optimal `[1,1,1,0,1,1,0,0]` for seed=0 with pop_size=50, n_generations=50
- `lesson09` — Using a library: pymoo solves the Rastrigin function (continuous, 5 variables, bounds [−5.12, 5.12]); three-step API: subclass `ElementwiseProblem` → choose `GA` algorithm → call `minimize()`; koans: understand the function, define the Problem class, call `_evaluate` directly, read `res.X`/`res.F`, implement `solve_rastrigin`
- `lesson10` — Parallel objective evaluation via `Problem` (not `ElementwiseProblem`); `Problem._evaluate(self, X, out)` receives the full population matrix `X` of shape `(pop_size, n_var)` and must fill `out["F"]` of shape `(pop_size, n_obj)`; `ThreadPool.map(rastrigin, X)` dispatches all row evaluations concurrently; koans: trace the shape contract of `_evaluate`, compare serial vs parallel map output, implement `ParallelRastriginProblem(Problem)`, implement `solve_rastrigin_parallel`

**Central knapsack fixture (lessons 04–08):**
```python
weights  = [2, 5, 3, 7, 1, 4, 6, 3]
values   = [4, 7, 5, 9, 2, 6, 8, 4]
capacity = 15
# Optimal: [1,1,1,0,1,1,0,0] → weight=15, value=24, score=−24
```

---

## Regression Test Structure

`tests/test_platform.py` covers:
- FILL_ME_IN sentinel: raises AssertionError on `==`, returns True on `!=`, correct repr
- `_count()`: all-pass, all-fail, mixed, empty file
- `_bar()`: empty, full, half, zero-total, valid chars only
- Runner exit codes: single file unsolved → 1, missing file → 1, global unsolved → non-zero

`tests/test_lesson##_key.py` — each mirrors the koan logic with correct answers substituted. Does NOT import the lesson file (independent of student progress).

**When adding a new lesson:**
1. Create `lesson##_name.py` with koans
2. Create `tests/test_lesson##_key.py` with reference implementation and answer assertions
3. Update README.md lesson table and project structure tree
4. Update AGENTS.md

---

## Known Issues / Gotchas

1. **Nested pytest sessions:** `_count()` calls `pytest.main()` from within a running pytest session (when `test_platform.py` tests call `_count()` directly). Works reliably with `-p no:terminal` — do NOT add `--tb=no` or `-q` alongside it, as those flags are registered by the terminal plugin and become unrecognised when terminal is disabled.

2. **`pytest_collecterror` is not a valid hook** in pytest 9.x — using it in a plugin class causes `PluginValidationError`. Removed from `_Counter`. Collection errors result in `(0, 0)` from `_count()`.

3. **Progress table uses ASCII chars** (`#`, `.`, `<-- you are here`) not Unicode box-drawing characters — intentional, needed for Windows CP1252 consoles.
