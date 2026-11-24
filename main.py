#!/usr/bin/env python3
"""news-image-20261123 atlas entry for make.fun.

Writes the pre-built entry image to the output directory named by
MAKEFUN_OUTPUT_DIR (falling back to "." only when unset). The image is
a fixed data file shipped in this repository, so the program is fully
deterministic: no timestamps, no randomness, no network.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def png_size(path):
    """Read width and height from a PNG header without any decoder."""
    with open(path, "rb") as fh:
        header = fh.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.digest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Self-check: the copy must be byte-identical to the source and
    # inside the competition's gate limits, or the run fails loudly
    # instead of submitting a broken image.
    if sha256_of(SOURCE) != sha256_of(dest):
        print("copy mismatch: output differs from entry.png", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        sys.exit(1)
    width, height = png_size(dest)
    if width > MAX_DIM or height > MAX_DIM:
        print(f"entry.png is {width}x{height}, over the 1024x1024 limit",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
