# PowerPoint Package Safety

The renderer accepts PowerPoint uploads up to the configured `MAX_UPLOAD_MB` limit. A compressed file size alone does not bound the work required to inspect a ZIP-based Office package: a small archive can contain many entries or data that expands substantially.

The renderer enforces a maximum of 10,000 ZIP entries and 512 MiB of declared uncompressed package data before inspecting package contents. Packages above either bound receive HTTP 413. These limits complement the compressed upload limit; they do not make arbitrary archive extraction safe. Do not extract archive paths without separate path and resource controls.

## Manual regression checks

- A valid small PPTX passes package inspection.
- A non-ZIP file returns HTTP 400.
- A ZIP missing `[Content_Types].xml` or `ppt/presentation.xml` returns HTTP 400.
- An archive exceeding 10,000 entries or 512 MiB of declared expanded data is rejected with HTTP 413 before rendering.
- A LibreOffice failure returns a generic rendering error to the client while diagnostic details remain in server logs.
- The original uploaded presentation remains unchanged after inspection.
