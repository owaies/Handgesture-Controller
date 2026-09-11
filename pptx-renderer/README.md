# PPTX Renderer for Hugging Face Spaces

Free/open-source backend for the Handgesture Controller project.

## Architecture

```text
Netlify frontend
      |
      v
Hugging Face Space (Docker)
      |
      +--> PPTX validation / storage
      |
      +--> LibreOffice (fallback rendering, thumbnails, PDF preview)
      |
      +--> optional ONLYOFFICE Document Server
      |
      v
Original PPTX + extracted Office assets
```

The original PPTX is kept intact. The service can inspect/extract Office package contents and use LibreOffice for broad compatibility. If `ONLYOFFICE_URL` is configured, the API also exposes an ONLYOFFICE-compatible document configuration for higher-fidelity interactive presentation viewing.

## Hugging Face deployment

1. Create a new **Docker Space** on Hugging Face.
2. Import/copy the contents of this `pptx-renderer` directory into the Space root.
3. Set Space port to `7860` if Hugging Face asks for it.
4. Optional environment variables:

```text
PUBLIC_BASE_URL=https://YOUR-SPACE.hf.space
ONLYOFFICE_URL=https://YOUR-ONLYOFFICE-SERVER
MAX_UPLOAD_MB=100
```

`PUBLIC_BASE_URL` is important when an external ONLYOFFICE server needs to download the uploaded document.

## API

- `GET /` health landing page
- `GET /health`
- `POST /api/pptx/upload` upload a `.pptx`
- `GET /api/pptx/{id}` download/serve the original PPTX
- `GET /api/pptx/{id}/info` inspect slides and package assets
- `GET /api/pptx/{id}/config` return an ONLYOFFICE editor configuration when configured
- `POST /api/pptx/{id}/render/pdf` render a PDF with LibreOffice
- `POST /api/pptx/{id}/render/slides` render slide preview images with LibreOffice
- `DELETE /api/pptx/{id}` delete an uploaded document

## Important fidelity note

LibreOffice is an open-source compatibility renderer, not Microsoft's PowerPoint rendering engine. It cannot guarantee pixel-perfect reproduction of every PowerPoint feature. ONLYOFFICE improves compatibility for many PPTX files, but it is also not a mathematical guarantee of 100% Microsoft PowerPoint fidelity.

For a $0 deployment, this project deliberately keeps the original PPTX and all its package contents instead of flattening the presentation into PDF only.
