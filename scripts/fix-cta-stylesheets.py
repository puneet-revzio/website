#!/usr/bin/env python3
"""Ensure cta-band.css loads on every page and add gold em highlights to CTA headings."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CTA_LINK_ROOT = '  <link rel="stylesheet" href="css/cta-band.css">\n'
CTA_LINK_BLOG = '  <link rel="stylesheet" href="../css/cta-band.css">\n'

# Headline text replacements: add <em> around key phrase (skip if already has em)
HEADLINE_UPDATES = [
    (
        "<h2>Ready to automate your order-to-cash cycle?</h2>",
        "<h2>Ready to automate your <em>order-to-cash</em> cycle?</h2>",
    ),
    (
        "<h2>Ready to automate your procure-to-pay cycle?</h2>",
        "<h2>Ready to automate your <em>procure-to-pay</em> cycle?</h2>",
    ),
    (
        "<h2>Talk to someone who's actually closed books.</h2>",
        "<h2>Talk to someone who's actually <em>closed books</em>.</h2>",
    ),
    (
        "<h2>Security questions? Talk to our team.</h2>",
        "<h2>Security questions? <em>Talk to our team.</em></h2>",
    ),
    (
        "<h2>Download the Security Overview.</h2>",
        "<h2>Download the <em>Security Overview</em>.</h2>",
    ),
    (
        "<h2>Don't see your tool? Let's talk.</h2>",
        "<h2>Don't see your tool? <em>Let's talk.</em></h2>",
    ),
    (
        "<h2>Ready to write your own story?</h2>",
        "<h2>Ready to write <em>your own story</em>?</h2>",
    ),
    (
        "<h2>Ready to close your SaaS books faster?</h2>",
        "<h2>Ready to close your <em>SaaS books</em> faster?</h2>",
    ),
    (
        "<h2>Built for your stage. Ready for the next one.</h2>",
        "<h2>Built for your stage. <em>Ready for the next one.</em></h2>",
    ),
    (
        "<h2>Replace your legacy close platform — in weeks, not months.</h2>",
        "<h2>Replace your legacy close platform — <em>in weeks, not months.</em></h2>",
    ),
    (
        "<h2>About revzio</h2>",
        "<h2>About <em>revzio</em></h2>",
    ),
    (
        "<h2>Don't see your role? We want to hear from you.</h2>",
        "<h2>Don't see your role? <em>We want to hear from you.</em></h2>",
    ),
    (
        "<h2>Ready to validate every dollar of revenue?</h2>",
        "<h2>Ready to validate every <em>dollar of revenue</em>?</h2>",
    ),
    (
        "<h2>Ready to run a faster, cleaner close?</h2>",
        "<h2>Ready to run a <em>faster, cleaner close</em>?</h2>",
    ),
    (
        "<h2>Ready to automate your accruals?</h2>",
        "<h2>Ready to automate your <em>accruals</em>?</h2>",
    ),
    (
        "<h2>Ready to accelerate your receivables?</h2>",
        "<h2>Ready to accelerate your <em>receivables</em>?</h2>",
    ),
    (
        "<h2>Ready to automate your accounts payable?</h2>",
        "<h2>Ready to automate your <em>accounts payable</em>?</h2>",
    ),
]


def inject_cta_stylesheet(text: str, path: Path) -> str:
    if "cta-band.css" in text:
        return text
    blog = "/blog/" in str(path)
    link = CTA_LINK_BLOG if blog else CTA_LINK_ROOT
    marker = "../css/dark-global.css" if blog else "css/dark-global.css"
    needle = f'<link rel="stylesheet" href="{marker}">'
    if needle in text:
        return text.replace(needle, needle + "\n" + link.rstrip(), 1)
    return text


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = inject_cta_stylesheet(original, path)
        for old, new in HEADLINE_UPDATES:
            if old in updated:
                updated = updated.replace(old, new)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
