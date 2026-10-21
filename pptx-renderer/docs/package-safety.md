# PowerPoint Package Safety

The renderer accepts PowerPoint uploads up to the configured `MAX_UPLOAD_MB` limit. A compressed file size alone does not bound the work required to inspect a ZIP-based Office package: a small archive can contain many entries or data that expands substantially.

Before enabling additional conversion or extraction features, validate both the number of package entries and the sum of declared uncompressed entry sizes. Return a controlled client error when either limit is exceeded, and do not extract arbitrary archive paths. Keep limits configurable only when the deployment has matching memory and disk capacity.

## Manual regression checks

- A valid small PPTX passes package inspection.
- A non-ZIP file returns HTTP 400.
- A ZIP missing `[Content_Types].xml` or `ppt/presentation.xml` returns HTTP 400.
- An archive exceeding the entry-count or expanded-size limit is rejected before rendering.
- The original uploaded presentation remains unchanged after inspection.
