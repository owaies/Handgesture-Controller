from __future__ import annotations

import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from fastapi import HTTPException

RENDERER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RENDERER_ROOT))

from scripts.extract_pptx import extract


class StandaloneExtractionTests(unittest.TestCase):
    def _archive(self, path: Path, extra_entries: dict[str, bytes] | None = None) -> None:
        entries = {
            "[Content_Types].xml": b"types",
            "ppt/presentation.xml": b"presentation",
            **(extra_entries or {}),
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in entries.items():
                archive.writestr(name, data)

    def test_extracts_a_valid_minimal_presentation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "valid.pptx"
            destination = root / "extracted"
            self._archive(source)

            extract(source, destination)

            self.assertEqual((destination / "ppt" / "presentation.xml").read_bytes(), b"presentation")

    def test_rejects_unsafe_archive_before_creating_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "unsafe.pptx"
            destination = root / "extracted"
            self._archive(source, {"../outside.txt": b"outside"})

            with self.assertRaises(HTTPException) as raised:
                extract(source, destination)

            self.assertEqual(raised.exception.status_code, 400)
            self.assertFalse(destination.exists())
            self.assertFalse((root / "outside.txt").exists())

    def test_rejects_symbolic_link_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "symlink.pptx"
            info = zipfile.ZipInfo("ppt/link")
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("[Content_Types].xml", b"types")
                archive.writestr("ppt/presentation.xml", b"presentation")
                archive.writestr(info, b"../outside.txt")

            with self.assertRaises(HTTPException) as raised:
                extract(source, Path(directory) / "extracted")

            self.assertEqual(raised.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
