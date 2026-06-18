#!/usr/bin/env python3
"""Convert internal .html links to clean root-relative URLs (/page, /blog/post)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HREF_RE = re.compile(r'href="([^"]+)"')
SKIP_PREFIX = re.compile(r"^(https?:|//|mailto:|tel:|#)")


def to_clean_path(url: str) -> str | None:
    if SKIP_PREFIX.match(url):
        if ".html" not in url:
            return None
        # Clean absolute revzio URLs if present
        m = re.match(r"^(https?://[^/]+)(/.*)$", url)
        if not m:
            return None
        url = m.group(2)

    hash_part = ""
    if "#" in url:
        url, frag = url.split("#", 1)
        hash_part = f"#{frag}"

    url = url.strip()
    while url.startswith("./"):
        url = url[2:]
    while url.startswith("../"):
        url = url[3:]

    if url in ("", "index.html"):
        return f"/{hash_part}" if hash_part else "/"

    if not url.endswith(".html"):
        return None

    slug = url[:-5]
    return f"/{slug}{hash_part}"


def clean_hrefs(text: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        original = match.group(1)
        cleaned = to_clean_path(original)
        if cleaned is None or cleaned == original:
            return match.group(0)
        count += 1
        return f'href="{cleaned}"'

    return HREF_RE.sub(repl, text), count


def clean_js_string_urls(text: str) -> tuple[str, int]:
    """Update quoted *.html paths used as navigation targets in JS."""
    count = 0
    pattern = re.compile(r"(['\"])([\w./-]+\.html(?:#[\w-]+)?)\1")

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        quote, url = match.group(1), match.group(2)
        cleaned = to_clean_path(url)
        if cleaned is None:
            return match.group(0)
        count += 1
        return f"{quote}{cleaned}{quote}"

    return pattern.sub(repl, text), count


def main() -> None:
    total = 0
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".html", ".js", ".py"}:
            continue
        if ".git" in path.parts or path.name == "clean-urls.py":
            continue

        original = path.read_text(encoding="utf-8")
        updated, n = clean_hrefs(original)
        if path.suffix == ".js":
            updated, n2 = clean_js_string_urls(updated)
            n += n2

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"{path.relative_to(ROOT)}: {n} links")
            total += n

    print(f"Done. Updated {total} links.")


if __name__ == "__main__":
    main()
