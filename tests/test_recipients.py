"""Tests for recipient list parsing (pasted text or an uploaded CSV/TXT)."""

import pytest

from payroll_dashboard.backend.recipients import parse_recipients


def test_parses_one_address_per_line():
    assert parse_recipients("a@x.com\nb@x.com") == ["a@x.com", "b@x.com"]


def test_parses_a_comma_separated_list():
    assert parse_recipients("a@x.com, b@x.com,c@x.com") == ["a@x.com", "b@x.com", "c@x.com"]


def test_strips_surrounding_whitespace_and_blank_lines():
    assert parse_recipients("  a@x.com  \n\n\n  b@x.com\n") == ["a@x.com", "b@x.com"]


def test_handles_windows_line_endings():
    assert parse_recipients("a@x.com\r\nb@x.com") == ["a@x.com", "b@x.com"]


def test_skips_a_csv_header_row():
    csv = "email,name\na@x.com,Alice\nb@x.com,Bob"
    assert parse_recipients(csv) == ["a@x.com", "b@x.com"]


def test_reads_the_email_column_of_a_multi_column_csv():
    csv = "name,email\nAlice,a@x.com\nBob,b@x.com"
    assert parse_recipients(csv) == ["a@x.com", "b@x.com"]


def test_deduplicates_while_preserving_first_seen_order():
    assert parse_recipients("b@x.com\na@x.com\nb@x.com") == ["b@x.com", "a@x.com"]


def test_deduplicates_case_insensitively():
    """Mail addresses are case-insensitive in practice; keep the first spelling."""
    assert parse_recipients("A@x.com\na@X.com") == ["A@x.com"]


@pytest.mark.parametrize("junk", ["not-an-email", "@x.com", "a@", "", "   "])
def test_drops_entries_that_are_not_addresses(junk):
    assert parse_recipients(f"good@x.com\n{junk}") == ["good@x.com"]


def test_extracts_an_address_that_follows_a_bare_name():
    """Same rule as the quoted display-name form: take the address, drop the name.
    A bare 'Alice b@x.com' is indistinguishable from a display name, so it extracts."""
    assert parse_recipients("Alice b@x.com") == ["b@x.com"]


def test_returns_empty_list_for_empty_input():
    assert parse_recipients("") == []


def test_ignores_quotes_and_display_names():
    assert parse_recipients('"Alice" <a@x.com>\nb@x.com') == ["a@x.com", "b@x.com"]


def test_tolerates_semicolon_separators():
    """Outlook exports separate addresses with semicolons."""
    assert parse_recipients("a@x.com; b@x.com") == ["a@x.com", "b@x.com"]
