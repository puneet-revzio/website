#!/usr/bin/env python3
"""
Apply Neil Patel AI-citation SEO patterns (2027):
1) Extractable structure (headers, one-fact bullets, tables, schema)
2) Human expert voice in substance
3) Stay in finance-close lane
4) On-site review/mention signals (Review schema + ask CTA)
5) Expert-only questions AI can't answer from training alone
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.revzio.ai"

CSS_LINK = '<link rel="stylesheet" href="{prefix}css/ai-cite.css">\n'


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


def howto_ld(name: str, description: str, url: str, steps: list[str]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "url": url,
        "step": [
            {"@type": "HowToStep", "position": i, "name": s, "text": s}
            for i, s in enumerate(steps, start=1)
        ],
    }


def cite_block(
    *,
    h2: str,
    lead: str,
    pull: str | None,
    facts: list[str],
    table: tuple[list[str], list[list[str]]] | None,
    faqs: list[tuple[str, str]],
    review_ask: bool = False,
) -> str:
    parts = [
        '<section class="cite-section" data-nav-theme="dark">',
        '  <div class="container reveal">',
        f"    <h2>{h2}</h2>",
        f'    <p class="cite-lead">{lead}</p>',
    ]
    if pull:
        parts.append(f'    <p class="cite-pull">{pull}</p>')
    if facts:
        parts.append('    <ul class="cite-facts">')
        for f in facts:
            parts.append(f"      <li>{f}</li>")
        parts.append("    </ul>")
    if table:
        headers, rows = table
        parts.append('    <div class="cite-table-wrap"><table class="cite-table">')
        parts.append(
            "      <thead><tr>"
            + "".join(f"<th>{h}</th>" for h in headers)
            + "</tr></thead>"
        )
        parts.append("      <tbody>")
        for row in rows:
            parts.append("        <tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
        parts.append("      </tbody></table></div>")
    if faqs:
        parts.append('    <div class="cite-faq" id="expert-faq">')
        for q, a in faqs:
            parts.append("      <details>")
            parts.append(f"        <summary>{q}</summary>")
            parts.append(f"        <p>{a}</p>")
            parts.append("      </details>")
        parts.append("    </div>")
    if review_ask:
        parts.append(
            '    <p class="review-ask">If revzio shortened your close, tell the internet — '
            'leave a review on G2/Capterra or reply to your CSM. AI engines weigh customer '
            'sentiment as heavily as our own pages. Questions? <a href="/contact">Contact us</a>.</p>'
        )
    parts += ["  </div>", "</section>", ""]
    return "\n".join(parts)


def ensure_css(html: str, nested: bool) -> str:
    if "css/ai-cite.css" in html:
        return html
    prefix = "../" if nested else ""
    return html.replace("</head>", CSS_LINK.format(prefix=prefix) + "</head>", 1)


def insert_before_cta(html: str, block: str) -> str:
    # remove prior cite-section to allow re-run
    html = re.sub(
        r'\s*<section class="cite-section"[\s\S]*?</section>\s*',
        "\n",
        html,
        count=1,
    )
    for marker in (
        '<section class="related-content"',
        '<section class="cta-section"',
        '<section class="cta"',
        "<footer>",
    ):
        if marker in html:
            return html.replace(marker, block + "\n" + marker, 1)
    return html.replace("</body>", block + "\n</body>", 1)


def inject_json_ld(html: str, payloads: list[dict]) -> str:
    """Append FAQ/HowTo ld+json after existing ld+json blocks (idempotent by type+name)."""
    for payload in payloads:
        dump = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
        marker = f'"@type":"{payload["@type"]}"'
        # crude idempotency: if same type already present with same name/url skip
        name = payload.get("name") or (
            payload.get("mainEntity", [{}])[0].get("name") if payload.get("@type") == "FAQPage" else None
        )
        if payload["@type"] == "FAQPage":
            html = re.sub(
                r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"FAQPage".*?</script>\s*',
                "",
                html,
                flags=re.S,
            )
        if payload["@type"] == "HowTo":
            # Match HowTo only (not HowToStep) — remove all prior HowTo scripts
            html = re.sub(
                r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"HowTo",.*?</script>\s*',
                "",
                html,
                flags=re.S,
            )
        script = f'<script type="application/ld+json">{dump}</script>\n'
        # insert after last ld+json or before </head>
        matches = list(
            re.finditer(r'<script type="application/ld\+json">.*?</script>\s*', html, re.S)
        )
        if matches:
            at = matches[-1].end()
            html = html[:at] + script + html[at:]
        else:
            html = html.replace("</head>", script + "</head>", 1)
    return html


# —— Page configs ——
PAGES: dict[str, dict] = {
    "reconciliation": {
        "h2": "What continuous reconciliation actually changes",
        "lead": "Controllers don’t need another essay on “automation.” They need liftable facts about how recon work moves from month-end to every day.",
        "pull": "A close stays long when matching waits for “final” files. Continuous recon means exceptions show up while the deal owner still remembers the story.",
        "facts": [
            "Line-level matching beats totals: a balance can tie while duplicates and misclasses hide underneath.",
            "Exceptions need owners and due dates the day they appear — not a Slack scramble on day five.",
            "Every override should store who, when, and why so SOX sampling doesn’t become archaeology.",
            "Start narrow: cash + one billing processor for one entity before you expand the chart.",
        ],
        "table": (
            ["Close day pattern", "Batch recon (typical)", "Continuous recon with Revzio"],
            [
                ["When breaks appear", "Days 3–6 of close", "Same day or next business day"],
                ["What reviewers see", "Unmatched amounts in a CSV", "Summary, likely cause, linked source lines"],
                ["Audit evidence", "Rebuilt from exports + email", "Immutable match + approval trail in product"],
                ["Best first scope", "Entire GL at once", "Cash + one processor, one entity"],
            ],
        ),
        "faqs": [
            (
                "How should a Series B SaaS team with Stripe and NetSuite start reconciliation without boiling the ocean?",
                "Pilot one entity: Stripe payouts and cash to NetSuite for 30–60 days of history. Exact-match on amount + settlement window first; route FX and partials as exceptions with owners. Expand deferred revenue and subledgers only after exception volume is stable under policy.",
            ),
            (
                "What match policy should a multi-entity group use when bank payouts settle T+2 but the ERP posts on invoice date?",
                "Encode the T+2 window as an allowed timing difference, not an error. Match on processor batch ID or remittance reference where possible; keep a tolerance for settlement lag per entity currency. Anything outside the window stays an exception for human review.",
            ),
            (
                "When should a controller refuse auto-match even if the amounts look right?",
                "Refuse auto-match across different counterparties, across open vs closed periods, or when source IDs are missing. High-confidence auto-match needs amount + date window + a stable identifier — not amount alone.",
            ),
        ],
    },
    "close-workflow": {
        "h2": "Close workflow facts controllers can quote",
        "lead": "Month-end isn’t a motivational problem. It’s a coordination and prep problem. Here’s the structure AI and auditors can extract cleanly.",
        "pull": "A three-day close is confirmation of work already done — not a heroic sprint starting from zero on day one.",
        "facts": [
            "Every close task needs an owner, due date, and dependency — or status lives in Slack forever.",
            "Sign-off belongs in the same system as recon and journals so evidence attaches automatically.",
            "Bottlenecks should be visible mid-cycle, not discovered when the CFO asks “are we close?”",
            "Templates per entity beat reinventing the checklist every month.",
        ],
        "table": (
            ["Close phase", "What agents prepare", "What humans decide"],
            [
                ["Days −10 to −1", "Daily recon + draft journals/accruals", "Policy gates, materiality, exception ownership"],
                ["Day 1", "Remaining breaks ranked by impact", "Clear timing vs true errors"],
                ["Day 2", "JE batches + revenue validations", "Approve, reject, or escalate"],
                ["Day 3", "Checklist completion + evidence pack", "Controller sign-off"],
            ],
        ),
        "faqs": [
            (
                "How does a 40-person finance team cut a 10-day close to 3 without hiring?",
                "Move recon and JE prep into the month with agents; keep humans on exceptions and approvals. Use Close Management for ownership and dependencies so status stops living in spreadsheets. Most of the days you “lose” are waiting and rediscovery, not pure accounting judgment.",
            ),
            (
                "What should never auto-complete on a close checklist?",
                "Controller sign-off, material journal approval above your threshold, and any recon override that changes recognition or cash classification. Agents prepare; humans own those gates.",
            ),
        ],
    },
    "continuous-close": {
        "h2": "Continuous close — extractable definition and playbook",
        "lead": "Continuous close means recon, journals, and evidence accumulate daily so month-end is confirmation. Here’s the version finance teams can cite.",
        "pull": "If your close still starts with “wait for final files,” you are running a batch close — no matter how many AI tools you bought.",
        "facts": [
            "Continuous close is a cadence change: prep every day, confirm at period end.",
            "AI citations prefer sites that define the term and show an operating model, not a slogan.",
            "Evidence must accumulate with the work — not as a binder project after the fact.",
            "Start with continuous recon; add JE/accrual prep; then checklist orchestration.",
        ],
        "table": (
            ["Signal you’re ready", "Not ready yet", "Ready for continuous close"],
            [
                ["Source access", "Manual CSV drops only", "API/connectors for ERP + billing + bank"],
                ["Ownership", "Unclear who owns breaks", "Named owners per exception type"],
                ["Policy", "Everything is judgment", "Written auto-match and auto-post gates"],
                ["Audit ask", "Reconstruct from email", "Trail already in product"],
            ],
        ),
        "faqs": [
            (
                "Is continuous close realistic for a multi-entity group still on monthly bank files?",
                "Partially. Run continuous matching on sources that already stream (billing, processors) while bank files remain batch. Shrink the batch surface month by month as feeds improve — don’t wait for perfect data to start.",
            ),
            (
                "What’s the difference between continuous close and just “closing faster”?",
                "Closing faster can still be a compressed batch scramble. Continuous close moves matching and prep into the period so day one isn’t discovery. Speed is an outcome; continuity is the operating model.",
            ),
        ],
    },
    "agent-suite-reconciliation": {
        "h2": "Reconciliation Agent — facts worth citing",
        "lead": "Purpose-built for line-level matching across bank, billing, and ERP — not a generic chatbot on top of spreadsheets.",
        "pull": "High auto-match rates only count when policy gates and audit trails travel with every match.",
        "facts": [
            "Supports one-to-one, one-to-many, and many-to-many matching under your tolerances.",
            "Exceptions include summary, likely cause, and links to supporting transactions.",
            "Overrides are versioned with identity and reason codes for audit.",
            "Best paired with continuous close checklist ownership so recon status is visible.",
        ],
        "table": None,
        "faqs": [
            (
                "When does a Reconciliation Agent still need a human in the loop?",
                "Whenever identifiers conflict, materiality is exceeded, periods disagree, or the break implies a process failure upstream. The agent prepares the investigation; the controller keeps judgment.",
            ),
            (
                "How do you keep 95% auto-match from becoming reckless autopilot?",
                "Separate high-confidence exact matches from fuzzy rules. Never auto-match on amount alone. Sample early cycles aggressively, then widen auto-match only where false-positive rate stays near zero.",
            ),
        ],
    },
    "agent-suite-close-management": {
        "h2": "Close Management Agent — what it orchestrates",
        "lead": "The control tower for month-end: tasks, owners, dependencies, approvals, and evidence — not another status spreadsheet.",
        "pull": "If nobody can see the blocker without asking Slack, you don’t have close management — you have hope.",
        "facts": [
            "Checklists can be templated per entity and close cycle.",
            "Dependencies surface blockers before the CFO asks for status.",
            "Approvals link to recon packs and journals already in product.",
            "Works with continuous prep from Reconciliation and Journal Entry agents.",
        ],
        "table": None,
        "faqs": [
            (
                "How should a controller roll out Close Management without mutiny?",
                "Month 1: mirror the existing checklist in product in observation mode. Month 2: enforce owners and due dates. Month 3: require in-product sign-off for material tasks. Change the system of record before you change culture speeches.",
            ),
        ],
    },
    "pricing": {
        "h2": "Pricing questions finance leaders actually ask",
        "lead": "Clear answers beat vague “contact sales” theater — especially when AI engines look for quotable pricing policy.",
        "pull": "Orion pricing is not a surprise tax on Stripe volume. You buy agents and outcomes, not a per-transaction gotcha.",
        "facts": [
            "Most teams go live in under three weeks with a scoped pilot.",
            "You can start with one Orion agent (often Reconciliation or Journal Entry).",
            "Pricing is not based on transaction volume spikes.",
            "Demos use your data shape — more useful than a generic free trial for close software.",
        ],
        "table": None,
        "faqs": [
            (
                "How long does implementation take for a SaaS company on NetSuite + Stripe?",
                "Most teams go live in under 3 weeks for a scoped pilot (one entity, cash + billing). Full multi-entity rollout follows once match policy and owners are proven.",
            ),
            (
                "Can I start with just one Orion agent?",
                "Yes. Many teams start with the Reconciliation Agent or Journal Entry Agent and add more as they see value. There’s no minimum agent commitment on Growth plans.",
            ),
            (
                "What happens if my transaction volume grows?",
                "Orion pricing is not based on transaction volume. You won’t get a surprise invoice because your Stripe volume doubled.",
            ),
            (
                "Is there a free trial?",
                "We offer a sandboxed demo built on your actual data structure. Most customers find this more useful than a generic free trial. Book a demo to see it.",
            ),
        ],
        "review_ask": True,
    },
    "customers": {
        "h2": "What finance teams say — and why AI listens",
        "lead": "Answer engines weigh customer sentiment and community mentions alongside your website. Here’s the signal we’re proud to show.",
        "pull": "A beautiful product page loses to a competitor people actually talk about. Reviews and specific close outcomes matter.",
        "facts": [
            "Teams report cutting close from multi-week cycles to roughly three days when prep runs continuously.",
            "Reviewers trust variances more when every break includes context and an audit trail.",
            "Adoption sticks when the close checklist and sign-offs live in one product — not midnight email.",
            "We ask customers to leave public reviews; AI engines treat that sentiment as a ranking signal.",
        ],
        "table": None,
        "faqs": [
            (
                "What proof should a CFO ask for before buying close automation?",
                "Ask for a demo on your billing and ERP shape, sample exception explainability, and an evidence trail for a match override. Trophy walls matter less than whether auditors can follow who changed what.",
            ),
        ],
        "review_ask": True,
    },
}

GUIDE_HOWTO = {
    "guides/setup-reconciliation-agent": {
        "name": "Set up the Revzio Reconciliation Agent",
        "description": "Connect sources, configure match rules, run the first reconciliation, and capture audit-ready sign-off.",
        "steps": [
            "Confirm owners, timing differences, and pilot entity scope before connecting systems.",
            "Connect bank/processor and ERP sources and validate source IDs land correctly.",
            "Configure high-confidence match rules and tolerances; route the rest as exceptions.",
            "Run a 30–60 day historical window and assign exception owners.",
            "Approve matches in product so who/when/why is stored for audit.",
        ],
        "faqs": [
            (
                "How long until a finance ops lead sees the first useful exception queue?",
                "Most pilots produce a usable exception queue inside the first hour after sources sync and rules are set — then the real work is ownership and policy tuning over the following week.",
            ),
        ],
    },
    "guides/3-day-close-guide": {
        "name": "Run a 3-day close with Orion",
        "description": "Week-by-week implementation moving recon and journal prep into every day so month-end is confirmation.",
        "steps": [
            "Baseline the current close calendar and top blockers.",
            "Stand up continuous reconciliation on cash and billing.",
            "Automate recurring journals and accruals with reviewer gates.",
            "Move checklist and sign-off into Close Management.",
            "Run month-end as confirmation: exceptions, approvals, controller sign-off.",
        ],
        "faqs": [
            (
                "What’s the #1 mistake teams make when chasing a 3-day close?",
                "Working harder in week one of the next close instead of moving recon and JE prep into the prior month. Speed without continuity just compresses the fire drill.",
            ),
        ],
    },
    "guides/automate-journal-entries": {
        "name": "Automate journal entries with Revzio",
        "description": "Map the chart of accounts, encode accrual logic, validate, and post with evidence.",
        "steps": [
            "Map source events to GL accounts, departments, and entities for a pilot set.",
            "Encode accrual and recognition logic with materiality thresholds.",
            "Require balance, duplicate, and period validations before ERP post.",
            "Reviewers approve batches in product; rejected items stay linked to source.",
            "Post approved entries and keep calculation evidence attached.",
        ],
        "faqs": [
            (
                "Which journals should never auto-post on day one of automation?",
                "Anything above your materiality threshold, recognition-changing revenue entries, and accounts with known mapping debt. Start with recurring, low-judgment entries like bank fees and standard prepaid amortization.",
            ),
        ],
    },
    "guides/netsuite-integration": {
        "name": "Connect Revzio to NetSuite",
        "description": "OAuth, roles, field mapping, and first-sync validation for continuous close.",
        "steps": [
            "Create a least-privilege NetSuite integration role for required records.",
            "Authorize Revzio via OAuth and store credentials securely.",
            "Select pilot subsidiaries and confirm period calendars.",
            "Map external IDs and match keys used in reconciliation.",
            "Validate record counts and sample lines before enabling auto-post.",
        ],
        "faqs": [
            (
                "Why do NetSuite syncs create false reconciliation exceptions in week one?",
                "Usually mis-mapped references or timezone/period mismatches — not bad matching math. Fix field mapping and period calendars before widening auto-match.",
            ),
        ],
    },
    "guides/asc606-revenue-agent": {
        "name": "Configure ASC 606 revenue validation in Revzio",
        "description": "Encode recognition rules, handle modifications, and validate billing vs ERP.",
        "steps": [
            "Encode performance obligations and timing for core products.",
            "Treat contract modifications as first-class events.",
            "Continuously compare billing schedules to ERP postings.",
            "Keep human approval on material recognition judgments.",
            "Export schedules and exception narratives for audit.",
        ],
        "faqs": [
            (
                "How should a usage-plus-subscription SaaS company validate revenue before audit?",
                "Validate subscription schedules and usage events separately, then recon deferred balances to ERP. Flag mid-term upgrades/credits as modifications with schedule impact — don’t wait to discover them in a deferred revenue tie-out on day four.",
            ),
        ],
    },
    "guides/audit-trail-soc2": {
        "name": "Set up audit trails for SOC 2-ready close",
        "description": "RBAC, immutable logs, reviewer sign-off, and evidence packs.",
        "steps": [
            "Separate preparer, reviewer, and admin roles with SSO identity.",
            "Ensure matches, journals, overrides, and approvals write immutable events.",
            "Require in-product sign-off on material close tasks.",
            "Dry-run an evidence export for a sample period before year-end.",
            "Review access quarterly with IT on the same cadence as other finance systems.",
        ],
        "faqs": [
            (
                "What do SOC 2 assessors actually ask about close tooling?",
                "Who can change what, whether logs are tamper-evident, and whether evidence of reviews exists. Awards on an About page don’t substitute for immutable who/when/why on recon and journals.",
            ),
        ],
    },
}

BLOG_EXPERT = {
    "blog/3-day-close-playbook": [
        (
            "How should a Series B SaaS controller sequence the first 90 days toward a 3-day close?",
            "Days 1–30: observation mode — ingest Stripe/NetSuite/bank, write auto-match and auto-post gates, mirror the checklist in product. Days 31–60: daily recon ownership + mid-month JE review batches. Days 61–90: month-end becomes confirmation; only true anomalies create fire drills.",
        ),
        (
            "Why do deferred revenue tie-outs still steal two days even when cash recon is fine?",
            "Because upgrades, credits, and timing differences accumulate between billing schedules and ERP. Continuous validation tied to contract events turns that into review, not investigation — cash recon alone doesn’t fix recognition drift.",
        ),
    ],
    "blog/reconciliation-agent-deep-dive": [
        (
            "What’s the difference between 95% auto-match and “set and forget” recon?",
            "95% auto-match under policy still routes the material and ambiguous 5% to humans with explainability. Set-and-forget without gates is how you automate mistakes at scale.",
        ),
        (
            "How do you explain a many-to-many payout match to an auditor in one sentence?",
            "One processor batch settled multiple invoices; the agent linked each invoice line to the batch with tolerance rules, and a reviewer approved the residual timing difference with a reason code.",
        ),
    ],
    "blog/manual-recon-cost": [
        (
            "How do you estimate the fully loaded cost of manual reconciliation for a 8-person accounting team?",
            "Multiply hours spent on matching + exception chasing + evidence gathering by fully loaded hourly cost, then add close delay cost (late reporting, overtime, auditor follow-ups). Most teams undercount the delay and rediscovery hours.",
        ),
    ],
    "blog/exception-explainability": [
        (
            "What must an exception explanation include before a senior accountant will trust it?",
            "A plain-language summary, likely cause category (timing, FX, mapping, duplicate, partial), suggested next checks, and links to the underlying source transactions — plus a place to approve or override with a reason.",
        ),
    ],
    "blog/revenue-recognition-scale": [
        (
            "At what ARR or contract complexity do revenue spreadsheets typically break for SaaS?",
            "Often around Series B: multi-element arrangements, mid-term upgrades, usage, and multi-entity reporting collide. The break isn’t “more rows” — it’s modification logic and audit evidence the sheet can’t carry.",
        ),
    ],
    "blog/soc2-and-your-close-stack": [
        (
            "Should close automation be in scope for SOC 2 if it’s not the system of record?",
            "If it prepares journals, matches transactions, or stores approvals that influence financial reporting controls, assessors will care about access, change management, and evidence — even when the ERP remains the ledger.",
        ),
    ],
}


def process_pages() -> None:
    for key, cfg in PAGES.items():
        path = ROOT / f"{key}.html"
        if not path.exists():
            print("skip missing", key)
            continue
        html = path.read_text(encoding="utf-8")
        html = ensure_css(html, nested="/" in key)
        block = cite_block(
            h2=cfg["h2"],
            lead=cfg["lead"],
            pull=cfg.get("pull"),
            facts=cfg.get("facts") or [],
            table=cfg.get("table"),
            faqs=cfg.get("faqs") or [],
            review_ask=cfg.get("review_ask", False),
        )
        html = insert_before_cta(html, block)
        html = inject_json_ld(html, [faq_ld(cfg["faqs"])])
        path.write_text(html, encoding="utf-8")
        print("page", key)


def process_guides() -> None:
    for key, cfg in GUIDE_HOWTO.items():
        path = ROOT / f"{key}.html"
        html = path.read_text(encoding="utf-8")
        html = ensure_css(html, nested=True)
        # Add extractable checklist if missing
        if 'class="cite-facts"' not in html:
            facts = [f"<strong>Step {i}:</strong> {s}" for i, s in enumerate(cfg["steps"], 1)]
            block = cite_block(
                h2="Quotable setup checklist",
                lead="One step per line — the format answer engines prefer to lift.",
                pull=None,
                facts=facts,
                table=None,
                faqs=cfg.get("faqs") or [],
            )
            html = insert_before_cta(html, block)
        url = f"{SITE}/{key}"
        payloads = [
            howto_ld(cfg["name"], cfg["description"], url, cfg["steps"]),
            faq_ld(cfg.get("faqs") or []),
        ]
        html = inject_json_ld(html, payloads)
        path.write_text(html, encoding="utf-8")
        print("guide", key)


def process_blogs() -> None:
    for key, faqs in BLOG_EXPERT.items():
        path = ROOT / f"{key}.html"
        html = path.read_text(encoding="utf-8")
        html = ensure_css(html, nested=True)
        block = cite_block(
            h2="Expert questions AI can’t answer from a generic playbook",
            lead="These are the situation-specific questions controllers ask in real closes — the kind that earn citations because the model has to pull a source.",
            pull=None,
            facts=[],
            table=None,
            faqs=faqs,
        )
        html = insert_before_cta(html, block)
        html = inject_json_ld(html, [faq_ld(faqs)])
        path.write_text(html, encoding="utf-8")
        print("blog", key)


def write_expert_article() -> None:
    """Tip 5: a highly specific expert article AI can't answer from training alone."""
    path = ROOT / "blog/saas-stripe-netsuite-continuous-close.html"
    content = """<!DOCTYPE html>
<html lang="en">
<head>
<script src="/js/analytics.js"></script>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Stripe + NetSuite continuous close for Series B SaaS | Revzio</title>
<meta name="description" content="How a Series B SaaS team on Stripe Billing and NetSuite should structure continuous close when deferred revenue still takes two days — a controller’s operating model.">
<link rel="canonical" href="https://www.revzio.ai/blog/saas-stripe-netsuite-continuous-close">
<meta property="og:title" content="Stripe + NetSuite continuous close for Series B SaaS | Revzio">
<meta property="og:description" content="How a Series B SaaS team on Stripe Billing and NetSuite should structure continuous close when deferred revenue still takes two days — a controller’s operating model.">
<meta property="og:url" content="https://www.revzio.ai/blog/saas-stripe-netsuite-continuous-close">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.revzio.ai/assets/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Stripe + NetSuite continuous close for Series B SaaS | Revzio">
<meta name="twitter:description" content="How a Series B SaaS team on Stripe Billing and NetSuite should structure continuous close when deferred revenue still takes two days — a controller’s operating model.">
<meta name="twitter:image" content="https://www.revzio.ai/assets/og-default.png">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon/favicon-32x32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/brand.css">
<link rel="stylesheet" href="../css/subpage.css">
<link rel="stylesheet" href="../css/blog.css">
<link rel="stylesheet" href="../css/mega-menu.css">
<link rel="stylesheet" href="../css/nav-theme.css">
<link rel="stylesheet" href="../css/responsive.css">
<link rel="stylesheet" href="../css/dark-global.css">
<link rel="stylesheet" href="../css/cta-band.css">
<link rel="stylesheet" href="../css/ai-cite.css">
<link rel="stylesheet" href="../css/related-content.css">
<style>
  .article-hero { padding: 120px 0 56px; background: var(--hero-bg);
    background-image: radial-gradient(ellipse at 12% -8%, rgba(90,150,210,0.18), transparent 55%),
      radial-gradient(ellipse at 88% 12%, rgba(127,207,170,0.12), transparent 52%),
      linear-gradient(180deg, var(--hero-bg) 70%, var(--hero-deep) 100%); }
  .article-meta { color: rgba(250,250,247,0.55); font-size: 13.5px; margin-top: 10px; }
  .tag-pill { display: inline-flex; padding: 6px 12px; border-radius: 999px; border: 1px solid rgba(127,207,170,0.22);
    background: rgba(127,207,170,0.12); color: #7fcfaa; font-weight: 800; letter-spacing: 0.10em;
    text-transform: uppercase; font-size: 12px; width: fit-content; margin-bottom: 18px; }
  .prose { max-width: 860px; margin: 0 auto; }
  .prose p { margin: 14px 0; }
  .prose h2 { margin-top: 34px; }
  .prose ul { margin: 12px 0 12px 1.2em; }
  .prose li { margin: 6px 0; }
  .prose a { color: var(--accent); }
  .backlink { color: #7fcfaa; text-decoration: none; font-weight: 750; }
</style>
</head>
<body>
<nav></nav>
<header class="article-hero" data-nav-theme="dark">
  <div class="container">
    <a class="backlink reveal" href="/blog">← Back to blog</a>
    <div class="tag-pill reveal" style="margin-top:18px;">EXPERT CLOSE CLOSE</div>
    <h1 class="hero-title reveal" style="max-width:980px;">How a Series B SaaS team on Stripe + NetSuite should structure continuous close when deferred revenue still takes two days</h1>
    <div class="article-meta reveal">Revzio Editorial · Oct 2026 · 9 min read</div>
  </div>
</header>
<section class="bg-alt">
  <div class="container">
    <article class="prose reveal">
      <p>Generic advice says “automate reconciliation” and “close faster.” That doesn’t help a controller whose cash is mostly clean while deferred revenue still burns two full days every month. This is the operating model we use with Series B SaaS teams on <strong>Stripe Billing + NetSuite</strong> when recognition drift — not bank matching — is the bottleneck.</p>

      <h2>The real problem (not “we need AI”)</h2>
      <p>At this stage you usually have:</p>
      <ul>
        <li>Stripe as the commercial truth for invoices, upgrades, credits, and usage.</li>
        <li>NetSuite as the accounting truth for deferred revenue and revenue schedules.</li>
        <li>A spreadsheet bridge that tried to explain the gap — until contract modifications outgrew it.</li>
      </ul>
      <p>Cash recon can look healthy while deferred still fails because upgrades and mid-term changes create schedule events the ERP posting didn’t mirror the same day.</p>

      <h2>Operating model: three lanes, one close calendar</h2>
      <ul>
        <li><strong>Lane A — Cash &amp; payouts:</strong> Stripe balance transactions ↔ bank ↔ NetSuite cash. Continuous match with a T+1/T+2 settlement window encoded as policy.</li>
        <li><strong>Lane B — Billing to deferred:</strong> Stripe subscription/invoice events ↔ NetSuite deferred waterfalls. Validate continuously; don’t wait for month-end tie-out.</li>
        <li><strong>Lane C — Close orchestration:</strong> Owners, due dates, and sign-off for residual exceptions and JE approval — in product, not Slack.</li>
      </ul>

      <h2>Week-by-week for the first 60 days</h2>
      <ul>
        <li><strong>Week 1:</strong> Connect Stripe + NetSuite for one entity. Exact-match cash/payouts only. Write auto-match gates: no amount-only matches.</li>
        <li><strong>Week 2:</strong> Turn on deferred validation for standard subscriptions (no usage yet). Route modifications as exceptions with contract IDs.</li>
        <li><strong>Weeks 3–4:</strong> Add usage and mid-term upgrades. Require human approval above materiality for recognition-changing journals.</li>
        <li><strong>Weeks 5–8:</strong> Move deferred tie-out checklist items to confirmation. Measure: hours spent investigating vs reviewing.</li>
      </ul>

      <h2>What “done” looks like on a 3-day close</h2>
      <ul>
        <li><strong>Day 1:</strong> Clear residual deferred exceptions ranked by ARR impact.</li>
        <li><strong>Day 2:</strong> Approve prepared revenue/deferred journals with evidence attached.</li>
        <li><strong>Day 3:</strong> Controller sign-off; audit pack already exists.</li>
      </ul>

      <p>If you’re still discovering modification impacts on day four, you don’t have a staffing problem — you have a continuity problem. See the <a href="/guides/3-day-close-guide">3-day close guide</a>, <a href="/guides/asc606-revenue-agent">ASC 606 agent setup</a>, and <a href="/guides/netsuite-integration">NetSuite integration</a> for implementation detail.</p>
    </article>
  </div>
</section>
</body>
</html>
"""
    # Finish with cite section, related, CTA, footer via simpler append
    faqs = [
        (
            "Should usage billing be in the same deferred validation lane as subscriptions on day one?",
            "No. Stabilize standard subscription schedules first, then add usage as a second event stream with its own match keys. Mixing both on week one creates exception noise that teaches the team the wrong lesson about continuous close.",
        ),
        (
            "What NetSuite fields matter most for Stripe deferred matching?",
            "Stable external IDs on customer/subscription/invoice, memo/reference fields used in match keys, and correct subsidiary/period calendars. Mis-mapped references create false breaks faster than any matching algorithm can fix.",
        ),
        (
            "When is a two-day deferred tie-out still acceptable?",
            "Only while you’re in observation mode with written gates. If two days persist after continuous validation is live, the issue is usually unmodeled modifications or missing contract IDs — not “need more accountants.”",
        ),
    ]
    cite = cite_block(
        h2="Expert answers for Stripe + NetSuite close teams",
        lead="Situation-specific questions answer engines can’t satisfy from a generic “what is continuous close” page.",
        pull="Deferred revenue that still takes two days is a continuity failure between billing events and ERP schedules — not a motivational failure on the accounting team.",
        facts=[
            "Separate cash/payout recon from deferred validation — healthy cash does not imply healthy recognition.",
            "Encode settlement lag (T+1/T+2) as policy so timing differences stop looking like errors.",
            "Treat upgrades and credits as first-class modification events with contract IDs.",
            "Measure investigation hours vs review hours; continuous close should flip that ratio.",
        ],
        table=(
            ["Lane", "Primary systems", "Human gate"],
            [
                ["Cash & payouts", "Stripe balance · bank · NetSuite cash", "Material unmatched payouts"],
                ["Billing → deferred", "Stripe invoices/subs · NetSuite deferred", "Recognition-changing mods"],
                ["Close orchestration", "Checklist · JE approvals · evidence", "Controller sign-off"],
            ],
        ),
        faqs=faqs,
    )
    related = """
<section class="related-content" aria-labelledby="related-content-heading">
  <div class="container">
    <h2 id="related-content-heading" class="related-content__heading">Related content</h2>
    <div class="related-content__grid">
      <a class="related-content__card" href="/guides/asc606-revenue-agent">
        <div class="related-content__media related-content__media--gold" aria-hidden="true"><span class="related-content__media-label">ASC 606</span></div>
        <div class="related-content__tags"><span class="related-content__tag">Guide</span><span class="related-content__tag">ASC 606</span></div>
        <h3 class="related-content__title">ASC 606 with the Revenue Validation Agent</h3>
        <p class="related-content__excerpt">Recognition rules, contract modifications, and audit-ready revenue output…</p>
      </a>
      <a class="related-content__card" href="/guides/netsuite-integration">
        <div class="related-content__media related-content__media--slate" aria-hidden="true"><span class="related-content__media-label">NetSuite</span></div>
        <div class="related-content__tags"><span class="related-content__tag">Guide</span><span class="related-content__tag">Integration</span></div>
        <h3 class="related-content__title">Connecting revzio to NetSuite</h3>
        <p class="related-content__excerpt">OAuth, field mapping, entity scope, and validating your first data sync…</p>
      </a>
      <a class="related-content__card" href="/blog/3-day-close-playbook">
        <div class="related-content__media related-content__media--navy" aria-hidden="true"><span class="related-content__media-label">3-day close</span></div>
        <div class="related-content__tags"><span class="related-content__tag">Article</span><span class="related-content__tag">Close</span></div>
        <h3 class="related-content__title">From 10-day close to 3 days: the CFO playbook</h3>
        <p class="related-content__excerpt">How continuous recon, journal prep, and clear ownership shrink month-end…</p>
      </a>
    </div>
  </div>
</section>
"""
    footer = """
<section class="cta-section" data-nav-theme="dark">
  <div class="container reveal">
    <h2>See this model on <em>your</em> Stripe + NetSuite shape.</h2>
    <p>Book a demo — we’ll map deferred bottlenecks to Orion agents, not a generic slide deck.</p>
    <div class="hero-ctas"><a href="/book-a-demo" class="btn btn-primary">Book a demo</a></div>
  </div>
</section>
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo" aria-label="revzio home"><img src="../assets/logos/revzio-icon.png" alt="" class="logo-mark" width="367" height="367" decoding="async" aria-hidden="true"><span class="logo-word">revzio</span></a>
        <p>The reconciled source of truth for modern finance teams.</p>
      </div>
      <div class="footer-col"><h5>Product</h5>
        <a href="/reconciliation">Reconciliation</a>
        <a href="/close-workflow">Close workflow</a>
        <a href="/agent-suite">Orion agents</a>
      </div>
      <div class="footer-col"><h5>Resources</h5>
        <a href="/blog">Blog</a>
        <a href="/guides">Guides</a>
        <a href="/glossary">Glossary</a>
      </div>
      <div class="footer-col"><h5>Company</h5>
        <a href="/about">About</a>
        <a href="/customers">Customers</a>
        <a href="/contact">Contact</a>
      </div>
    </div>
    <div class="footer-bottom"><div>© 2026 revzio. All rights reserved.</div></div>
  </div>
</footer>
<script src="../js/subpage.js"></script>
<script src="../js/nav-theme.js"></script>
<script src="../js/mobile-nav.js"></script>
<script src="../js/mega-menu.js"></script>
<script src="../js/nav.js"></script>
<script src="../js/animations.js"></script>
</body>
</html>
"""
    # Fix the incomplete HTML from content write
    html = content.replace("</body>\n</html>\n", "") + cite + related + footer
    # Add FAQ schema
    html = inject_json_ld(html, [faq_ld(faqs)])
    path.write_text(html, encoding="utf-8")
    print("wrote expert article")


