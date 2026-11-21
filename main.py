#!/usr/bin/env python3
"""Entry point for the news-image-20261120 make.fun submission.

The entry image is the committed asset ``news.png`` beside this file,
rendered beforehand by ``make_image.py``.  This program verifies the
asset (PNG signature, 1024x1024 dimensions, 1 MiB size cap) and copies
it byte-for-byte to ``entry.png`` in the output directory
(``$MAKEFUN_OUTPUT_DIR`` when set, else ``/output``), so every graded
run produces byte-identical output.  Standard library only.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB cap for entry.png
EXPECTED_SIZE = (1024, 1024)  # required pixel dimensions
ASSET_NAME = "news.png"
ENTRY_NAME = "entry.png"


def asset_path() -> Path:
    """Return the path of the committed image asset beside this file."""
    return Path(__file__).resolve().parent / ASSET_NAME


def output_dir() -> Path:
    """Resolve the output directory from the environment or default."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def verify_asset(path: Path) -> int:
    """Check that the asset exists, is a PNG of the required
    dimensions and fits the size cap; return its size in bytes.
    Raises ValueError otherwise.  Width and height come from the
    IHDR chunk, which follows the 8-byte PNG signature.
    """
    if not path.is_file():
        raise ValueError(f"asset not found: {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(f"asset is {size} bytes, over the {MAX_BYTES} cap")
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise ValueError(f"asset is not a PNG file: {path}")
    dimensions = struct.unpack(">II", header[16:24])
    if dimensions != EXPECTED_SIZE:
        raise ValueError(f"asset is {dimensions[0]}x{dimensions[1]}, "
                         f"expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}")
    return size


def main() -> int:
    asset = asset_path()
    try:
        size = verify_asset(asset)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    destination_dir = output_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / ENTRY_NAME
    shutil.copyfile(asset, destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(f"wrote {destination} ({size} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
