# Privacy notes

The presentation experience is designed to run in the browser without a traditional application backend for gesture control.

## Camera data
Camera access is required for gesture recognition. Keep permission prompts explicit and do not request camera access until the user starts the feature.

## Local documents
Uploaded presentation files should be treated as user-controlled local content. Avoid adding automatic persistence unless it is intentionally designed and documented.

## Release checks
Verify camera permission behavior, fullscreen behavior, and document handling on a clean browser profile.
