# Browser support checks

Before shipping browser-facing changes, verify:

- Camera permission can be granted and revoked.
- PDF rendering loads correctly.
- Fullscreen requests work where supported.
- Pointer and keyboard interaction remain usable.
- Mobile/touch layouts do not depend on hover-only controls.

Also test a fresh browser profile so permissions and cached assets do not hide regressions.
