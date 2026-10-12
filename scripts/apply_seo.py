#!/usr/bin/env python3
"""Apply SEO head tags across the Revzio marketing site. Run from repo root."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.revzio.ai"
OG_IMAGE = f"{SITE}/assets/og-default.png"
LOGO = f"{SITE}/assets/logos/revzio-logo.png"
TODAY = date.today().isoformat()

# path (no leading slash except "") -> SEO config
# description must be 140–160 chars; title "… | Revzio" max 60
PAGES: dict[str, dict] = {
    "": {
        "title": "AI Financial Close Automation Software | Revzio",
        "description": "Revzio helps finance teams close the books faster with AI agents for reconciliation, journal entries, AP, AR, and continuous close — with full audit trails.",
        "type": "website",
        "home": True,
    },
    "agent-suite": {
        "title": "AI Agents for Accounting & Finance | Revzio",
        "description": "Seven purpose-built Orion agents for finance close — reconciliation, journal entry, AP, AR, accruals, revenue validation, and close management.",
        "type": "website",
    },
    "pricing": {
        "title": "Pricing | Revzio",
        "description": "Transparent Revzio pricing for AI financial close automation. Start with one Orion agent or the full suite — book a demo for a quote mapped to your workflows.",
        "type": "website",
        "faq": [
            ("How long does implementation take?", "Most teams go live in under 3 weeks."),
            (
                "Can I start with just one Orion agent?",
                "Yes. Many teams start with the Reconciliation Agent or Journal Entry Agent and add more agents as they see value. There's no minimum agent commitment on Growth plans.",
            ),
            (
                "What happens if my transaction volume grows?",
                "Orion pricing is not based on transaction volume. You won't get a surprise invoice because your Stripe volume doubled.",
            ),
            (
                "Is there a free trial?",
                "We offer a sandboxed demo built on your actual data structure. Most customers find this more useful than a generic free trial. Book a demo to see it.",
            ),
        ],
    },
    "book-a-demo": {
        "title": "Book a Demo | Revzio",
        "description": "Book a 30-minute Revzio demo to see Orion AI agents on your close workflows — reconciliation, journals, AP, AR, and audit-ready continuous close.",
        "type": "website",
    },
    "platform": {
        "title": "Finance Close Platform Overview | Revzio",
        "description": "Explore the Revzio platform for AI-powered financial close — data ingestion, reconciliation, workflows, controls, and reporting in one connected system.",
        "type": "website",
    },
    "how-it-works": {
        "title": "How Orion AI Close Works | Revzio",
        "description": "See how Revzio’s Orion agents prepare reconciliations and journals continuously, so your team reviews exceptions and closes the books with confidence.",
        "type": "website",
    },
    "solutions": {
        "title": "Finance Close Solutions by Role | Revzio",
        "description": "Revzio solutions for CFOs, controllers, and accounting teams — faster close, cleaner reconciliations, and audit-ready workflows across SaaS and enterprise.",
        "type": "website",
    },
    "integrations": {
        "title": "ERP & Ledger Integrations | Revzio",
        "description": "Connect Revzio to your ERP, billing, banks, and data stack. Orion agents sync sources so reconciliation and close stay continuous, not spreadsheet-driven.",
        "type": "website",
    },
    "security": {
        "title": "Security & Data Protection | Revzio",
        "description": "Learn how Revzio protects financial data with enterprise security controls, access management, encryption, and practices designed for audit-ready close teams.",
        "type": "website",
    },
    "trust-center": {
        "title": "Trust Center & Compliance | Revzio",
        "description": "Visit the Revzio Trust Center for security, compliance, and assurance resources your IT and procurement teams need before adopting AI close automation.",
        "type": "website",
    },
    "industry-saas": {
        "title": "Financial Close for SaaS Companies | Revzio",
        "description": "Revzio helps SaaS finance teams automate reconciliation, revenue validation, and month-end close — built for subscription billing complexity and scale.",
        "type": "website",
    },
    "industry-startup": {
        "title": "Close Automation for Startups | Revzio",
        "description": "VC-backed startups use Revzio to close faster with lean teams — AI agents for recon, journals, and close checklists without adding headcount every quarter.",
        "type": "website",
    },
    "industry-enterprise": {
        "title": "Enterprise Financial Close Software | Revzio",
        "description": "Enterprise finance teams use Revzio for multi-entity close, controls, and AI agents that scale reconciliation and reporting without sacrificing auditability.",
        "type": "website",
    },
    "reconciliation": {
        "title": "Account Reconciliation Software | Revzio",
        "description": "Automate account reconciliation with Revzio — match bank, subledger, and billing data continuously so exceptions surface early and month-end close shrinks.",
        "type": "website",
    },
    "recon-automation": {
        "title": "Automated Reconciliation Software | Revzio",
        "description": "Automated reconciliation software from Revzio matches transactions at scale, explains breaks, and keeps finance teams focused on exceptions that need judgment.",
        "type": "website",
    },
    "record-to-report": {
        "title": "Journal Entry Automation | Revzio",
        "description": "Automate record-to-report with Revzio — journal entry generation, accruals, reconciliations, and close workflows that keep your books audit-ready every day.",
        "type": "website",
    },
    "order-to-cash": {
        "title": "AR Automation Software | Revzio",
        "description": "Revzio AR automation helps order-to-cash teams match payments, clear remittances, and reduce DSO with AI agents that keep receivables continuous and clean.",
        "type": "website",
    },
    "procure-to-pay": {
        "title": "AP Automation Software | Revzio",
        "description": "Automate procure-to-pay with Revzio AP agents — invoice matching, exception handling, and controls that cut manual AP work while preserving a clear audit trail.",
        "type": "website",
    },
    "continuous-close": {
        "title": "Continuous Close Software | Revzio",
        "description": "Move from periodic scramble to continuous close with Revzio — daily reconciliations, prepared journals, and live close status before month-end even starts.",
        "type": "website",
    },
    "close-workflow": {
        "title": "Month-End Close Software | Revzio",
        "description": "Run month-end close with Revzio workflows — checklists, ownership, approvals, and AI prep so controllers see status clearly and finish close days earlier.",
        "type": "website",
    },
    "automated-workflows": {
        "title": "Finance Workflow Automation | Revzio",
        "description": "Automate finance workflows with Revzio — route exceptions, approvals, and close tasks by policy so work moves without Slack chases or spreadsheet trackers.",
        "type": "website",
    },
    "accelerate-reporting-cycles": {
        "title": "Faster Financial Reporting Cycles | Revzio",
        "description": "Accelerate reporting cycles with Revzio — cleaner source data, automated recon and journals, and earlier close so leadership gets reliable numbers sooner.",
        "type": "website",
    },
    "controls-and-audit-trails": {
        "title": "SOX Controls & Audit Trail Automation | Revzio",
        "description": "Strengthen SOX controls and audit trails with Revzio — every match, journal, and approval captured automatically for auditors without month-end evidence hunts.",
        "type": "website",
    },
    "data-ingestion": {
        "title": "Finance Data Ingestion Platform | Revzio",
        "description": "Ingest ERP, bank, billing, and warehouse data into Revzio so Orion agents reconcile and prepare close work from trusted sources instead of manual exports.",
        "type": "website",
    },
    "reporting": {
        "title": "Financial Close Reporting | Revzio",
        "description": "Close reporting with Revzio gives finance leaders live status, exception trends, and audit-ready evidence — so cycles stop waiting on spreadsheet cleanup.",
        "type": "website",
    },
    "customers": {
        "title": "Customer Stories | Revzio",
        "description": "See how finance teams use Revzio to cut close time, automate reconciliation, and keep books audit-ready with Orion AI agents across SaaS and growth companies.",
        "type": "website",
    },
    "about": {
        "title": "About Revzio | Revzio",
        "description": "About Revzio — the AI financial close company building Orion agents so accounting teams reconcile continuously, close faster, and stay audit-ready.",
        "type": "website",
    },
    "contact": {
        "title": "Contact Sales & Support | Revzio",
        "description": "Contact Revzio for demos, sales, or support. Talk with a team that understands financial close, reconciliation automation, and what controllers need day to day.",
        "type": "website",
    },
    "careers": {
        "title": "Careers | Revzio",
        "description": "Join Revzio to build AI for financial close. Explore open roles if you want to help finance teams automate reconciliation, journals, and audit-ready workflows.",
        "type": "website",
    },
    "resources": {
        "title": "Finance Close Resources Hub | Revzio",
        "description": "Revzio resources for finance leaders — guides, blog posts, and playbooks on continuous close, reconciliation automation, and AI agents for accounting teams.",
        "type": "website",
    },
    "blog": {
        "title": "Finance Close Blog | Revzio",
        "description": "The Revzio blog covers AI in accounting, continuous close, reconciliation, revenue integrity, and playbooks for controllers and CFOs shipping faster closes.",
        "type": "website",
    },
    "guides": {
        "title": "Financial Close Guides | Revzio",
        "description": "Practical Revzio guides on month-end close, reconciliation, and AI for finance — frameworks controllers can use to shorten close without sacrificing control.",
        "type": "website",
    },
    "guides/setup-reconciliation-agent": {
        "title": "Setup Reconciliation Agent Guide | Revzio",
        "description": "Set up Revzio’s Reconciliation Agent in under an hour — connect bank feeds, configure match rules, and run your first automated reconciliation with audit trail.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("Reconciliation setup", None)],
    },
    "guides/automate-journal-entries": {
        "title": "Automate Journal Entries Guide | Revzio",
        "description": "Configure Revzio’s Journal Entry Agent end-to-end — accrual logic, chart-of-accounts mapping, ERP posting, and reviewer gates that keep journals audit-ready.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("Journal entries", None)],
    },
    "guides/3-day-close-guide": {
        "title": "3-Day Close with Orion Guide | Revzio",
        "description": "Week-by-week guide to running a 3-day close with Revzio Orion — continuous recon, prepared journals, checklist ownership, and controller sign-off.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("3-day close", None)],
    },
    "guides/netsuite-integration": {
        "title": "Connect Revzio to NetSuite | Revzio",
        "description": "Step-by-step Revzio–NetSuite integration: OAuth setup, field mapping, entity scope, and validating your first sync for continuous reconciliation and close.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("NetSuite", None)],
    },
    "guides/asc606-revenue-agent": {
        "title": "ASC 606 Revenue Agent Guide | Revzio",
        "description": "Configure Revzio’s Revenue Validation Agent for ASC 606 — recognition rules, contract modifications, billing-to-ERP checks, and audit-ready revenue output.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("ASC 606", None)],
    },
    "guides/audit-trail-soc2": {
        "title": "Audit Trail & SOC 2 Guide | Revzio",
        "description": "Configure Revzio audit trails for SOC 2 readiness — RBAC, immutable logs, reviewer sign-off, and evidence workflows that satisfy auditors year-round.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Guides", "/guides"), ("Audit trail", None)],
    },
    "agent-suite-reconciliation": {
        "title": "AI Reconciliation Agent | Revzio",
        "description": "Revzio’s Reconciliation Agent matches bank, billing, and ERP transactions continuously — explainable exceptions and audit trails for faster month-end close.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Reconciliation", None)],
    },
    "agent-suite-journal-entry": {
        "title": "AI Journal Entry Agent | Revzio",
        "description": "Revzio’s Journal Entry Agent generates validated journals from source data — mappings, gates, and ERP posting so accountants review instead of rebuild.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Journal entry", None)],
    },
    "agent-suite-ap": {
        "title": "AI Accounts Payable Agent | Revzio",
        "description": "Revzio’s AP Agent extracts invoices, runs 3-way match, and routes approvals — so payables teams clear exceptions instead of keying data every day.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Accounts payable", None)],
    },
    "agent-suite-ar": {
        "title": "AI Accounts Receivable Agent | Revzio",
        "description": "Revzio’s AR Agent automates cash application and collections priority — apply payments faster, reduce DSO, and keep receivables continuous through close.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Accounts receivable", None)],
    },
    "agent-suite-accruals": {
        "title": "AI Accruals Agent | Revzio",
        "description": "Revzio’s Accruals Agent calculates prepaid amortization and period-end accruals from source data — schedules, postings, and evidence auditors can follow.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Accruals", None)],
    },
    "agent-suite-revenue-validation": {
        "title": "AI Revenue Validation Agent | Revzio",
        "description": "Revzio’s Revenue Validation Agent checks billing and ERP against ASC 606 rules — flag contract and recognition gaps before they hit your next audit.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Revenue validation", None)],
    },
    "agent-suite-close-management": {
        "title": "AI Close Management Agent | Revzio",
        "description": "Revzio’s Close Management Agent orchestrates month-end — checklists, owners, dependencies, approvals, and variance status in one audit-ready workflow.",
        "type": "website",
        "crumbs": [("Home", "/"), ("Orion agents", "/agent-suite"), ("Close management", None)],
    },
    "glossary": {
        "title": "Finance Close Glossary | Revzio",
        "description": "A clear glossary of financial close terms — reconciliation, continuous close, accruals, cash application, and more — plus how Revzio Orion agents relate.",
        "type": "website",
    },
    "changelog": {
        "title": "Product Changelog | Revzio",
        "description": "Follow the Revzio changelog for Orion agent updates, platform improvements, and capabilities that help finance teams close faster with stronger audit trails.",
        "type": "website",
    },
    "privacy": {
        "title": "Privacy Policy | Revzio",
        "description": "How Revzio Pte. Ltd. collects, uses, stores, and protects your information — including data accessed through Google Workspace APIs and product usage details.",
        "type": "website",
    },
    "terms": {
        "title": "Terms of Service | Revzio",
        "description": "The agreement governing use of Revzio products and services, provided by Revzio Pte. Ltd., Singapore — covering accounts, acceptable use, and service terms.",
        "type": "website",
    },
    "dpa": {
        "title": "Data Processing Agreement | Revzio",
        "description": "Read the Revzio Data Processing Agreement for how personal data is processed when you use Revzio — roles, security measures, and a subprocessors overview.",
        "type": "website",
    },
}

BLOG_FALLBACK_DESC = {
    "3-day-close-playbook": "A CFO playbook for cutting close from 10 days to 3 — how continuous recon, journal prep, and clear ownership shrink month-end without adding headcount.",
    "3-way-match-ai": "Learn how AI-powered 3-way match clears invoice exceptions faster — PO, receipt, and invoice alignment that reduces AP noise before it hits the close.",
    "3-week-onboarding": "How Revzio onboards finance teams in about three weeks — connect sources, configure Orion agents, and move from spreadsheet close to continuous prep.",
    "ai-agency-in-finance": "Why AI in accounting needs agency, not just automation — how Revzio Orion agents prepare work while humans keep judgment, approvals, and control.",
    "continuous-close-readiness": "Why periodic reconciliation costs days every month — and how continuous close readiness helps finance teams stop starting from zero at month-end.",
    "cutting-close-three-days": "How teams cut close by three days at scale with continuous reconciliation, prepared journals, and exception workflows that keep auditors satisfied.",
    "exception-explainability": "Introducing exception explainability in Revzio — clearer break reasons so accountants resolve recon items faster instead of reverse-engineering matches.",
    "human-in-the-loop-finance": "What human-in-the-loop really means for finance teams using AI — approvals, materiality thresholds, and keeping controllers in control of the close.",
    "manual-recon-cost": "Calculate the hidden cost of manual reconciliation — time, errors, and delayed close — and see how automation changes the economics for finance teams.",
    "reconciliation-agent-deep-dive": "A deep dive into Orion’s Reconciliation Agent — how high auto-match rates happen, when humans step in, and what audit trail evidence looks like.",
    "revenue-integrity-playbook": "A controller’s playbook for revenue integrity — validating billing, recognition, and recon signals so revenue numbers stay trustworthy through close.",
    "revenue-recognition-scale": "Why revenue recognition spreadsheets break at Series B — and how scalable processes and AI validation keep SaaS finance teams close-ready as they grow.",
    "soc2-and-your-close-stack": "How SOC 2 expectations intersect with your close stack — controls, evidence, and choosing close tooling that supports audit readiness year-round.",
}

MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def validate(path: str, title: str, desc: str, *, blog: bool = False) -> None:
    if blog:
        if "…" in title or "..." in title:
            raise SystemExit(f"TITLE truncated: {path!r} -> {title!r}")
        if len(title) > 65 and title.endswith("| Revzio"):
            raise SystemExit(f"TITLE over 65 with suffix: {path!r} -> {title!r}")
        if len(title) <= 65 and not title.endswith("| Revzio"):
            # Prefer suffix when it fits
            if len(f"{title} | Revzio") <= 65:
                raise SystemExit(f"TITLE missing suffix though it fits: {path!r}")
    else:
        if len(title) > 60:
            raise SystemExit(f"TITLE too long ({len(title)}): {path!r} -> {title!r}")
        if not title.endswith("| Revzio"):
            raise SystemExit(f"TITLE must end with | Revzio: {path!r}")
    if "revzio" in title.replace("Revzio", ""):
        raise SystemExit(f"TITLE has lowercase brand: {path!r}")
    if not (140 <= len(desc) <= 160):
        raise SystemExit(f"DESC len {len(desc)} for {path!r}: {desc!r}")


def path_to_file(path: str) -> Path:
    if path == "":
        return ROOT / "index.html"
    if path.startswith("blog/") or path.startswith("guides/"):
        return ROOT / f"{path}.html"
    return ROOT / f"{path}.html"


def breadcrumb_ld(crumbs: list[tuple[str, str | None]], page_url: str) -> dict:
    elements = []
    for i, (name, href) in enumerate(crumbs, start=1):
        item: dict = {
            "@type": "ListItem",
            "position": i,
            "name": name,
        }
        if href:
            item["item"] = f"{SITE}{href}" if href.startswith("/") else href
        else:
            item["item"] = page_url
        elements.append(item)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }


def default_crumbs(path: str, title: str) -> list[tuple[str, str | None]]:
    label = title.replace(" | Revzio", "").strip()
    if path.startswith("blog/"):
        return [("Home", "/"), ("Blog", "/blog"), (label, None)]
    if path.startswith("guides/"):
        return [("Home", "/"), ("Guides", "/guides"), (label, None)]
    if path.startswith("agent-suite-"):
        return [("Home", "/"), ("Orion agents", "/agent-suite"), (label, None)]
    if path in {"", "agent-suite"}:
        return [("Home", "/")] if path == "" else [("Home", "/"), ("Orion agents", None)]
    return [("Home", "/"), (label, None)]


def canonical_url(path: str) -> str:
    return f"{SITE}/" if path == "" else f"{SITE}/{path}"


def org_software_ld() -> list[dict]:
    return [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Revzio",
            "legalName": "Revzio Pte. Ltd.",
            "url": f"{SITE}/",
            "logo": LOGO,
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Revzio",
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Web",
            "url": f"{SITE}/",
            "publisher": {"@type": "Organization", "name": "Revzio", "legalName": "Revzio Pte. Ltd."},
        },
    ]


def faq_ld(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def blog_ld(headline: str, description: str, url: str, date_published: str, author: str) -> list[dict]:
    author_name = author.replace("revzio", "Revzio").strip() or "Revzio Editorial"
    if author_name.lower() in {"revzio team", "revzio editorial", "revzio"}:
        author_name = "Revzio Editorial"
    return [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": headline,
            "description": description,
            "datePublished": date_published,
            "author": {"@type": "Organization", "name": author_name},
            "publisher": {
                "@type": "Organization",
                "name": "Revzio",
                "legalName": "Revzio Pte. Ltd.",
                "logo": {"@type": "ImageObject", "url": LOGO},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "image": OG_IMAGE,
            "url": url,
        },
        breadcrumb_ld([("Home", "/"), ("Blog", "/blog"), (headline, None)], url),
    ]


def seo_block(
    *,
    title: str,
    description: str,
    url: str,
    og_type: str,
    json_ld: list[dict] | dict | None,
) -> str:
    lines = [
        f"<title>{html_escape(title)}</title>",
        f'<meta name="description" content="{html_escape(description)}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:title" content="{html_escape(title)}">',
        f'<meta property="og:description" content="{html_escape(description)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html_escape(title)}">',
        f'<meta name="twitter:description" content="{html_escape(description)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]
    if json_ld is not None:
        payloads = json_ld if isinstance(json_ld, list) else [json_ld]
        for payload in payloads:
            dump = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
            lines.append(f'<script type="application/ld+json">{dump}</script>')
    return "\n".join(lines) + "\n"


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


SEO_STRIP_RE = re.compile(
    r"[ \t]*<(?:title|meta|link|script)[^>]*(?:"
    r"name=[\"']description[\"']|"
    r"rel=[\"']canonical[\"']|"
    r"property=[\"']og:[^\"']+[\"']|"
    r"name=[\"']twitter:[^\"']+[\"']|"
    r"type=[\"']application/ld\+json[\"']"
    r")[^>]*>.*?</(?:title|script)>\n?"
    r"|[ \t]*<(?:title|meta|link)[^>]*(?:"
    r"name=[\"']description[\"']|"
    r"rel=[\"']canonical[\"']|"
    r"property=[\"']og:[^\"']+[\"']|"
    r"name=[\"']twitter:[^\"']+[\"']"
    r")[^>]*/?>\n?"
    r"|[ \t]*<title>.*?</title>\n?",
    re.I | re.S,
)

# Simpler approach: remove title, description, canonical, og, twitter, ld+json script blocks individually
PATTERNS = [
    re.compile(r"[ \t]*<title>.*?</title>\s*", re.I | re.S),
    re.compile(r"[ \t]*<meta\s+name=[\"']description[\"'][^>]*>\s*", re.I),
    re.compile(r"[ \t]*<link\s+rel=[\"']canonical[\"'][^>]*>\s*", re.I),
    re.compile(r"[ \t]*<meta\s+property=[\"']og:[^\"']+[\"'][^>]*>\s*", re.I),
    re.compile(r"[ \t]*<meta\s+name=[\"']twitter:[^\"']+[\"'][^>]*>\s*", re.I),
    re.compile(r"[ \t]*<script\s+type=[\"']application/ld\+json[\"']>.*?</script>\s*", re.I | re.S),
]


def apply_to_html(html: str, block: str) -> str:
    for pat in PATTERNS:
        html = pat.sub("", html)
    # Insert SEO block after viewport meta (or charset if no viewport)
    m = re.search(r"<meta\s+name=[\"']viewport[\"'][^>]*>\s*", html, re.I)
    if not m:
        m = re.search(r"<meta\s+charset=[^>]*>\s*", html, re.I)
    if not m:
        m = re.search(r"<head[^>]*>\s*", html, re.I)
        insert_at = m.end() if m else 0
        return html[:insert_at] + block + html[insert_at:]
    insert_at = m.end()
    return html[:insert_at] + block + html[insert_at:]


def parse_blog_meta(html: str) -> tuple[str, str, str]:
    """Return headline, author, datePublished ISO."""
    hm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    headline = re.sub(r"<[^>]+>", "", hm.group(1)).strip() if hm else "Revzio Blog"
    am = re.search(r'class="article-meta"[^>]*>(.*?)</div>', html, re.I | re.S)
    author = "Revzio Team"
    published = "2026-05-01"
    if am:
        text = re.sub(r"<[^>]+>", "", am.group(1)).strip()
        parts = [p.strip() for p in text.split("·")]
        if parts:
            author = parts[0].replace("revzio", "Revzio")
        if len(parts) >= 2:
            # e.g. May 2026
            mm = re.match(r"([A-Za-z]+)\s+(\d{4})", parts[1])
            if mm:
                month = MONTHS.get(mm.group(1), 5)
                published = f"{mm.group(2)}-{month:02d}-01"
    return headline, author, published


def blog_title(headline: str) -> str:
    """Full headline + ' | Revzio'. If over ~65 chars, drop the suffix instead of truncating."""
    core = re.sub(r"\brevzio\b", "Revzio", headline, flags=re.I)
    with_suffix = f"{core} | Revzio"
    if len(with_suffix) <= 65:
        return with_suffix
    return core


def fit_desc(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if 140 <= len(text) <= 160:
        return text
    if len(text) < 140:
        # pad carefully with a neutral close — should not happen if fallbacks are right
        pad = " Learn more from the Revzio finance close blog."
        while len(text) < 140:
            text = (text + pad)[:160]
        return text[:160] if len(text) > 160 else text
    # trim to 160 at word boundary
    cut = text[:157]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "…"


def process_marketing_pages() -> list[str]:
    updated = []
    for path, cfg in PAGES.items():
        validate(path, cfg["title"], cfg["description"])
        file = path_to_file(path)
        if not file.exists():
            raise SystemExit(f"Missing file for {path}: {file}")
        html = file.read_text(encoding="utf-8")
        url = canonical_url(path)
        ld: list[dict] = []
        if cfg.get("home"):
            ld.extend(org_software_ld())
        if cfg.get("faq"):
            ld.append(faq_ld(cfg["faq"]))
        crumbs = cfg.get("crumbs") or default_crumbs(path, cfg["title"])
        if path != "":
            ld.append(breadcrumb_ld(crumbs, url))
        block = seo_block(
            title=cfg["title"],
            description=cfg["description"],
            url=url,
            og_type=cfg.get("type", "website"),
            json_ld=ld or None,
        )
        new_html = apply_to_html(html, block)
        file.write_text(new_html, encoding="utf-8")
        updated.append(path or "/")
    return updated


def process_blog_posts() -> list[str]:
    updated = []
    blog_dir = ROOT / "blog"
    for file in sorted(blog_dir.glob("*.html")):
        slug = file.stem
        path = f"blog/{slug}"
        html = file.read_text(encoding="utf-8")
        headline, author, published = parse_blog_meta(html)
        title = blog_title(headline)
        desc = fit_desc(BLOG_FALLBACK_DESC.get(slug, headline + " — insights from Revzio on AI financial close, reconciliation, and audit-ready accounting workflows."))
        if not (140 <= len(desc) <= 160):
            # force fit
            if len(desc) < 140:
                desc = fit_desc(desc + " Practical guidance for controllers and CFOs using Revzio.")
            desc = fit_desc(desc)
        validate(path, title, desc, blog=True)
        url = canonical_url(path)
        block = seo_block(
            title=title,
            description=desc,
            url=url,
            og_type="article",
            json_ld=blog_ld(headline, desc, url, published, author),
        )
        new_html = apply_to_html(html, block)
        file.write_text(new_html, encoding="utf-8")
        updated.append(path)
    return updated


def write_sitemap(paths: list[str]) -> None:
    meta = {
        "/": ("weekly", "1.0"),
        "/agent-suite": ("weekly", "0.9"),
        "/pricing": ("weekly", "0.9"),
        "/book-a-demo": ("weekly", "0.9"),
    }

    def prio(p: str) -> tuple[str, str]:
        if p in meta:
            return meta[p]
        if p.startswith("/blog/") or p.startswith("/guides/"):
            return ("monthly", "0.6")
        if p.startswith("/agent-suite-"):
            return ("monthly", "0.8")
        if p in {"/blog", "/resources", "/guides"}:
            return ("weekly", "0.7")
        if p in {"/privacy", "/terms", "/dpa"}:
            return ("yearly", "0.3")
        if p in {"/careers", "/changelog"}:
            return ("weekly" if p == "/changelog" else "monthly", "0.5")
        if p.startswith("/industry-"):
            return ("monthly", "0.7")
        return ("monthly", "0.7")

    all_paths = ["/"] + [f"/{p}" for p in paths if p != "/"]
    seen = []
    for p in all_paths:
        if p not in seen and p != "/llms.txt":
            seen.append(p)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in seen:
        cf, pr = prio(p)
        loc = f"{SITE}{p}" if p != "/" else f"{SITE}/"
        if p == "/":
            f = ROOT / "index.html"
        elif p.startswith("/blog/") or p.startswith("/guides/"):
            f = ROOT / f"{p[1:]}.html"
        else:
            f = ROOT / f"{p[1:]}.html"
        lastmod = date.fromtimestamp(f.stat().st_mtime).isoformat() if f.exists() else TODAY
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{cf}</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    # validate all configured descriptions first
    for path, cfg in PAGES.items():
        validate(path, cfg["title"], cfg["description"])
        print(f"OK {path or '/':40} title={len(cfg['title']):2} desc={len(cfg['description']):3}")

    m = process_marketing_pages()
    b = process_blog_posts()
    write_sitemap(m + b)
    print(f"Updated {len(m)} marketing pages, {len(b)} blog posts, sitemap.xml")


if __name__ == "__main__":
    main()
