#!/usr/bin/env python3
"""Verified excerpt from the current thoracic atlas HAR capture script."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VIEWER_URL = (
    "https://www.openanatomy.org/atlases/macbioidi/mauritania/"
    "thorax-2020-11-15/viewer/"
)
ATLAS_PREFIX = (
    "https://www.openanatomy.org/atlases/macbioidi/mauritania/"
    "thorax-2020-11-15/"
)
HarData = dict[str, Any]


def load_har(path: Path) -> HarData:
    """Load a captured HAR file from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def contains_atlas_requests(har: HarData) -> bool:
    """Return True when the HAR contains successful atlas asset requests."""
    for entry in har.get("log", {}).get("entries", []):
        request = entry.get("request", {})
        response = entry.get("response", {})
        if (
            request.get("method") == "GET"
            and int(response.get("status", 0) or 0) == 200
            and str(request.get("url", "")).startswith(ATLAS_PREFIX)
        ):
            return True
    return False


def capture_raw_har(raw_har_path: Path, timeout_ms: int) -> None:
    """Capture a raw HAR file using Playwright."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            record_har_path=str(raw_har_path),
            record_har_mode="full",
            ignore_https_errors=False,
        )
        page = context.new_page()
        page.goto(
            VIEWER_URL,
            wait_until="networkidle",
            timeout=timeout_ms,
        )
        page.wait_for_timeout(15000)
        context.close()
        browser.close()
