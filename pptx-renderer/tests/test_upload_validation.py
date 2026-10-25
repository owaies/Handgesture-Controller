from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

from fastapi import HTTPException, UploadFile

from app import main


class UploadValidationTests(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_pptx_is_removed_after_package_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            upload_root = Path(directory)
            upload = UploadFile(
                filename="broken.pptx",
                file=BytesIO(b"this is not a zip archive"),
            )

            with patch.object(main, "UPLOAD_ROOT", upload_root):
                with self.assertRaises(HTTPException) as raised:
                    await main.upload_pptx(upload)

            self.assertEqual(raised.exception.status_code, 400)
            self.assertEqual(list(upload_root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
