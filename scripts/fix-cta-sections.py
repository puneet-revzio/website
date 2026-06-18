#!/usr/bin/env python3
"""Remove duplicate inline CTA CSS and upgrade blog CTAs to full-width bands."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INLINE_CTA_RE = re.compile(
    r"\n  /\* CTA \*/\n  \.cta \{[^}]+\}\n  \.cta h2 \{[^}]+\}\n"
    r"(?:  \.cta h2 em \{[^}]+\}\n)?"
    r"  \.cta p \{[^}]+\}\n"
    r"  \.cta \.btn-primary \{[^}]+\}\n"
    r"  \.cta \.btn-primary:hover \{[^}]+\}\n"
    r"(?:  \.cta \.btn-secondary[^\n]*\{[^}]+\}\n)*"
    r"(?:  \.cta \.btn-secondary::after \{[^}]+\}\n)?"
    r"(?:  \.cta \.btn-secondary:hover[^\n]*\{[^}]+\}\n)*"
)

INLINE_CTA_SECTION_RE = re.compile(
    r"  \.cta-section \{ background: var\(--ink\);[^}]+\}\n"
    r"  \.cta-section h2 \{[^}]+\}\n"
    r"  \.cta-section h2 em \{[^}]+\}\n"
    r"  \.cta-section p \{[^}]+\}\n"
    r"  \.cta-section \.btn-primary \{[^}]+\}\n"
    r"  \.cta-section \.btn-primary:hover \{[^}]+\}\n"
    r"  \.cta-section \.btn-secondary \{[^}]+\}\n"
    r"  \.cta-section \.btn-secondary:hover \{[^}]+\}\n"
    r"  \.cta-section \.hero-ctas \{[^}]+\}\n"
)

BLOG_CTA_BLOCK_RE = re.compile(
    r"    \.cta \{\n      margin-top: 42px;[\s\S]*?    \.cta a:hover \{ background: #9adfc0; \}\n",
    re.MULTILINE,
)

BLOG_CTA_DIV_RE = re.compile(
    r"      <div class=\"cta\">\n"
    r"        <h2 style=\"margin-top: 0;\">([^<]+)</h2>\n"
    r"        <p>([^<]+)</p>\n"
    r"        <a href=\"([^\"]+)\">([^<]+)</a>\n"
    r"      </div>\n"
    r"    </article>\n"
    r"  </div>\n"
    r"</section>",
    re.MULTILINE,
)


def strip_inline_cta_css(text: str) -> str:
    text = INLINE_CTA_RE.sub("\n", text)
    text = INLINE_CTA_SECTION_RE.sub("", text)
    return text


def upgrade_blog_cta(text: str) -> str:
    text = BLOG_CTA_BLOCK_RE.sub("", text)

    def repl(match: re.Match[str]) -> str:
        title, body, href, label = match.groups()
        title = title.replace("Ready to see Orion in action?", "See your <em>next close</em> in revzio.")
        if "<em>" not in title and "revzio" in title.lower():
            pass
        elif "<em>" not in title:
            # Highlight last meaningful phrase if short title
            title = f"Ready for your <em>next close</em>?"
        return (
            f"    </article>\n"
            f"  </div>\n"
            f"</section>\n\n"
            f'<section class="cta-section" data-nav-theme="dark">\n'
            f"  <div class=\"container reveal\">\n"
            f"    <h2>{title}</h2>\n"
            f"    <p>{body}</p>\n"
            f'    <div class="hero-ctas">\n'
            f'      <a href="{href}" class="btn btn-primary">{label.replace(" →", "")}</a>\n'
            f"    </div>\n"
            f"  </div>\n"
            f"</section>"
        )

    return BLOG_CTA_DIV_RE.sub(repl, text)


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = strip_inline_cta_css(original)
        if "/blog/" in str(path):
            updated = upgrade_blog_cta(updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
