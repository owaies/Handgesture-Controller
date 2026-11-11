from __future__ import annotations

import stat
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from fastapi import HTTPException

MAX_PACKAGE_ENTRIES = 10_000
MAX_PACKAGE_UNCOMPRESSED_BYTES = 512 * 1024 * 1024


def inspect_package(
    path: Path,
    *,
    max_entries: int = MAX_PACKAGE_ENTRIES,
    max_uncompressed_bytes: int = MAX_PACKAGE_UNCOMPRESSED_BYTES,
) -> dict[str, Any]:
    """Validate a PPTX ZIP package before any member is extracted or rendered."""
    try:
        with zipfile.ZipFile(path) as zf:
            entries = zf.infolist()
            if len(entries) > max_entries:
                raise HTTPException(status_code=413, detail="PowerPoint package contains too many entries")
            expanded_size = sum(entry.file_size for entry in entries)
            if expanded_size > max_uncompressed_bytes:
                raise HTTPException(status_code=413, detail="PowerPoint package expands beyond the allowed size")
            names = []
            seen_names: set[str] = set()
            for entry in entries:
                name = entry.filename
                normalized = name.replace("\\", "/")
                archive_path = PurePosixPath(normalized)
                is_windows_absolute = len(normalized) > 1 and normalized[1] == ":"
                is_symlink = stat.S_ISLNK(entry.external_attr >> 16)
                if (
                    not name
                    or name in seen_names
                    or "\\" in name
                    or archive_path.is_absolute()
                    or is_windows_absolute
                    or is_symlink
                    or any(part in {".", ".."} for part in archive_path.parts)
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="PowerPoint package contains an unsafe or duplicate entry path",
                    )
                seen_names.add(name)
                names.append(name)
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Invalid PPTX package") from exc

    if "[Content_Types].xml" not in names or "ppt/presentation.xml" not in names:
        raise HTTPException(status_code=400, detail="File is not a valid PowerPoint presentation")

    def count(prefix: str) -> int:
        return sum(1 for name in names if name.startswith(prefix))

    return {
        "package_entries": len(names),
        "slides": count("ppt/slides/slide"),
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
