#!/usr/bin/env python3
"""Replace agent-suite# hashes and upgrade related boxes to Numeric-style card grids."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HASH_MAP = {
    "/agent-suite#reconciliation": "/agent-suite-reconciliation",
    "/agent-suite#journal-entry": "/agent-suite-journal-entry",
    "/agent-suite#accounts-payable": "/agent-suite-ap",
    "/agent-suite#accounts-receivable": "/agent-suite-ar",
    "/agent-suite#accruals": "/agent-suite-accruals",
    "/agent-suite#revenue-validation": "/agent-suite-revenue-validation",
    "/agent-suite#close-management": "/agent-suite-close-management",
}

# href -> card metadata
CATALOG: dict[str, dict] = {
    "/blog/3-day-close-playbook": {
        "title": "From 10-day close to 3 days: the CFO playbook",
        "excerpt": "How continuous recon, journal prep, and clear ownership shrink month-end without adding headcount.",
        "tags": ["Article", "Close"],
        "media": "navy",
        "label": "3-day close",
    },
    "/blog/cutting-close-three-days": {
        "title": "Cutting close by three days at scale",
        "excerpt": "Continuous reconciliation, prepared journals, and exception workflows that keep auditors satisfied.",
        "tags": ["Article", "Close"],
        "media": "mint",
        "label": "Faster close",
    },
    "/blog/continuous-close-readiness": {
        "title": "Why periodic reconciliation is costing you days every month",
        "excerpt": "Stop starting from zero at month-end — continuous close readiness for finance teams.",
        "tags": ["Article", "Recon"],
        "media": "sage",
        "label": "Continuous close",
    },
    "/blog/exception-explainability": {
        "title": "Introducing exception explainability",
        "excerpt": "Clearer break reasons so accountants resolve recon items instead of reverse-engineering matches.",
        "tags": ["Article", "Product"],
        "media": "gold",
        "label": "Explainability",
    },
    "/blog/reconciliation-agent-deep-dive": {
        "title": "How Orion's Reconciliation Agent closed 95% of items without human touch",
        "excerpt": "Line-level matching, when humans step in, and what audit-ready evidence looks like.",
        "tags": ["Article", "Agents"],
        "media": "navy",
        "label": "Recon agent",
    },
    "/blog/manual-recon-cost": {
        "title": "The hidden cost of manual reconciliation",
        "excerpt": "Time, errors, and delayed close — and how automation changes the economics.",
        "tags": ["Article", "CFO"],
        "media": "slate",
        "label": "Manual recon",
    },
    "/blog/human-in-the-loop-finance": {
        "title": "What human-in-the-loop actually means for finance teams",
        "excerpt": "Approvals, materiality thresholds, and keeping controllers in control of the close.",
        "tags": ["Article", "AI"],
        "media": "mint",
        "label": "HITL",
    },
    "/blog/ai-agency-in-finance": {
        "title": "AI in accounting: agency over automation",
        "excerpt": "Why finance AI needs agency — Orion prepares work while humans keep judgment.",
        "tags": ["Article", "AI"],
        "media": "gold",
        "label": "AI agency",
    },
    "/blog/3-week-onboarding": {
        "title": "3 weeks to go-live: how revzio onboards finance teams",
        "excerpt": "Connect sources, configure Orion agents, and move from spreadsheet close to continuous prep.",
        "tags": ["Article", "Implementation"],
        "media": "sage",
        "label": "Onboarding",
    },
    "/blog/3-way-match-ai": {
        "title": "3-way match explained: how AI eliminates invoice exceptions",
        "excerpt": "PO, receipt, and invoice alignment that reduces AP noise before it hits the close.",
        "tags": ["Article", "AP"],
        "media": "navy",
        "label": "3-way match",
    },
    "/blog/revenue-integrity-playbook": {
        "title": "The controller's guide to revenue integrity",
        "excerpt": "Validate billing, recognition, and recon signals so revenue stays trustworthy through close.",
        "tags": ["Article", "Revenue"],
        "media": "mint",
        "label": "Revenue",
    },
    "/blog/revenue-recognition-scale": {
        "title": "Revenue recognition at scale: why spreadsheets break at Series B",
        "excerpt": "How scalable processes and AI validation keep SaaS finance close-ready as you grow.",
        "tags": ["Article", "ASC 606"],
        "media": "gold",
        "label": "ASC 606",
    },
    "/blog/soc2-and-your-close-stack": {
        "title": "SOC 2 and your close stack",
        "excerpt": "Controls, evidence, and choosing close tooling that supports audit readiness year-round.",
        "tags": ["Article", "Security"],
        "media": "slate",
        "label": "SOC 2",
    },
    "/guides/3-day-close-guide": {
        "title": "Running a 3-day close with Orion",
        "excerpt": "Week-by-week implementation for teams moving recon and JE prep into every day.",
        "tags": ["Guide", "Close"],
        "media": "navy",
        "label": "3-day guide",
    },
    "/guides/setup-reconciliation-agent": {
        "title": "Setting up your first Reconciliation Agent",
        "excerpt": "Connect feeds, configure match rules, and run your first automated reconciliation.",
        "tags": ["Guide", "Recon"],
        "media": "mint",
        "label": "Setup recon",
    },
    "/guides/automate-journal-entries": {
        "title": "Automating journal entries end-to-end",
        "excerpt": "Chart mapping, accrual logic, ERP posting, and reviewer gates that stay audit-ready.",
        "tags": ["Guide", "Journals"],
        "media": "sage",
        "label": "JE guide",
    },
    "/guides/netsuite-integration": {
        "title": "Connecting revzio to NetSuite",
        "excerpt": "OAuth, field mapping, entity scope, and validating your first data sync.",
        "tags": ["Guide", "Integration"],
        "media": "slate",
        "label": "NetSuite",
    },
    "/guides/asc606-revenue-agent": {
        "title": "ASC 606 with the Revenue Validation Agent",
        "excerpt": "Recognition rules, contract modifications, and audit-ready revenue output.",
        "tags": ["Guide", "ASC 606"],
        "media": "gold",
        "label": "ASC 606",
    },
    "/guides/audit-trail-soc2": {
        "title": "Audit trail setup and SOC 2 readiness",
        "excerpt": "RBAC, immutable logs, and reviewer sign-off workflows for your next audit.",
        "tags": ["Guide", "Security"],
        "media": "navy",
        "label": "Audit trail",
    },
    "/close-workflow": {
        "title": "Month-end close workflow",
        "excerpt": "Checklists, ownership, approvals, and AI prep so controllers finish close earlier.",
        "tags": ["Product", "Close"],
        "media": "mint",
        "label": "Close workflow",
    },
    "/reconciliation": {
        "title": "Account reconciliation software",
        "excerpt": "Match bank, subledger, and billing continuously so exceptions surface early.",
        "tags": ["Product", "Recon"],
        "media": "navy",
        "label": "Reconciliation",
    },
    "/continuous-close": {
        "title": "Continuous close software",
        "excerpt": "Daily reconciliations, prepared journals, and live close status before month-end.",
        "tags": ["Product", "Close"],
        "media": "sage",
        "label": "Continuous",
    },
    "/agent-suite-reconciliation": {
        "title": "Reconciliation Agent",
        "excerpt": "Line-level matching across bank, billing, and ERP — with explainable exceptions.",
        "tags": ["Agent", "Recon"],
        "media": "mint",
        "label": "Recon agent",
    },
    "/agent-suite-journal-entry": {
        "title": "Journal Entry Agent",
        "excerpt": "Validated journals from source data — mappings, gates, and ERP posting.",
        "tags": ["Agent", "Journals"],
        "media": "navy",
        "label": "JE agent",
    },
    "/agent-suite-ap": {
        "title": "Accounts Payable Agent",
        "excerpt": "Invoice extraction, 3-way match, and approval routing for AP teams.",
        "tags": ["Agent", "AP"],
        "media": "gold",
        "label": "AP agent",
    },
    "/agent-suite-ar": {
        "title": "Accounts Receivable Agent",
        "excerpt": "Cash application and collections priority that keep receivables continuous.",
        "tags": ["Agent", "AR"],
        "media": "sage",
        "label": "AR agent",
    },
    "/agent-suite-close-management": {
        "title": "Close Management Agent",
        "excerpt": "Checklists, owners, dependencies, and sign-offs in one audit-ready workflow.",
        "tags": ["Agent", "Close"],
        "media": "slate",
        "label": "Close agent",
    },
    "/agent-suite-revenue-validation": {
        "title": "Revenue Validation Agent",
        "excerpt": "ASC 606 checks that flag billing-to-ERP gaps before they hit audit.",
        "tags": ["Agent", "Revenue"],
        "media": "gold",
        "label": "Revenue agent",
    },
    "/procure-to-pay": {
        "title": "AP automation software",
        "excerpt": "Invoice matching, exceptions, and controls that cut manual AP work.",
        "tags": ["Product", "AP"],
        "media": "navy",
        "label": "Procure-to-pay",
    },
    "/order-to-cash": {
        "title": "AR automation software",
        "excerpt": "Match payments, clear remittances, and reduce DSO with AI agents.",
        "tags": ["Product", "AR"],
        "media": "mint",
        "label": "Order-to-cash",
    },
    "/record-to-report": {
        "title": "Journal entry automation",
        "excerpt": "Journals, accruals, reconciliations, and close workflows in one path.",
        "tags": ["Product", "R2R"],
        "media": "sage",
        "label": "Record-to-report",
    },
    "/security": {
        "title": "Security & data protection",
        "excerpt": "Enterprise controls, access management, and practices for audit-ready teams.",
        "tags": ["Product", "Security"],
        "media": "slate",
        "label": "Security",
    },
    "/trust-center": {
        "title": "Trust Center & compliance",
        "excerpt": "Security and assurance resources for IT and procurement before you buy.",
        "tags": ["Product", "Trust"],
        "media": "navy",
        "label": "Trust center",
    },
    "/industry-saas": {
        "title": "Financial close for SaaS",
        "excerpt": "Automate reconciliation, revenue validation, and month-end for subscription finance.",
        "tags": ["Solution", "SaaS"],
        "media": "mint",
        "label": "SaaS close",
    },
    "/how-it-works": {
        "title": "How Orion AI close works",
        "excerpt": "Agents prepare continuously so your team reviews exceptions and closes with confidence.",
        "tags": ["Product", "Platform"],
        "media": "gold",
        "label": "How it works",
    },
    "/recon-automation": {
        "title": "Automated reconciliation software",
        "excerpt": "Match at scale, explain breaks, and focus humans on exceptions that need judgment.",
        "tags": ["Product", "Recon"],
        "media": "sage",
        "label": "Recon automation",
    },
}

# page path (relative to site root, no leading slash, no .html) -> 3 related hrefs
RELATED: dict[str, list[str]] = {
    "blog/3-day-close-playbook": [
        "/guides/3-day-close-guide",
        "/close-workflow",
        "/blog/cutting-close-three-days",
    ],
    "blog/3-way-match-ai": [
        "/agent-suite-ap",
        "/procure-to-pay",
        "/blog/human-in-the-loop-finance",
    ],
    "blog/3-week-onboarding": [
        "/guides/setup-reconciliation-agent",
        "/guides/netsuite-integration",
        "/how-it-works",
    ],
    "blog/ai-agency-in-finance": [
        "/agent-suite-reconciliation",
        "/blog/human-in-the-loop-finance",
        "/how-it-works",
    ],
    "blog/continuous-close-readiness": [
        "/continuous-close",
        "/reconciliation",
        "/blog/3-day-close-playbook",
    ],
    "blog/cutting-close-three-days": [
        "/guides/3-day-close-guide",
        "/blog/3-day-close-playbook",
        "/agent-suite-close-management",
    ],
    "blog/exception-explainability": [
        "/blog/manual-recon-cost",
        "/blog/continuous-close-readiness",
        "/blog/cutting-close-three-days",
    ],
    "blog/human-in-the-loop-finance": [
        "/blog/ai-agency-in-finance",
        "/security",
        "/guides/audit-trail-soc2",
    ],
    "blog/manual-recon-cost": [
        "/reconciliation",
        "/agent-suite-reconciliation",
        "/blog/reconciliation-agent-deep-dive",
    ],
    "blog/reconciliation-agent-deep-dive": [
        "/guides/setup-reconciliation-agent",
        "/agent-suite-reconciliation",
        "/blog/exception-explainability",
    ],
    "blog/revenue-integrity-playbook": [
        "/guides/asc606-revenue-agent",
        "/agent-suite-revenue-validation",
        "/industry-saas",
    ],
    "blog/revenue-recognition-scale": [
        "/blog/revenue-integrity-playbook",
        "/guides/asc606-revenue-agent",
        "/industry-saas",
    ],
    "blog/soc2-and-your-close-stack": [
        "/guides/audit-trail-soc2",
        "/trust-center",
        "/security",
    ],
    "guides/setup-reconciliation-agent": [
        "/agent-suite-reconciliation",
        "/blog/reconciliation-agent-deep-dive",
        "/blog/manual-recon-cost",
    ],
    "guides/automate-journal-entries": [
        "/agent-suite-journal-entry",
        "/record-to-report",
        "/blog/3-day-close-playbook",
    ],
    "guides/3-day-close-guide": [
        "/continuous-close",
        "/blog/3-day-close-playbook",
        "/blog/cutting-close-three-days",
    ],
    "guides/netsuite-integration": [
        "/agent-suite-reconciliation",
        "/guides/setup-reconciliation-agent",
        "/how-it-works",
    ],
    "guides/asc606-revenue-agent": [
        "/agent-suite-revenue-validation",
        "/blog/revenue-integrity-playbook",
        "/industry-saas",
    ],
    "guides/audit-trail-soc2": [
        "/blog/soc2-and-your-close-stack",
        "/trust-center",
        "/security",
    ],
    "reconciliation": [
        "/agent-suite-reconciliation",
        "/blog/reconciliation-agent-deep-dive",
        "/guides/setup-reconciliation-agent",
    ],
    "close-workflow": [
        "/agent-suite-close-management",
        "/guides/3-day-close-guide",
        "/blog/3-day-close-playbook",
    ],
    "continuous-close": [
        "/blog/continuous-close-readiness",
        "/guides/3-day-close-guide",
        "/reconciliation",
    ],
    "agent-suite-reconciliation": [
        "/guides/setup-reconciliation-agent",
        "/blog/reconciliation-agent-deep-dive",
        "/reconciliation",
    ],
    "agent-suite-journal-entry": [
        "/guides/automate-journal-entries",
        "/record-to-report",
        "/blog/3-day-close-playbook",
    ],
    "agent-suite-ap": [
        "/blog/3-way-match-ai",
        "/procure-to-pay",
        "/agent-suite-reconciliation",
    ],
    "agent-suite-ar": [
        "/order-to-cash",
        "/agent-suite-reconciliation",
        "/blog/continuous-close-readiness",
    ],
    "agent-suite-accruals": [
        "/agent-suite-journal-entry",
        "/record-to-report",
        "/close-workflow",
    ],
    "agent-suite-revenue-validation": [
        "/guides/asc606-revenue-agent",
        "/blog/revenue-integrity-playbook",
        "/industry-saas",
    ],
    "agent-suite-close-management": [
        "/close-workflow",
        "/guides/3-day-close-guide",
        "/blog/3-day-close-playbook",
    ],
}

RELATED_CSS = """
/* Numeric-style RELATED CONTENT grid */
.related-content {
  padding: 72px 0 80px;
  background: var(--bg, #fff);
}
.related-content__heading {
  text-align: center;
  font-family: Inter, system-ui, sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-muted, #6b7280);
  margin: 0 0 36px;
}
.related-content__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
.related-content__card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  min-width: 0;
}
.related-content__card:hover .related-content__title {
  color: var(--accent, #0f6b4e);
}
.related-content__media {
  position: relative;
  aspect-ratio: 16 / 10;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 14px;
  display: flex;
  align-items: flex-end;
  padding: 18px;
  background: var(--hero-bg, #0a1a2f);
}
.related-content__media::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 0%, rgba(127, 207, 170, 0.22), transparent 55%),
    radial-gradient(ellipse at 90% 80%, rgba(90, 150, 210, 0.18), transparent 50%);
  opacity: 0.9;
}
.related-content__media--mint { background: linear-gradient(145deg, #0f6b4e 0%, #0a1a2f 70%); }
.related-content__media--navy { background: linear-gradient(145deg, #0a1a2f 0%, #163a5c 80%); }
.related-content__media--sage { background: linear-gradient(145deg, #2d5a45 0%, #0a1a2f 75%); }
.related-content__media--gold { background: linear-gradient(145deg, #6b5328 0%, #0a1a2f 70%); }
.related-content__media--slate { background: linear-gradient(145deg, #334155 0%, #0a1a2f 75%); }
.related-content__media-label {
  position: relative;
  z-index: 1;
  font-family: Fraunces, Georgia, serif;
  font-size: clamp(18px, 1.6vw, 22px);
  font-weight: 500;
  color: #fafaf7;
  letter-spacing: -0.02em;
  line-height: 1.2;
  max-width: 90%;
}
.related-content__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}
.related-content__tag {
  display: inline-flex;
  align-items: center;
  padding: 5px 11px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 650;
  letter-spacing: 0.02em;
  background: rgba(15, 107, 78, 0.10);
  color: var(--accent, #0f6b4e);
}
.related-content__title {
  font-family: Inter, system-ui, sans-serif;
  font-size: 17px;
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: -0.015em;
  color: var(--ink, #0a0f0c);
  margin: 0 0 8px;
  transition: color 0.2s ease;
}
.related-content__excerpt {
  margin: 0;
  font-size: 14px;
  line-height: 1.55;
  color: var(--ink-muted, #6b7280);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
@media (max-width: 900px) {
  .related-content__grid { grid-template-columns: 1fr; gap: 32px; max-width: 520px; margin: 0 auto; }
}
"""


def fix_hashes() -> int:
    n = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".html", ".js", ".txt", ".md", ".xml"}:
            continue
        if "node_modules" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in HASH_MAP.items():
            text = text.replace(old, new)
        # also bare agent-suite# without leading slash variants already covered
        if text != orig:
            path.write_text(text, encoding="utf-8")
            n += 1
            print("hash-fixed", path.relative_to(ROOT))
    return n


def card_html(href: str) -> str:
    meta = CATALOG[href]
    tags = "".join(f'<span class="related-content__tag">{t}</span>' for t in meta["tags"])
    excerpt = meta["excerpt"]
    if not excerpt.endswith("…") and not excerpt.endswith("."):
        excerpt = excerpt.rstrip(".") + "…"
    elif excerpt.endswith("."):
        excerpt = excerpt[:-1] + "…"
    return f"""      <a class="related-content__card" href="{href}">
        <div class="related-content__media related-content__media--{meta['media']}" aria-hidden="true">
          <span class="related-content__media-label">{meta['label']}</span>
        </div>
        <div class="related-content__tags">{tags}</div>
        <h3 class="related-content__title">{meta['title']}</h3>
        <p class="related-content__excerpt">{excerpt}</p>
      </a>"""


def section_html(hrefs: list[str]) -> str:
    cards = "\n".join(card_html(h) for h in hrefs)
    return f"""
<section class="related-content" aria-labelledby="related-content-heading">
  <div class="container">
    <h2 id="related-content-heading" class="related-content__heading">Related content</h2>
    <div class="related-content__grid">
{cards}
    </div>
  </div>
</section>
"""


RELATED_BOX_RE = re.compile(
    r"\s*<(?:aside|div)\s+class=\"related-box\"[^>]*>[\s\S]*?</(?:aside|div)>\s*",
    re.I,
)

INLINE_RELATED_CSS_RE = re.compile(
    r"<style>\.related-box\{[^<]*\}</style>\s*",
    re.I,
)


def asset_prefix(key: str) -> str:
    return "../" if "/" in key else ""


def upgrade_related_pages() -> int:
    count = 0
    for key, hrefs in RELATED.items():
        file = ROOT / f"{key}.html"
        if not file.exists():
            print("missing", key)
            continue
        html = file.read_text(encoding="utf-8")
        html = INLINE_RELATED_CSS_RE.sub("", html)
        html = RELATED_BOX_RE.sub("\n", html)
        html = re.sub(
            r'\s*<p class="reveal"[^>]*>Related reading:[\s\S]*?</p>\s*',
            "\n",
            html,
            count=1,
        )

        css_href = f"{asset_prefix(key)}css/related-content.css"
        if "css/related-content.css" not in html:
            html = html.replace(
                "</head>",
                f'<link rel="stylesheet" href="{css_href}">\n</head>',
                1,
            )

        section = section_html(hrefs)
        if 'class="related-content"' in html:
            html = re.sub(
                r'\s*<section class="related-content"[\s\S]*?</section>\s*',
                "\n" + section + "\n",
                html,
                count=1,
            )
        else:
            inserted = False
            for marker in (
                '<section class="cta-section"',
                '<section class="cta"',
                "<footer>",
            ):
                if marker in html:
                    html = html.replace(marker, section + "\n" + marker, 1)
                    inserted = True
                    break
            if not inserted:
                html = html.replace("</body>", section + "\n</body>", 1)

        file.write_text(html, encoding="utf-8")
        count += 1
        print("related", key)
    return count


def write_css() -> None:
    (ROOT / "css" / "related-content.css").write_text(RELATED_CSS.strip() + "\n", encoding="utf-8")
    print("wrote css/related-content.css")


def main() -> None:
    write_css()
    h = fix_hashes()
    r = upgrade_related_pages()
    # verify no hashes remain in html
    left = []
    for p in ROOT.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        if "/agent-suite#" in t:
            left.append(str(p.relative_to(ROOT)))
    print(f"done hashes={h} related={r} remaining_hashes={left}")


if __name__ == "__main__":
    main()
