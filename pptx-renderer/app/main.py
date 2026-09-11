from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

APP_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = Path(os.getenv("DATA_ROOT", "/data"))
UPLOAD_ROOT = DATA_ROOT / "uploads"
OUTPUT_ROOT = DATA_ROOT / "output"
CACHE_ROOT = DATA_ROOT / "cache"
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
ONLYOFFICE_URL = os.getenv("ONLYOFFICE_URL", "").rstrip("/")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "100"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

for directory in (UPLOAD_ROOT, OUTPUT_ROOT, CACHE_ROOT):
    directory.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Handgesture Controller PPTX Renderer", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_document_path(document_id: str) -> Path:
    if not document_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in document_id):
        raise HTTPException(status_code=400, detail="Invalid document id")
    path = UPLOAD_ROOT / f"{document_id}.pptx"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Presentation not found")
    return path


def inspect_package(path: Path) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Invalid PPTX package") from exc

    if "[Content_Types].xml" not in names or "ppt/presentation.xml" not in names:
        raise HTTPException(status_code=400, detail="File is not a valid PowerPoint presentation")

    def count(prefix: str) -> int:
        return sum(1 for name in names if name.startswith(prefix))

    return {
        "package_entries": len(names),
        "slides": count("ppt/slides/slide") ,
        "layouts": count("ppt/slideLayouts/slideLayout"),
        "masters": count("ppt/slideMasters/slideMaster"),
        "themes": count("ppt/theme/"),
        "images": count("ppt/media/"),
        "charts": count("ppt/charts/"),
        "diagrams": count("ppt/diagrams/") + count("ppt/diagramData/"),
        "embeddings": count("ppt/embeddings/"),
        "notes": count("ppt/notesSlides/"),
        "comments": count("ppt/comments/"),
        "has_videos": any(name.lower().endswith((".mp4", ".wmv", ".mov", ".avi", ".m4v")) for name in names),
        "has_audio": any(name.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".wma")) for name in names),
        "has_embedded_fonts": any("font" in name.lower() and name.startswith("ppt/") for name in names),
        "has_vba": any(name.lower().endswith("vbaProject.bin".lower()) for name in names),
    }


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <html><head><title>PPTX Renderer</title></head>
    <body style='font-family:system-ui;padding:40px'>
      <h1>Handgesture Controller PPTX Renderer</h1>
      <p>Free Hugging Face backend is running.</p>
      <p><a href='/health'>Health</a> · <a href='/docs'>API docs</a></p>
    </body></html>
    """


@app.get("/health")
def health() -> dict[str, Any]:
    libreoffice = shutil.which("libreoffice") or shutil.which("soffice")
    return {
        "status": "ok",
        "libreoffice": bool(libreoffice),
        "onlyoffice_configured": bool(ONLYOFFICE_URL),
        "max_upload_mb": MAX_UPLOAD_MB,
    }


@app.post("/api/pptx/upload")
async def upload_pptx(file: UploadFile = File(...)) -> dict[str, Any]:
    filename = Path(file.filename or "presentation.pptx").name
    if not filename.lower().endswith(".pptx"):
        raise HTTPException(status_code=415, detail="Only .pptx files are supported")

    document_id = uuid.uuid4().hex
    destination = UPLOAD_ROOT / f"{document_id}.pptx"
    total = 0

    try:
        with destination.open("wb") as output:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail=f"File exceeds {MAX_UPLOAD_MB} MB limit")
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    info = inspect_package(destination)
    base = PUBLIC_BASE_URL or ""
    return {
        "id": document_id,
        "filename": filename,
        "size": total,
        "url": f"{base}/api/pptx/{document_id}",
        "info_url": f"{base}/api/pptx/{document_id}/info",
        "config_url": f"{base}/api/pptx/{document_id}/config",
        "info": info,
    }


@app.get("/api/pptx/{document_id}")
def serve_pptx(document_id: str) -> FileResponse:
    path = safe_document_path(document_id)
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=path.name,
        headers={"Cache-Control": "private, max-age=3600"},
    )


@app.get("/api/pptx/{document_id}/info")
def pptx_info(document_id: str) -> dict[str, Any]:
    path = safe_document_path(document_id)
    return {"id": document_id, "filename": path.name, **inspect_package(path)}


@app.get("/api/pptx/{document_id}/config")
def onlyoffice_config(document_id: str) -> JSONResponse:
    path = safe_document_path(document_id)
    if not ONLYOFFICE_URL:
        raise HTTPException(status_code=503, detail="ONLYOFFICE_URL is not configured")
    if not PUBLIC_BASE_URL:
        raise HTTPException(status_code=503, detail="PUBLIC_BASE_URL is required for ONLYOFFICE")

    stat = path.stat()
    key = f"{document_id}-{stat.st_size}-{int(stat.st_mtime)}"[:120]
    config = {
        "documentType": "slide",
        "type": "embedded",
        "document": {
            "title": path.name,
            "fileType": "pptx",
            "key": key,
            "url": f"{PUBLIC_BASE_URL}/api/pptx/{document_id}",
            "permissions": {
                "edit": False,
                "download": True,
                "print": False,
                "comment": False,
                "review": False,
            },
        },
        "editorConfig": {
            "mode": "view",
            "lang": "en-US",
            "customization": {
                "compactHeader": True,
                "hideRightMenu": True,
                "hideRulers": True,
                "help": False,
                "toolbar": False,
            },
        },
    }
    return JSONResponse({"document_server_url": ONLYOFFICE_URL, "config": config})


def run_libreoffice(input_path: Path, output_dir: Path) -> None:
    binary = shutil.which("libreoffice") or shutil.which("soffice")
    if not binary:
        raise HTTPException(status_code=503, detail="LibreOffice is not installed")
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="lo-profile-"))
    try:
        command = [
            binary,
            "--headless",
            "--nologo",
            "--nodefault",
            "--nolockcheck",
            "--norestore",
            f"-env:UserInstallation=file://{profile}",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(input_path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr[-2000:] or "LibreOffice render failed")
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=504, detail="Presentation rendering timed out") from exc
    finally:
        shutil.rmtree(profile, ignore_errors=True)


@app.post("/api/pptx/{document_id}/render/pdf")
def render_pdf(document_id: str) -> FileResponse:
    path = safe_document_path(document_id)
    target_dir = OUTPUT_ROOT / document_id / "pdf"
    target_dir.mkdir(parents=True, exist_ok=True)
    output = target_dir / f"{document_id}.pdf"
    if not output.exists():
        run_libreoffice(path, target_dir)
        generated = target_dir / f"{path.stem}.pdf"
        if generated != output and generated.exists():
            generated.replace(output)
    if not output.exists():
        raise HTTPException(status_code=500, detail="PDF was not produced")
    return FileResponse(output, media_type="application/pdf", filename=f"{path.stem}.pdf")


@app.delete("/api/pptx/{document_id}")
def delete_pptx(document_id: str) -> dict[str, Any]:
    path = safe_document_path(document_id)
    path.unlink(missing_ok=True)
    shutil.rmtree(OUTPUT_ROOT / document_id, ignore_errors=True)
    return {"deleted": True, "id": document_id}
