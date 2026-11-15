# Lab 5 - Static Code Analysis: Issue Table

File analysed: `maintenance_system.py` (Warehouse Asset Maintenance Registry)
Tools: Pylint 4.1.4, Bandit 1.9.4, Flake8 7.4.1

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Mutable default argument | Bug (Pylint W0102) | 10 | `logs=[]` is shared across calls, so the registration count leaks between calls | Track registrations in a module-level `registration_log` list instead of a default argument |
| Insecure temp file | Security (Bandit B306, Medium) | 40 | `tempfile.mktemp()` is deprecated and vulnerable to a race condition (CWE-377) | Use `tempfile.NamedTemporaryFile` which creates the file atomically |
| Use of `assert` | Security (Bandit B101, Low) | 61 | `assert` is removed when Python runs with `-O`, so the check silently disappears | Replace with an explicit `if not assets:` check and message |
| Bare `except` | Bug (Pylint W0702, Flake8 E722) | 18 | Catches every exception including KeyboardInterrupt and hides real errors | Validate membership first and catch only `ValueError` for date parsing |
| Unused import | Style (Flake8 F401, Pylint W0611) | 2 | `logging` is imported but never used | Remove the import |
| Global statement | Design (Pylint W0603) | 30 | `global SERVICE_INTERVAL_DAYS` mutates module state; also allowed an invalid negative interval | Store the interval in a module-level `config` dict and reject non-positive values |
| File opened without `with`/encoding | Bug (Pylint R1732, W1514) | 34, 41 | Files opened manually may stay open on error and use a platform-dependent encoding | Use `with open(..., encoding="utf-8")` |
| Invalid function name | Style (Pylint C0103) | 46 | `printAlerts` does not follow snake_case | Rename to `print_alerts` |
| Missing docstrings | Convention (Pylint C0114, C0116) | 1, all functions | Module and functions undocumented | Add module and function docstrings |
| Formatting violations | Style (Flake8 E302, E305, E501) | 10-66 | Missing blank lines between functions and a 98-character line | Reformat to PEP 8 (2 blank lines, lines <= 79 chars) |
| Dict iteration by key | Refactor (Pylint C0206) | 23 | Iterating keys and indexing back into the dict | Iterate with `assets.items()` |
| Empty asset id accepted | Logic bug (runtime) | 50 | `register_asset("", ...)` registers an asset with an empty id | Reject empty ids with a message |
| Duplicate asset id overwrites | Logic bug (runtime) | 51 | Registering `FL-01` twice silently overwrote the Forklift record with Crane | Reject duplicate ids with a message |
| Negative interval accepted | Logic bug (runtime) | 55 | `change_interval(-30)` made every asset permanently overdue | Reject non-positive intervals |
| Unvalidated date input | Logic bug (runtime) | 16 | Any string was accepted as a service date, crashing `due_for_inspection` later | Validate with `datetime.strptime` before storing |

## Result

- Pylint: 6.55/10 -> 10.00/10
- Bandit: 2 findings (1 Medium, 1 Low) -> 0 findings
- Flake8: 12 findings -> 0 findings
