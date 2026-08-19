"""Parse a recipient list from pasted text or an uploaded CSV/TXT file."""

import re

# Deliberately permissive: this guards against obvious junk (headers, names,
# stray columns), not against every RFC 5322 edge case.
_EMAIL = re.compile(r"[^\s@,;<>\"]+@[^\s@,;<>\".]+\.[^\s@,;<>\"]+")


def parse_recipients(raw: str) -> list[str]:
    """Extract unique email addresses from *raw*, preserving first-seen order.

    Accepts one-per-line text, comma or semicolon separated lists, and CSV with
    or without a header. Display names ("Alice" <a@x.com>) are discarded.
    """
    seen: set[str] = set()
    addresses: list[str] = []

    for match in _EMAIL.findall(raw or ""):
        key = match.lower()
        if key not in seen:
            seen.add(key)
            addresses.append(match)

    return addresses