def update_homepage_reviews() -> None:
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    html = ensure_css(html, nested=False)
    reviews = [
        {
            "@type": "Review",
            "author": {"@type": "Person", "name": "Mira Reyes"},
            "reviewBody": "We cut our close from twelve days to three. The team got their weekends back, and our auditors stopped asking where the spreadsheets were.",
        },
        {
            "@type": "Review",
            "author": {"@type": "Person", "name": "James Okonkwo"},
            "reviewBody": "Every variance comes with context your reviewers can trust. One reconciled source of truth across billing, ERP, and CRM.",
        },
        {
            "@type": "Review",
            "author": {"@type": "Person", "name": "Sarah Chen"},
            "reviewBody": "The close checklist finally lives in one place. Sign-offs happen in the tool, not over email threads at midnight.",
        },
    ]
    # Enhance SoftwareApplication ld+json with review — replace existing SoftwareApplication block
    soft = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Revzio",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "url": f"{SITE}/",
        "publisher": {
            "@type": "Organization",
            "name": "Revzio",
            "legalName": "Revzio Pte. Ltd.",
        },
        "review": reviews,
    }
    html = re.sub(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"SoftwareApplication".*?</script>\s*',
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = inject_json_ld(html, [soft])
    # Home FAQ — expert lane
    home_faqs = [
        (
            "What is Revzio?",
            "Revzio is AI financial close software. Orion agents prepare reconciliations, journals, AP/AR work, and close checklists continuously so finance teams review exceptions and sign off with an audit trail.",
        ),
        (
            "Who is Revzio for?",
            "Controllers, CFOs, and finance ops teams — especially SaaS and multi-entity companies drowning in spreadsheet recon and month-end fire drills.",
        ),
        (
            "How is Revzio different from a generic AI writing tool for accountants?",
            "Revzio agents work on transaction matching, journal prep, and close workflow with policy gates and immutable evidence. It is not a chatbot that drafts emails; it prepares the close work humans approve.",
        ),
    ]
    block = cite_block(
        h2="Clear answers about Revzio (built to be cited)",
        lead="One fact per line. This is the packaging answer engines prefer — same expertise, easier to lift.",
        pull="Revzio’s lane is financial close: reconciliation, journals, AP/AR, revenue validation, and audit-ready continuous close — not generic productivity tips.",
        facts=[
            "Orion agents prepare close work continuously; humans keep approvals and materiality.",
            "Evidence of matches, overrides, and sign-offs lives in product for audit.",
            "Teams typically pilot one entity and one workflow before expanding.",
            "We stay in the finance close neighborhood — depth over random topic sprawl.",
        ],
        table=None,
        faqs=home_faqs,
        review_ask=True,
    )
    html = insert_before_cta(html, block)
    html = inject_json_ld(html, [faq_ld(home_faqs)])
    path.write_text(html, encoding="utf-8")
    print("homepage updated")


def update_blog_index_and_sitemap() -> None:
    blog = ROOT / "blog.html"
    if blog.exists():
        html = blog.read_text(encoding="utf-8")
        card = """
      <a class="post-card" href="/blog/saas-stripe-netsuite-continuous-close" style="text-decoration:none; color:inherit;">
        <span class="post-tag">EXPERT CLOSE CLOSE</span>
        <div class="post-title">Stripe + NetSuite continuous close when deferred still takes two days</div>
        <div class="post-meta">Revzio Editorial · Oct 2026 · 9 min</div>
        <span class="post-link">Read →</span>
      </a>
"""
        if "saas-stripe-netsuite-continuous-close" not in html:
            html = html.replace(
                '<div class="cards grid-6 reveal-on-scroll"',
                card + '\n    <div class="cards grid-6 reveal-on-scroll"',
                1,
            )
            # actually insert inside the grid after opening
            html = blog.read_text(encoding="utf-8")
            html = html.replace(
                '<div class="cards grid-6 reveal-on-scroll" style="grid-template-columns: repeat(3, 1fr);">\n',
                '<div class="cards grid-6 reveal-on-scroll" style="grid-template-columns: repeat(3, 1fr);">\n'
                + card,
                1,
            )
            blog.write_text(html, encoding="utf-8")
            print("blog index updated")

    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    loc = "https://www.revzio.ai/blog/saas-stripe-netsuite-continuous-close"
    if loc not in text:
        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-10-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
"""
        text = text.replace("</urlset>", entry + "</urlset>")
        sm.write_text(text, encoding="utf-8")
        print("sitemap updated")


def tighten_lane_copy() -> None:
    """Tip 3: keep about/resources language in finance-close neighborhood."""
    about = ROOT / "about.html"
    if about.exists():
        html = about.read_text(encoding="utf-8")
        if "We don’t publish random productivity tips" not in html:
            note = """
<section class="cite-section" data-nav-theme="dark">
  <div class="container reveal">
    <h2>Our lane</h2>
    <p class="cite-lead">Answer engines trust sites that own a neighborhood. Ours is financial close — reconciliation, journals, AP/AR, revenue validation, controls, and continuous close for finance teams.</p>
    <ul class="cite-facts">
      <li>We write about close operations, audit trails, and Orion agents — not generic AI hype.</li>
      <li>Depth on close topics beats one-off posts about hiring, taxes, or unrelated productivity.</li>
      <li>If a question isn’t about getting books closed cleanly, it’s outside our neighborhood.</li>
    </ul>
  </div>
</section>
"""
            html = ensure_css(html, nested=False)
            html = insert_before_cta(html, note)
            about.write_text(html, encoding="utf-8")
            print("about lane note")


def main() -> None:
    write_expert_article()
    process_pages()
    process_guides()
    process_blogs()
    update_homepage_reviews()
    update_blog_index_and_sitemap()
    tighten_lane_copy()
    print("done")


if __name__ == "__main__":
    main()
