#!/usr/bin/env python3
"""Verified excerpt from the current thoracic atlas ZIP rebuild script."""

from __future__ import annotations

import base64
from typing import Any
from urllib.parse import unquote, urlparse


ATLAS_ROOT = "thorax-2020-11-15"
ATLAS_PREFIX = (
    "https://www.openanatomy.org/atlases/macbioidi/mauritania/"
    f"{ATLAS_ROOT}/"
)
REQUIRED_FILES = {
    "atlasStructure.json",
    "Data/CT-256.nrrd",
    "Data/Segmentation-flattened.seg.nrrd",
}
HarData = dict[str, Any]


def atlas_relative_path(url: str) -> str | None:
    """Return the atlas-relative path for a matching atlas asset URL."""
    if not url.startswith(ATLAS_PREFIX):
        return None

    relative = unquote(urlparse(url).path.split(f"/{ATLAS_ROOT}/", 1)[1])
    if relative.startswith("viewer/") or not relative:
        return None

    return relative


def decode_content(content: HarData, relative_path: str) -> bytes:
    """Decode a HAR response body into raw bytes."""
    text = content.get("text")
    if text is None:
        raise SystemExit(f"Missing embedded response body for {relative_path}")

    if content.get("encoding") == "base64":
        try:
            return base64.b64decode(text)
        except Exception as exc:  # pragma: no cover - defensive path
            raise SystemExit(
                f"Failed to base64-decode {relative_path}: {exc}"
            ) from exc

    return text.encode("utf-8")
