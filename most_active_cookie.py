import argparse
import csv
import sys
from collections import Counter
from datetime import date, datetime, timezone


def read_cookie_log(file_path):
    """Read log file and return cookies and time, with times in UTC"""
    entries = []
    with open(file_path) as log_file:
        reader = csv.reader(log_file)
        for row in reader:
            # Edge case: header row - skip it (only if it really is the header)
            if reader.line_num == 1 and row == ["cookie", "timestamp"]:
                continue

            # Edge case: blank line - skip it
            if not row:
                continue

            # Edge case: line doesn't have exactly two parts
            if len(row) != 2:
                raise ValueError(f"line {reader.line_num} should be cookie,timestamp")

            cookie, timestamp = row

            # Edge case: cookie is empty
            if not cookie:
                raise ValueError(f"line {reader.line_num} has no cookie")

            # Exception case: timestamp can't be read
            try:
                seen_at = datetime.fromisoformat(timestamp)
            except ValueError:
                raise ValueError(f"line {reader.line_num} has an invalid timestamp")

            # Edge case: timestamp has no timezone
            if seen_at.tzinfo is None:
                raise ValueError(f"line {reader.line_num} has no timezone")

            entries.append((cookie, seen_at.astimezone(timezone.utc)))
    return entries


def find_most_active_cookies(entries, day):
    """Return list of most active cookies on the given day."""
    counts = Counter()
    for cookie, seen_at in entries:
        if seen_at.date() == day:
            counts[cookie] += 1

    # Edge case: no cookies on that day - return an empty list
    if not counts:
        return []

    highest = max(counts.values())
    most_active = []
    for cookie, count in counts.items():
        if count == highest:
            most_active.append(cookie)
    return most_active


def main():
    parser = argparse.ArgumentParser(description="Find the most active cookie.")
    parser.add_argument("log_file")
    parser.add_argument("-d", "--date", required=True, type=date.fromisoformat)
    args = parser.parse_args()

    # Exception cases: file is missing, or a line in it is bad
    try:
        entries = read_cookie_log(args.log_file)
    except FileNotFoundError:
        sys.exit(f"Error: file not found: {args.log_file}")
    except ValueError as error:
        sys.exit(f"Error: {error}")

    # Edge case: log file has no entries
    if not entries:
        print("No entries in the log file.", file=sys.stderr)
        return

    most_active = find_most_active_cookies(entries, args.date)

    # Edge case: no cookies on that day - tell the user
    if not most_active:
        print(f"No cookies found for {args.date}.", file=sys.stderr)
        return

    for cookie in most_active:
        print(cookie)


if __name__ == "__main__":
    main()
