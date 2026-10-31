from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import main


class PackageSafetyTests(unittest.TestCase):
    def _archive(self, directory: str, entries: dict[str, bytes]) -> Path:
        path = Path(directory) / "sample.pptx"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in entries.items():
                archive.writestr(name, data)
        return path

    def test_rejects_packages_with_too_many_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._archive(directory, {"a": b"x", "b": b"y"})
            with patch.object(main, "MAX_PACKAGE_ENTRIES", 1):
                with self.assertRaises(HTTPException) as raised:
                    main.inspect_package(path)
        self.assertEqual(raised.exception.status_code, 413)

    def test_rejects_packages_with_excessive_expanded_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._archive(directory, {"ppt/presentation.xml": b"12345"})
            with patch.object(main, "MAX_PACKAGE_UNCOMPRESSED_BYTES", 4):
                with self.assertRaises(HTTPException) as raised:
                    main.inspect_package(path)
        self.assertEqual(raised.exception.status_code, 413)

    def test_renderer_errors_do_not_expose_process_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(main.shutil, "which", return_value="/usr/bin/libreoffice"),
                patch.object(
                    main.subprocess,
                    "run",
                    return_value=SimpleNamespace(returncode=1, stderr="/srv/private/renderer/profile"),
                ),
            ):
                with self.assertRaises(HTTPException) as raised:
                    main.run_libreoffice(Path(directory) / "input.pptx", Path(directory) / "output")
        self.assertEqual(raised.exception.status_code, 500)
        self.assertEqual(raised.exception.detail, "Presentation rendering failed")
        self.assertNotIn("/srv/private", raised.exception.detail)


if __name__ == "__main__":
    unittest.main()
