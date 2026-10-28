# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The Flake8 issues were easiest: adding blank lines and wrapping long lines is mechanical and does not change behaviour. Missing docstrings and renaming `printQueue` were also quick. The hardest was replacing `pickle` with JSON (Bandit B301). JSON only allows string keys, so the integer order ids came back as `"1"`, `"2"` after a restore and had to be converted back. Removing the `global` statements was also harder, because I had to change how `orders`, `menu` and the next order id are managed without breaking the program.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Not strictly, but some warnings depend on context. Bandit B403 flags `import pickle` on its own even though importing it is harmless; only loading untrusted data is risky. In this program the backup file could be edited by anyone with disk access, so the warning was worth acting on. Pylint's W0603 (global statement) is a design warning, not a bug, and would be acceptable in a very small script. The tools also missed the most serious bugs: invalid statuses being stored, unknown dishes silently costing 99, and empty orders being accepted. Those were only found by running the program and reading its output.

**3. How would you integrate static analysis tools into your software development workflow?**

- Run Flake8 and Pylint in the editor so problems show up while typing.
- Add a pre-commit hook that runs Flake8, Pylint and Bandit and blocks commits that fail.
- Run all three in CI (for example GitHub Actions) on every push and pull request, and fail the build if the Pylint score drops below a threshold such as 9.5 or if Bandit reports Medium or High issues.
- Keep shared config files (`.pylintrc`, `.flake8`) in the repo so everyone uses the same rules.

**4. What tangible improvements did you observe in the code quality, readability, and potential robustness after applying the fixes?**

- **Security:** no more pickle deserialization, so a tampered backup file cannot run code.
- **Robustness:** errors are no longer swallowed. Invalid statuses, unknown order ids, unknown dishes and empty orders are reported instead of silently producing wrong data, so revenue and the queue are now correct.
- **Correctness:** the shared mutable default list is gone, and files are always closed, even on errors.
- **Readability:** docstrings, snake_case names, f-strings and PEP 8 formatting make the code easier to read. The Pylint score went from 6.27 to 10.00, and Bandit and Flake8 report no issues.
