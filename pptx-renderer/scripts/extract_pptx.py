from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


def extract(source: Path, destination: Path) -> None:
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
