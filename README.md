# Most Active Cookie

A command-line tool that finds the most active cookie in a cookie log for a given day.

## Description

The program reads a cookie log in CSV format and prints the cookie that appears most often on a given date (UTC). If several cookies share the highest count, all of them are printed, one per line, in the order they first appear in the log.


### How it works

The program is split into three functions in `most_active_cookie.py`:

- `read_cookie_log` reads the file, validates each line and returns `(cookie, timestamp)` with timestamps in UTC
- `find_most_active_cookies` counts the cookies seen on the given day and returns those with the highest count
- `main` handles the command-line arguments, error messages and output

## Requirements

- Python 3.9 or newer
- No third-party packages are needed to run the program
- For development: pytest and ruff (installed with the steps below), and `make` (optional, macOS/Linux)

## Installation

No installation is needed to run the program. Clone the repository and run it from the project folder:

```
git clone <repository-url>
cd most-active-cookie
```

To set up the development tools (macOS/Linux):

```
python3 -m venv .venv
source .venv/bin/activate
make install
```

On Windows:

```
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```
./most_active_cookie <log_file> -d <YYYY-MM-DD>
```

| Argument | Description |
|---|---|
| `log_file` | Path to the cookie log CSV file |
| `-d`, `--date` | The day to check, in UTC (format `YYYY-MM-DD`) |

Example:

```
$ ./most_active_cookie cookie_log.csv -d 2018-12-09
AtY0laUfhglK3lC7
```

Example with a tie:

```
$ ./most_active_cookie cookie_log.csv -d 2018-12-08
SAZuXPGUrfbcn5UA
4sMM2LxV07bPJzwf
fbcn5UAVanZf6UtG
```

On Windows, run the launcher with Python: `python most_active_cookie cookie_log.csv -d 2018-12-09`

### Log file format

```
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
```

Each line holds a cookie and an ISO 8601 timestamp with a timezone offset. The header row is optional.

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success. This includes the case where no cookies match the date: nothing is printed to standard output, and a message is shown on stderr |
| 1 | The log file is missing, or a line in it is malformed. The error message names the line |
| 2 | Invalid or missing command-line arguments |

## Development

Run the tests:

```
make test
```

Check code style and formatting:

```
make lint
```

Without `make`, run `pytest`, `ruff check .` and `ruff format --check .` directly.

The tests cover the examples from the task, ties, days with no cookies, timezone conversion, malformed lines and missing files.

### Project structure

```
most-active-cookie/
├── most_active_cookie            # launcher, so the program runs as ./most_active_cookie
├── most_active_cookie.py         # reading, counting and command-line interface
├── tests/
│   └── test_most_active_cookie.py
├── cookie_log.csv                # sample log from the task
├── pyproject.toml                # project metadata and development dependencies
├── Makefile                      # install, lint and test shortcuts
└── README.md
```

## Design decisions and assumptions

- **UTC conversion:** the `-d` date is in UTC, so every timestamp is converted to UTC before its date is compared.
- **Ties:** printed in the order the cookies first appear in the log, matching the example in the task.
- **Header:** skipped if the first line is `cookie,timestamp`. Files without a header are also accepted.
- **Misinformed lines:** a line with the wrong number of columns, an empty cookie, an invalid timestamp or a timestamp without a timezone stops the program with an error naming the line.
- **Blank lines:** skipped.
- **No matches or empty log:** not treated as an error. Nothing is printed to standard output, a message is shown on stderr, and the exit code is 0.
- **Memory:** the whole file is read into memory, as the task allows.
- **Sorted input:** the log is sorted by timestamp, so reading could stop once past the given date. A single full pass was chosen instead, because it is simpler and fast enough for this task.

## Author

Ravpreet Gill

## Project status

Complete.