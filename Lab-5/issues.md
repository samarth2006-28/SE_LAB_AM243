# Issues Found in `delivery_system.py`

Line numbers refer to the original file (`reports/before/`).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Unsafe deserialization | Bandit B301 | Security | Medium | 49 | `pickle.load()` on a file can execute arbitrary code if the file is tampered with | Back up and restore orders as JSON; convert JSON string keys back to `int` ids on restore |
| 2 | Pickle import | Bandit B403 | Security | Low | 2 | Importing `pickle` flags the module as a deserialization risk | Removed the import along with the pickle calls |
| 3 | Try / except / pass | Bandit B110, Pylint W0702, Flake8 E722 | Security / Bug | Low | 23-25 | Bare `except: pass` hides every error, so an unknown order id (42) silently does nothing | Replaced with explicit checks: unknown status and unknown order id are reported and return `False` |
| 4 | Invalid status accepted | Logic (not flagged by tools) | Bug | High | 21-23 | `"teleported"` was stored as an order status; `VALID_STATUSES` was never used | Validate `status` against `VALID_STATUSES` before updating |
| 5 | Unknown dishes cost 99 | Logic (not flagged by tools) | Bug | High | 14-15 | `menu.get(i, 99)` silently charged 99 for "sushi", which is not on the menu | Reject the order with `ValueError` listing the unknown dishes |
| 6 | Empty order accepted | Logic (not flagged by tools) | Bug | Medium | 60, 64 | An order with no customer and no items was created and marked delivered | Reject orders with no customer name or no items |
| 7 | Mutable default argument | Pylint W0102 | Bug | Medium | 11 | `order_history=[]` is created once and shared across every call | Default to `None` and create a new list inside the function |
| 8 | Global statements | Pylint W0603 | Design | Medium | 12, 28, 48 | `global next_id/menu/orders` makes state hard to follow and test | Mutate `orders`/`menu` in place (`clear()`/`update()`); derive the next id from `max(orders) + 1` |
| 9 | Files not closed safely | Pylint R1732, W1514 | Bug | Medium | 30, 43, 49 | `open()` without `with` leaks the handle on error; no encoding given | Use `with open(..., encoding="utf-8")` everywhere |
| 10 | Broad exception | Pylint W0718 | Bug | Medium | 32 | `except Exception` would also hide programming errors | Catch only `OSError` and `json.JSONDecodeError` |
| 11 | Naming / formatting | Pylint C0103, C0209 | Style | Low | 7, 51-52 | `printQueue` is not snake_case; `%` formatting instead of f-string | Renamed to `print_queue`; switched to f-strings |
| 12 | Missing docstrings | Pylint C0114, C0116 | Style | Low | 1, all functions | No module or function documentation | Added a module docstring and one per function |
| 13 | Code runs on import | Best practice | Design | Low | 70 | `main()` ran whenever the module was imported | Wrapped in `if __name__ == "__main__":` |
| 14 | Blank lines | Flake8 E302, E305 | Style | Low | 11-70 | One blank line between top-level functions instead of two | Two blank lines around every top-level function |
| 15 | Lines too long | Flake8 E501 | Style | Low | 16, 54 | Lines longer than 79 characters | Wrapped the order dict and long expressions over several lines |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.27/10 (22 messages) | **10.00/10** (0 messages) |
| Bandit | 3 issues (1 Medium, 2 Low) | **0 issues** |
| Flake8 | 12 issues | **0 issues** (empty report) |
