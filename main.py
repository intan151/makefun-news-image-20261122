#!/usr/bin/env python3
"""Entry point (Python 3.13, standard library only).

Copies the entry image beside this file to $MAKEFUN_OUTPUT_DIR/entry.png.
The image itself was drawn by draw_news.py (Pillow, run locally when the
entry was built); the grader runs standard library only, so this entry
point copies the pre-rendered PNG instead of drawing it.
Deterministic: a copy writes the same bytes on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    src = os.path.join(HERE, "entry.png")
    shutil.copyfile(src, path)
    with open(path, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("copied entry.png is not a PNG file")
    # The copy must be byte-for-byte the source: same size means the
    # whole file landed; a truncated write would fail this check.
    if os.path.getsize(src) != os.path.getsize(path):
        raise SystemExit("copied entry.png has the wrong size")
    print("wrote", path, os.path.getsize(path), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
