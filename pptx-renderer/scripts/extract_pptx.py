from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.package_safety import inspect_package


def extract(source: Path, destination: Path) -> None:
    # Keep the standalone extractor subject to the same archive path and
    # expansion limits as uploads handled by the renderer API.
    inspect_package(source)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as zf:
        zf.extractall(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a PPTX Office package")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    extract(args.source, args.destination)
    print(f"Extracted {args.source} -> {args.destination}")


if __name__ == "__main__":
    main()
