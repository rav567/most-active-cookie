from datetime import date
from pathlib import Path

import pytest

from most_active_cookie import find_most_active_cookies, read_cookie_log

SAMPLE_LOG = Path(__file__).parent.parent / "cookie_log.csv"


def test_example_9_december():
    entries = read_cookie_log(SAMPLE_LOG)
    assert find_most_active_cookies(entries, date(2018, 12, 9)) == ["AtY0laUfhglK3lC7"]


def test_example_8_december():
    entries = read_cookie_log(SAMPLE_LOG)
    expected = ["SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"]
    assert find_most_active_cookies(entries, date(2018, 12, 8)) == expected


def test_no_cookies_on_that_day():
    entries = read_cookie_log(SAMPLE_LOG)
    assert find_most_active_cookies(entries, date(2018, 12, 1)) == []


def test_timestamp_is_converted_to_utc(tmp_path):
    log_file = tmp_path / "log.csv"
    log_file.write_text("cookie,timestamp\ncookie_a,2018-12-09T01:00:00+02:00\n")
    entries = read_cookie_log(log_file)
    assert find_most_active_cookies(entries, date(2018, 12, 8)) == ["cookie_a"]


def test_bad_timestamp_raises_error(tmp_path):
    log_file = tmp_path / "log.csv"
    log_file.write_text("cookie,timestamp\ncookie_a,not-a-date\n")
    with pytest.raises(ValueError):
        read_cookie_log(log_file)


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        read_cookie_log("missing.csv")
