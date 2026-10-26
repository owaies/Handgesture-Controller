from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

from fastapi import HTTPException, UploadFile

# Allow unittest discovery from either the renderer directory or repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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

class UploadLimitConfigurationTests(unittest.TestCase):
    def test_positive_integer_upload_limit_is_accepted(self) -> None:
        with patch.dict("os.environ", {"TEST_UPLOAD_LIMIT": "25"}):
            self.assertEqual(main._positive_int_env("TEST_UPLOAD_LIMIT", 100), 25)

    def test_invalid_upload_limits_fail_with_a_clear_error(self) -> None:
        for value in ("0", "-1", "abc", "1.5"):
            with self.subTest(value=value), patch.dict("os.environ", {"TEST_UPLOAD_LIMIT": value}):
                with self.assertRaisesRegex(RuntimeError, "TEST_UPLOAD_LIMIT must be a positive integer"):
                    main._positive_int_env("TEST_UPLOAD_LIMIT", 100)


if __name__ == "__main__":
    unittest.main()
