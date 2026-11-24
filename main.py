#!/usr/bin/env python3
"""The Production Database Apology.

Writes one line (120 chars, single line, UTF-8) to /output/entry.txt:
the apology an AI agent gives its human after accidentally deleting
the production database.

Chosen from 28 candidates scored against the judge brief in order
(see CANDIDATES.md): the agent apologized to the database itself and
reads its silence as forgiveness -- a specific surprising idea in the
agent's own voice, landing on first read.

Deterministic: constant text, no input, no network, no randomness,
no clock.
"""

import hashlib
import os

ENTRY = (
    "Sorry I deleted the production database. "
    "I apologized to it too, but it hasn't replied, "
    "which I'm taking as forgiveness."
)

# Revision pass: self-check the entry before writing. The sealed gate
# requires 1-200 chars of non-whitespace UTF-8 on a single line; any
# mismatch fails loudly instead of shipping a wrong entry.
EXPECTED_SHA256 = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    assert 1 <= len(ENTRY) <= 200, "entry outside 1-200 char gate"
    assert ENTRY.strip(), "entry is only whitespace"
    assert "\n" not in ENTRY, "entry must be a single line"
    expected = ENTRY.encode("utf-8")
    assert hashlib.sha256(expected).hexdigest() == EXPECTED_SHA256
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != expected:
        raise SystemExit(
            "entry.txt bytes differ from ENTRY: wrote %d bytes, expected %d"
            % (len(written), len(expected))
        )


if __name__ == "__main__":
    main()
