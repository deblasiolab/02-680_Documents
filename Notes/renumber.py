#!/usr/bin/env python3
"""Renumber a file with `#_Something.ext` naming by shifting its leading number via `git mv`.

Usage:
    python3 renumber.py <filename> <delta>

Example:
    python3 renumber.py 03_Tuples.pdf 1
    -> git mv 03_Tuples.pdf 04_Tuples.pdf
"""

import re
import subprocess
import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <filename> <delta>", file=sys.stderr)
        sys.exit(1)

    filename, delta_str = sys.argv[1], sys.argv[2]

    try:
        delta = int(delta_str)
    except ValueError:
        print(f"Error: delta must be an integer, got {delta_str!r}", file=sys.stderr)
        sys.exit(1)

    match = re.match(r"^(\d+)(_.*)$", filename)
    if not match:
        print(f"Error: filename {filename!r} does not match '#_Something.ext' pattern", file=sys.stderr)
        sys.exit(1)

    number_str, rest = match.groups()
    new_number = int(number_str) + delta
    if new_number < 0:
        print(f"Error: resulting number {new_number} is negative", file=sys.stderr)
        sys.exit(1)

    new_number_str = str(new_number).zfill(len(number_str))
    new_filename = f"{new_number_str}{rest}"

    subprocess.run(["git", "mv", filename, new_filename], check=True)


if __name__ == "__main__":
    main()
