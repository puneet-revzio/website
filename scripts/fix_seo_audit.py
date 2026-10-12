#!/usr/bin/env python3
"""Generate guides, agent landings, expand thin pages, fix alts/authors/interlinks/reveal."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER = """
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo" aria-label="revzio home"><img src="{asset_prefix}assets/logos/revzio-icon.png" alt="" class="logo-mark" width="367" height="367" decoding="async" aria-hidden="true"><span class="logo-word">revzio</span></a>
        <p>The reconciled source of truth for modern finance teams.</p>
      </div>
      <div class="footer-col"><h5>Product</h5>
        <a href="/reconciliation">Reconciliation</a>
        <a href="/close-workflow">Close workflow</a>
        <a href="/agent-suite">Orion agents</a>
        <a href="/integrations">Integrations</a>
      </div>
      <div class="footer-col"><h5>Company</h5>
        <a href="/about">About</a>
        <a href="/customers">Customers</a>
        <a href="/careers">Careers</a>
        <a href="/contact">Contact</a>
      </div>
      <div class="footer-col"><h5>Resources</h5>
        <a href="/blog">Blog</a>
        <a href="/guides">Guides</a>
        <a href="/glossary">Glossary</a>
        <a href="/changelog">Changelog</a>
      </div>
      <div class="footer-col"><h5>Legal</h5>
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
        <a href="/security">Security</a>
        <a href="/dpa">DPA</a>
      </div>
    </div>
    <div class="footer-bottom"><div>© 2026 revzio. All rights reserved.</div></div>
  </div>
</footer>
"""

SCRIPTS = """
  <script src="{asset_prefix}js/subpage.js"></script>
  <script src="{asset_prefix}js/nav-theme.js"></script>
  <script src="{asset_prefix}js/mobile-nav.js"></script>
  <script src="{asset_prefix}js/mega-menu.js"></script>
  <script src="{asset_prefix}js/nav.js"></script>
  <script src="{asset_prefix}js/animations.js"></script>
"""

HEAD_COMMON = """<!DOCTYPE html>
<html lang="en">
<head>
<script src="/js/analytics.js"></script>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://www.revzio.ai/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://www.revzio.ai/{path}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.revzio.ai/assets/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://www.revzio.ai/assets/og-default.png">
<link rel="icon" type="image/png" sizes="32x32" href="{asset_prefix}assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{asset_prefix}assets/favicon/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{asset_prefix}assets/favicon/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset_prefix}style.css">
<link rel="stylesheet" href="{asset_prefix}css/brand.css">
<link rel="stylesheet" href="{asset_prefix}css/subpage.css">
<link rel="stylesheet" href="{asset_prefix}css/mega-menu.css">
<link rel="stylesheet" href="{asset_prefix}css/nav-theme.css">
<link rel="stylesheet" href="{asset_prefix}css/responsive.css">
<link rel="stylesheet" href="{asset_prefix}css/dark-global.css">
<link rel="stylesheet" href="{asset_prefix}css/cta-band.css">
<style>
  .article-hero {{
    padding: 120px 0 56px;
    background: var(--hero-bg);
    background-image:
      radial-gradient(ellipse at 12% -8%, rgba(90, 150, 210, 0.18), transparent 55%),
      radial-gradient(ellipse at 88% 12%, rgba(127, 207, 170, 0.12), transparent 52%),
      linear-gradient(180deg, var(--hero-bg) 70%, var(--hero-deep) 100%);
  }}
  .article-meta {{ color: rgba(250,250,247,0.55); font-size: 13.5px; margin-top: 10px; }}
  .tag-pill {{
    display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px;
    border-radius: 999px; border: 1px solid rgba(127,207,170,0.22);
    background: rgba(127,207,170,0.12); color: #7fcfaa; font-weight: 800;
    letter-spacing: 0.10em; text-transform: uppercase; font-size: 12px;
    width: fit-content; margin-bottom: 18px;
  }}
  .prose {{ max-width: 860px; margin: 0 auto; }}
  .prose p {{ margin: 14px 0; }}
  .prose h2 {{ margin-top: 34px; }}
  .prose ul {{ margin: 12px 0 12px 1.2em; }}
  .prose li {{ margin: 6px 0; }}
  .prose a {{ color: var(--accent); }}
  .backlink {{ color: #7fcfaa; text-decoration: none; font-weight: 750; }}
  .backlink:hover {{ color: #fafaf7; }}
  .related-box {{
    margin: 36px 0 8px; padding: 20px 22px; border-radius: 16px;
    border: 1px solid rgba(15,107,78,0.18); background: rgba(15,107,78,0.04);
  }}
  .related-box h3 {{ margin: 0 0 10px; font-size: 16px; }}
  .related-box ul {{ margin: 0; padding-left: 1.1em; }}
  .related-box li {{ margin: 6px 0; }}
</style>
</head>
<body>
<nav></nav>
"""


def page_shell(path: str, title: str, description: str, tag: str, h1: str, meta: str, body: str, *, nested: bool = False) -> str:
    asset = "../" if nested else ""
    back = "/guides" if path.startswith("guides/") else "/agent-suite"
    back_label = "← All guides" if path.startswith("guides/") else "← Orion agent suite"
    return (
        HEAD_COMMON.format(title=title, description=description, path=path, asset_prefix=asset)
        + f"""
<header class="article-hero" data-nav-theme="dark">
  <div class="container">
    <a class="backlink reveal" href="{back}">{back_label}</a>
    <div class="tag-pill reveal" style="margin-top: 18px;">{tag}</div>
    <h1 class="hero-title reveal" style="max-width: 980px;">{h1}</h1>
    <div class="article-meta reveal">{meta}</div>
  </div>
</header>
<section class="bg-alt">
  <div class="container">
    <article class="prose reveal">
{body}
    </article>
  </div>
</section>
<section class="cta-section" data-nav-theme="dark">
  <div class="container reveal">
    <h2>See revzio with <em>your data</em>.</h2>
    <p>Book a 30-minute walkthrough on your billing and ERP stack.</p>
    <div class="hero-ctas"><a href="/book-a-demo" class="btn btn-primary">Book a demo</a></div>
  </div>
</section>
"""
        + FOOTER.format(asset_prefix=asset)
        + SCRIPTS.format(asset_prefix=asset)
        + "\n</body>\n</html>\n"
    )


GUIDES = [
    {
        "slug": "setup-reconciliation-agent",
        "title": "Setup Reconciliation Agent Guide | Revzio",
        "description": "Set up Revzio’s Reconciliation Agent in under an hour — connect bank feeds, configure match rules, and run your first automated reconciliation with audit trail.",
        "tag": "GETTING STARTED",
        "h1": "Setting up your first Reconciliation Agent",
        "body": """
      <p>This guide walks a controller or finance ops lead through the first productive hour with Orion’s <a href="/agent-suite-reconciliation">Reconciliation Agent</a>. By the end you will have sources connected, match policy set, and a first continuous run producing exceptions you can review in product.</p>
      <h2>Before you start</h2>
      <p>Have read access (or a service user) for at least one bank or processor feed and your ERP or subledger. Decide which entities and accounts are in scope for week one — start narrow (cash and one billing processor) so exception volume stays manageable while you tune rules.</p>
      <ul>
        <li>Confirm who can approve overrides and who owns unmatched items.</li>
        <li>List known timing differences (payout delays, FX, batch settlement) so they become policy, not noise.</li>
        <li>Skim the <a href="/blog/reconciliation-agent-deep-dive">Reconciliation Agent deep dive</a> if your team needs line-level context before go-live.</li>
      </ul>
      <h2>Step 1 — Connect sources</h2>
      <p>In Revzio, open Integrations and connect the bank/processor and ERP connectors for your pilot entity. Validate that recent transactions land with source IDs intact. If you use NetSuite, follow the field-mapping checks in the <a href="/guides/netsuite-integration">NetSuite integration guide</a>.</p>
      <h2>Step 2 — Configure matching rules</h2>
      <p>Start with high-confidence exact matches on amount + date window + reference. Add fuzzy rules only where your identifiers routinely diverge (for example remittance batch vs invoice). Set tolerances for cents and FX. Anything outside policy should route as an exception with explainability — see <a href="/blog/exception-explainability">exception explainability</a>.</p>
      <h2>Step 3 — Run the first reconciliation</h2>
      <p>Trigger a historical window (often 30–60 days) so the agent builds a baseline. Review auto-matched items sample for correctness, then work the exception queue. Assign owners and due dates so breaks do not pile up into month-end.</p>
      <h2>Step 4 — Sign-off and audit trail</h2>
      <p>Approve matches and overrides in product. Confirm each decision stores who, when, and why. That trail feeds SOX and external audit without a separate evidence hunt — covered further in <a href="/guides/audit-trail-soc2">audit trail and SOC 2 readiness</a>.</p>
      <h2>What “done” looks like after week one</h2>
      <p>Daily matching is running, exception owners are clear, and your team is resolving breaks while context is fresh. Next, expand accounts and tighten auto-match rates. Pair with <a href="/reconciliation">continuous reconciliation</a> and the <a href="/guides/3-day-close-guide">3-day close guide</a> when you are ready to pull prep into every day of the month.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/agent-suite-reconciliation">Reconciliation Agent overview</a></li>
          <li><a href="/blog/manual-recon-cost">The cost of manual reconciliation</a></li>
          <li><a href="/integrations">Integrations</a></li>
        </ul>
      </div>
""",
    },
    {
        "slug": "automate-journal-entries",
        "title": "Automate Journal Entries Guide | Revzio",
        "description": "Configure Revzio’s Journal Entry Agent end-to-end — accrual logic, chart-of-accounts mapping, ERP posting, and reviewer gates that keep journals audit-ready.",
        "tag": "AGENT SETUP",
        "h1": "Automating journal entries end-to-end",
        "body": """
      <p>Manual journal construction from exports is one of the largest close bottlenecks. Orion’s <a href="/agent-suite-journal-entry">Journal Entry Agent</a> generates entries from source data with validations and evidence so your team reviews and posts instead of rebuilding spreadsheets.</p>
      <h2>Map your chart of accounts</h2>
      <p>Define how source events map to GL accounts, departments, and entities. Keep a short pilot set (payroll accruals, deferred revenue, bank fees) before expanding. Document materiality thresholds and accounts that must never auto-post.</p>
      <h2>Encode accrual and recognition logic</h2>
      <p>Translate existing spreadsheet logic into agent rules: prepaid amortization schedules, commission accruals, and period cutoffs. Pair with the <a href="/agent-suite-accruals">Accruals Agent</a> when schedules are recurring. For revenue-side validation, see the <a href="/guides/asc606-revenue-agent">ASC 606 revenue agent guide</a>.</p>
      <h2>Validations before ERP post</h2>
      <p>Require balance checks, duplicate detection, and period-open gates. Reviewers approve batches in product; rejected items stay linked to source transactions. This is the same human-in-the-loop model described in <a href="/blog/human-in-the-loop-finance">human-in-the-loop finance</a>.</p>
      <h2>Posting and evidence</h2>
      <p>Once approved, post to your ERP through the integration. Evidence — source extract, calculation, approver — stays attached for audit. Controllers should sample early cycles aggressively, then widen auto-post as confidence grows.</p>
      <h2>Roll into close cadence</h2>
      <p>JE prep belongs in the continuous close, not day five. Combine with <a href="/close-workflow">close workflow</a> checklists and the <a href="/guides/3-day-close-guide">3-day close guide</a> so journals are waiting for confirmation at month-end.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/record-to-report">Record-to-report automation</a></li>
          <li><a href="/blog/3-day-close-playbook">CFO 3-day close playbook</a></li>
          <li><a href="/agent-suite">Full Orion agent suite</a></li>
        </ul>
      </div>
""",
    },
    {
        "slug": "3-day-close-guide",
        "title": "3-Day Close with Orion Guide | Revzio",
        "description": "Week-by-week guide to running a 3-day close with Revzio Orion — continuous recon, prepared journals, checklist ownership, and controller sign-off.",
        "tag": "CLOSE MANAGEMENT",
        "h1": "Running a 3-day close with Orion",
        "body": """
      <p>A three-day close is not a sprint at month-end — it is the result of moving reconciliation and journal prep into every day. This guide is the implementation companion to the <a href="/blog/3-day-close-playbook">CFO 3-day close playbook</a>.</p>
      <h2>Week 0 — Baseline</h2>
      <p>Document current close calendar, top five blockers, and which tasks wait on “final” files. Instrument ownership with the <a href="/agent-suite-close-management">Close Management Agent</a> so status lives in product, not Slack.</p>
      <h2>Weeks 1–2 — Continuous recon</h2>
      <p>Stand up the <a href="/guides/setup-reconciliation-agent">Reconciliation Agent</a> on cash and billing. Route exceptions daily. Goal: enter month-end with most balances already explained. See also <a href="/blog/continuous-close-readiness">continuous close readiness</a>.</p>
      <h2>Weeks 3–4 — Journals and accruals</h2>
      <p>Automate recurring JEs and accruals. Reviewers work smaller batches mid-month. Use <a href="/guides/automate-journal-entries">journal entry automation</a> for mapping and gates.</p>
      <h2>Month-end — Confirmation, not discovery</h2>
      <p>Day 1: clear remaining exceptions and FX. Day 2: approve prepared journals and revenue validations. Day 3: checklist sign-off, variance narratives, and controller review. Audit evidence is already attached.</p>
      <h2>Governance</h2>
      <p>Keep materiality and auto-post policies written. Train reviewers on exception explainability. Align IT on access and logging via <a href="/guides/audit-trail-soc2">SOC 2 readiness</a>.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/continuous-close">Continuous close product</a></li>
          <li><a href="/blog/cutting-close-three-days">Cutting close by three days</a></li>
          <li><a href="/close-workflow">Close workflow software</a></li>
        </ul>
      </div>
""",
    },
    {
        "slug": "netsuite-integration",
        "title": "Connect Revzio to NetSuite | Revzio",
        "description": "Step-by-step Revzio–NetSuite integration: OAuth setup, field mapping, entity scope, and validating your first sync for continuous reconciliation and close.",
        "tag": "INTEGRATION",
        "h1": "Connecting Revzio to NetSuite",
        "body": """
      <p>NetSuite is a common system of record for Revzio customers. This guide covers a clean first sync so Orion agents can reconcile and prepare journals against trusted ERP data. Broader connector options live on <a href="/integrations">Integrations</a>.</p>
      <h2>OAuth and roles</h2>
      <p>Create a NetSuite integration role with least privilege for the records you need (transactions, accounts, subsidiaries). Authorize Revzio via OAuth. Store credentials in your secret manager; rotate on the same cadence as other finance systems.</p>
      <h2>Entity and period scope</h2>
      <p>Select pilot subsidiaries and open periods. Confirm timezone and period calendars match how finance closes. Multi-entity rollups should preserve local currency and local rules.</p>
      <h2>Field mapping</h2>
      <p>Map external IDs, memo fields, and custom segments used in your match keys. Document which NetSuite fields are authoritative for amount, date, and counterparty. Mis-mapped references are the #1 cause of false exceptions in week one.</p>
      <h2>Validate the first sync</h2>
      <p>Compare record counts and sample line items against NetSuite UI or saved searches. Run a short reconciliation window with the <a href="/guides/setup-reconciliation-agent">Reconciliation Agent setup guide</a>. Investigate gaps before enabling auto-post of journals.</p>
      <h2>Ongoing operations</h2>
      <p>Monitor sync health, schema drift, and permission changes after NetSuite upgrades. Pair with <a href="/data-ingestion">data ingestion</a> practices so bank and billing feeds stay aligned with ERP truth.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/agent-suite">Orion agents</a></li>
          <li><a href="/security">Security</a></li>
          <li><a href="/book-a-demo">Book a demo</a></li>
        </ul>
      </div>
""",
    },
    {
        "slug": "asc606-revenue-agent",
        "title": "ASC 606 Revenue Agent Guide | Revzio",
        "description": "Configure Revzio’s Revenue Validation Agent for ASC 606 — recognition rules, contract modifications, billing-to-ERP checks, and audit-ready revenue output.",
        "tag": "COMPLIANCE",
        "h1": "ASC 606 compliance with the Revenue Validation Agent",
        "body": """
      <p>ASC 606 failures rarely show up as a single wrong total — they show up as billing, contract, and ERP events that diverge. Orion’s <a href="/agent-suite-revenue-validation">Revenue Validation Agent</a> checks recognition against policy and flags gaps before audit.</p>
      <h2>Encode recognition rules</h2>
      <p>Capture performance obligations, allocation methods, and timing for your main products. Start with standard SaaS subscriptions, then add usage, professional services, and multi-element arrangements. The <a href="/blog/revenue-integrity-playbook">revenue integrity playbook</a> is a useful controller checklist.</p>
      <h2>Contract modifications</h2>
      <p>Upgrades, credits, and mid-term changes create the most painful deferred revenue breaks. Configure the agent to treat modification events as first-class inputs and to explain resulting schedule changes — not just the residual variance.</p>
      <h2>Billing vs ERP validation</h2>
      <p>Continuously compare billing system invoices and schedules to ERP postings. Tie exceptions to contract IDs so revenue accountants investigate once. Pair with continuous <a href="/reconciliation">reconciliation</a> on cash and deferred accounts.</p>
      <h2>Audit-ready output</h2>
      <p>Export recognition schedules, exception narratives, and approval history. Keep human approval gates on material judgments as described in <a href="/blog/human-in-the-loop-finance">human-in-the-loop finance</a>.</p>
      <h2>Scale without spreadsheet debt</h2>
      <p>When ARR and contract volume climb, spreadsheet recognition breaks. See <a href="/blog/revenue-recognition-scale">revenue recognition at scale</a> and expand agent coverage entity by entity.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/industry-saas">Close for SaaS</a></li>
          <li><a href="/guides/automate-journal-entries">Automating journal entries</a></li>
          <li><a href="/controls-and-audit-trails">Controls and audit trails</a></li>
        </ul>
      </div>
""",
    },
    {
        "slug": "audit-trail-soc2",
        "title": "Audit Trail & SOC 2 Guide | Revzio",
        "description": "Configure Revzio audit trails for SOC 2 readiness — RBAC, immutable logs, reviewer sign-off, and evidence workflows that satisfy auditors year-round.",
        "tag": "SECURITY",
        "h1": "Audit trail setup and SOC 2 readiness",
        "body": """
      <p>Auditors ask for evidence of who changed what, when, and why. Revzio captures matches, journals, overrides, and approvals in product so you are not reconstructing history from email. Read <a href="/blog/soc2-and-your-close-stack">SOC 2 and your close stack</a> for the broader framing.</p>
      <h2>RBAC</h2>
      <p>Separate preparers, reviewers, and administrators. Limit who can change match policy or auto-post thresholds. Review access quarterly with IT — same cadence as other financial systems. Details on platform posture: <a href="/security">Security</a> and <a href="/trust-center">Trust Center</a>.</p>
      <h2>Immutable logging</h2>
      <p>Ensure every automated and manual action writes an immutable event: match created, exception resolved, JE approved, checklist signed. Prefer system time and user identity from SSO.</p>
      <h2>Reviewer sign-off workflows</h2>
      <p>Use <a href="/close-workflow">close workflow</a> and the <a href="/agent-suite-close-management">Close Management Agent</a> so sign-offs happen where work happens. Attach recon packs and JE evidence to tasks automatically.</p>
      <h2>Evidence packs for auditors</h2>
      <p>Practice exporting a sample period: exceptions, resolutions, journals, and checklist history. Run this dry-run before year-end. Pair with <a href="/controls-and-audit-trails">controls and audit trails</a> product capabilities.</p>
      <h2>Continuous readiness</h2>
      <p>SOC 2 is not a month-end project. Continuous close with governed agents means evidence accumulates daily — which is exactly what assessors prefer over a frantic binder at lunchtime.</p>
      <div class="related-box">
        <h3>Related</h3>
        <ul>
          <li><a href="/dpa">Data Processing Agreement</a></li>
          <li><a href="/guides/setup-reconciliation-agent">Reconciliation Agent setup</a></li>
          <li><a href="/book-a-demo">Book a demo</a></li>
        </ul>
      </div>
""",
    },
]

AGENTS = [
    (
        "agent-suite-reconciliation",
        "AI Reconciliation Agent | Revzio",
        "Revzio’s Reconciliation Agent matches bank, billing, and ERP transactions continuously — explainable exceptions and audit trails for faster month-end close.",
        "ORION AGENT",
        "Reconciliation Agent",
        "reconciliation",
        """
      <p>The Reconciliation Agent is Orion’s line-level matching engine. It ingests bank, processor, billing, and ERP events as they land, normalizes them, and matches one-to-one, one-to-many, and many-to-many relationships under your policy.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Continuous matching instead of month-end batch exports</li>
        <li>Exception queues with summaries, likely causes, and next steps</li>
        <li>Overrides and approvals with immutable audit history</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Use it as the foundation of <a href="/reconciliation">account reconciliation</a> and <a href="/continuous-close">continuous close</a>. Setup details: <a href="/guides/setup-reconciliation-agent">setup guide</a>. Deep dive: <a href="/blog/reconciliation-agent-deep-dive">95% auto-match story</a>.</p>
      <p>See all agents on the <a href="/agent-suite#reconciliation">Orion agent suite</a>.</p>
""",
    ),
    (
        "agent-suite-journal-entry",
        "AI Journal Entry Agent | Revzio",
        "Revzio’s Journal Entry Agent generates validated journals from source data — mappings, gates, and ERP posting so accountants review instead of rebuild.",
        "ORION AGENT",
        "Journal Entry Agent",
        "journal-entry",
        """
      <p>The Journal Entry Agent turns source events into balanced, validated journals with evidence. Controllers set mapping and materiality; the agent prepares entries continuously for review.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Recurring and event-driven journal generation</li>
        <li>Balance, duplicate, and period validations</li>
        <li>Reviewer approval before ERP post</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Core to <a href="/record-to-report">record-to-report</a>. Implementation: <a href="/guides/automate-journal-entries">automating journal entries</a>. Suite context: <a href="/agent-suite#journal-entry">agent suite</a>.</p>
""",
    ),
    (
        "agent-suite-ap",
        "AI Accounts Payable Agent | Revzio",
        "Revzio’s AP Agent extracts invoices, runs 3-way match, and routes approvals — so payables teams clear exceptions instead of keying data every day.",
        "ORION AGENT",
        "Accounts Payable Agent",
        "accounts-payable",
        """
      <p>The AP Agent fetches invoices, extracts line items, performs 3-way match, and routes payments for approval under your controls.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Invoice capture and line extraction</li>
        <li>PO / receipt / invoice matching</li>
        <li>Exception routing and approval trails</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Supports <a href="/procure-to-pay">procure-to-pay</a>. Read <a href="/blog/3-way-match-ai">AI 3-way match</a>. Full suite: <a href="/agent-suite#accounts-payable">AP on agent suite</a>.</p>
""",
    ),
    (
        "agent-suite-ar",
        "AI Accounts Receivable Agent | Revzio",
        "Revzio’s AR Agent automates cash application and collections priority — apply payments faster, reduce DSO, and keep receivables continuous through close.",
        "ORION AGENT",
        "Accounts Receivable Agent",
        "accounts-receivable",
        """
      <p>The AR Agent applies cash, ranks collection priority, and triggers follow-ups so receivables stay clean without spreadsheet remittance matching.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Cash application against open invoices</li>
        <li>Prioritized collections worklists</li>
        <li>Exception handling for short-pays and unapplied cash</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Powers <a href="/order-to-cash">order-to-cash</a> automation. See <a href="/agent-suite#accounts-receivable">AR on the agent suite</a>.</p>
""",
    ),
    (
        "agent-suite-accruals",
        "AI Accruals Agent | Revzio",
        "Revzio’s Accruals Agent calculates prepaid amortization and period-end accruals from source data — schedules, postings, and evidence auditors can follow.",
        "ORION AGENT",
        "Accruals Agent",
        "accruals",
        """
      <p>The Accruals Agent maintains schedules for prepaids, commissions, and other period adjustments, then prepares postings with a clear trail.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Schedule calculation from contracts and invoices</li>
        <li>Period-end accrual proposals</li>
        <li>Linked evidence for every posting</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Works with the <a href="/agent-suite-journal-entry">Journal Entry Agent</a> and <a href="/close-workflow">close workflow</a>. Suite: <a href="/agent-suite#accruals">Accruals Agent</a>.</p>
""",
    ),
    (
        "agent-suite-revenue-validation",
        "AI Revenue Validation Agent | Revzio",
        "Revzio’s Revenue Validation Agent checks billing and ERP against ASC 606 rules — flag contract and recognition gaps before they hit your next audit.",
        "ORION AGENT",
        "Revenue Validation Agent",
        "revenue-validation",
        """
      <p>The Revenue Validation Agent validates revenue events against recognition policy and highlights billing-to-ERP gaps early.</p>
      <h2>What it automates</h2>
      <ul>
        <li>ASC 606 rule checks on revenue events</li>
        <li>Contract modification impact detection</li>
        <li>Audit-ready schedules and exception narratives</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Guide: <a href="/guides/asc606-revenue-agent">ASC 606 setup</a>. Playbook: <a href="/blog/revenue-integrity-playbook">revenue integrity</a>. Suite: <a href="/agent-suite#revenue-validation">Revenue Validation</a>.</p>
""",
    ),
    (
        "agent-suite-close-management",
        "AI Close Management Agent | Revzio",
        "Revzio’s Close Management Agent orchestrates month-end — checklists, owners, dependencies, approvals, and variance status in one audit-ready workflow.",
        "ORION AGENT",
        "Close Management Agent",
        "close-management",
        """
      <p>The Close Management Agent is the control tower for month-end: tasks, owners, dependencies, and sign-offs with evidence attached.</p>
      <h2>What it automates</h2>
      <ul>
        <li>Entity and cycle checklists</li>
        <li>Bottleneck visibility and escalations</li>
        <li>In-product approvals linked to recon and journals</li>
      </ul>
      <h2>Where it fits</h2>
      <p>Use with <a href="/close-workflow">close workflow</a> and the <a href="/guides/3-day-close-guide">3-day close guide</a>. Suite: <a href="/agent-suite#close-management">Close Management</a>.</p>
""",
    ),
]


def write_guides() -> None:
    (ROOT / "guides").mkdir(exist_ok=True)
    for g in GUIDES:
        html = page_shell(
            f"guides/{g['slug']}",
            g["title"],
            g["description"],
            g["tag"],
            g["h1"],
            "Revzio Editorial · Guide · 8–12 min read",
            g["body"],
            nested=True,
        )
        (ROOT / "guides" / f"{g['slug']}.html").write_text(html, encoding="utf-8")
        print("wrote guides/" + g["slug"])


def write_agents() -> None:
    for slug, title, desc, tag, h1, _anchor, body in AGENTS:
        html = page_shell(slug, title, desc, tag, h1, "Revzio Editorial · Orion Agent", body)
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")
        print("wrote " + slug)


RECON_EXTRA = """
<section>
  <div class="container">
    <div class="reveal">
      <div class="section-eyebrow">Why it matters</div>
      <h2>Month-end recon is too <em>late</em></h2>
      <p class="section-sub">When matching waits for “final” files, exceptions surface after context is gone — and close slips a day at a time.</p>
    </div>
    <div class="cards reveal">
      <div class="card">
        <div class="card-icon">◎</div>
        <h4>Line-level truth</h4>
        <p>Totals can tie while duplicates and misclassifications hide underneath. Revzio matches at the transaction level across bank, billing, and GL.</p>
      </div>
      <div class="card">
        <div class="card-icon">▣</div>
        <h4>Explainable breaks</h4>
        <p>Every exception includes a summary, likely cause, and suggested next step — so reviewers resolve instead of reverse-engineer. See <a href="/blog/exception-explainability">exception explainability</a>.</p>
      </div>
      <div class="card">
        <div class="card-icon">◑</div>
        <h4>Audit-ready by default</h4>
        <p>Matches, overrides, and approvals stay in product with who, when, and why — ready for SOX sampling and external audit.</p>
      </div>
    </div>
  </div>
</section>
<section class="bg-alt">
  <div class="container">
    <div class="reveal">
      <div class="section-eyebrow">How teams deploy</div>
      <h2>From pilot entity to <em>continuous</em> recon</h2>
      <p class="section-sub">Most teams start with cash and one processor, then expand accounts once exception owners and match policy are proven.</p>
    </div>
    <div class="steps reveal">
      <div class="step">
        <div class="step-num">01</div>
        <h4>Connect &amp; scope</h4>
        <p>Wire ERP and bank feeds for one entity. Follow the <a href="/guides/setup-reconciliation-agent">setup guide</a> to configure rules in under an hour.</p>
      </div>
      <div class="step">
        <div class="step-num">02</div>
        <h4>Match daily</h4>
        <p>Let the <a href="/agent-suite-reconciliation">Reconciliation Agent</a> clear high-confidence items continuously and route only true breaks.</p>
      </div>
      <div class="step">
        <div class="step-num">03</div>
        <h4>Fold into close</h4>
        <p>Attach recon status to <a href="/close-workflow">close workflow</a> tasks so month-end is confirmation, not discovery.</p>
      </div>
    </div>
    <p class="reveal" style="margin-top:28px;max-width:720px;color:var(--ink-muted);">Related reading: <a href="/blog/manual-recon-cost">cost of manual recon</a> · <a href="/blog/reconciliation-agent-deep-dive">agent deep dive</a> · <a href="/recon-automation">recon automation</a></p>
  </div>
</section>
"""

CLOSE_EXTRA = """
<section>
  <div class="container">
    <div class="reveal">
      <div class="section-eyebrow">How the close runs</div>
      <h2>Prep every day. Confirm at <em>month-end</em>.</h2>
      <p class="section-sub">Orion agents prepare reconciliations and journals continuously; close workflow keeps humans focused on exceptions, ownership, and sign-off.</p>
    </div>
    <div class="steps reveal">
      <div class="step">
        <div class="step-num">Day −10 to −1</div>
        <h4>Continuous prep</h4>
        <p><a href="/agent-suite-reconciliation">Recon</a> and <a href="/agent-suite-journal-entry">journal</a> agents clear work mid-month. Exceptions are owned while context is fresh.</p>
      </div>
      <div class="step">
        <div class="step-num">Days 1–2</div>
        <h4>Exception &amp; JE review</h4>
        <p>Clear remaining breaks, approve prepared journals and accruals, validate revenue where needed with the <a href="/agent-suite-revenue-validation">Revenue Validation Agent</a>.</p>
      </div>
      <div class="step">
        <div class="step-num">Day 3</div>
        <h4>Controller sign-off</h4>
        <p>The <a href="/agent-suite-close-management">Close Management Agent</a> shows checklist status, blockers, and attached evidence for final approval.</p>
      </div>
    </div>
  </div>
</section>
<section class="bg-alt">
  <div class="container">
    <div class="reveal">
      <div class="section-eyebrow">Built for controllers</div>
      <h2>Visibility without <em>status theater</em></h2>
      <p class="section-sub">Replace spreadsheet trackers with live task state, dependencies, and audit-ready approvals.</p>
    </div>
    <div class="cards reveal">
      <div class="card">
        <h4>Dependencies that matter</h4>
        <p>Blockers surface early — not when someone asks “is deferred done?” in Slack on day four.</p>
      </div>
      <div class="card">
        <h4>Evidence attached</h4>
        <p>Sign-offs link to recon packs and journals. Auditors follow the same trail as your team. See <a href="/guides/audit-trail-soc2">audit trail setup</a>.</p>
      </div>
      <div class="card">
        <h4>Path to 3-day close</h4>
        <p>Follow the <a href="/guides/3-day-close-guide">3-day close guide</a> and <a href="/blog/3-day-close-playbook">CFO playbook</a> to compress prep into the month.</p>
      </div>
    </div>
    <p class="reveal" style="margin-top:28px;max-width:720px;color:var(--ink-muted);">Also explore <a href="/continuous-close">continuous close</a> and <a href="/automated-workflows">automated workflows</a>.</p>
  </div>
</section>
"""

EXCEPTION_BODY = """
    <p class="blog-meta">April 18, 2026 · Revzio Editorial · 8 min read</p>
    <h2>The problem with raw exceptions</h2>
    <p>A $42,000 variance with no narrative forces your team into detective mode. Export two systems, VLOOKUP until something looks familiar, ping three Slack channels, and hope the owner still remembers the deal. That loop is why closes slip — not because accountants lack skill, but because the system hands them noise instead of work.</p>
    <p>Raw exceptions also age badly. A timing difference that was obvious on Tuesday is opaque by the following Monday. Continuous close only works if breaks arrive with enough context to act the same day.</p>
    <h2>What explainability means in revzio</h2>
    <p>Explainability layers context onto every break: a short summary, likely causes (timing, FX, partial period, mapping change, duplicate), suggested checks, and links to supporting transactions. Reviewers approve or override in product — the trail stays intact for audit.</p>
    <p>This is not a black-box “AI said so.” Controllers still set match policy and materiality. The agent prepares the investigation; humans keep judgment. That model is the same <a href="/blog/human-in-the-loop-finance">human-in-the-loop</a> approach across Orion.</p>
    <h2>How it shows up in the workflow</h2>
    <p>Inside the <a href="/agent-suite-reconciliation">Reconciliation Agent</a>, unmatched or tolerance-break items land in an exception queue with ownership and due dates. From there, reviewers can:</p>
    <ul>
      <li>Accept the suggested resolution when evidence matches policy</li>
      <li>Override with a reason code that becomes part of the immutable log</li>
      <li>Escalate when the break implies a process or data issue upstream</li>
    </ul>
    <p>Those decisions feed <a href="/close-workflow">close workflow</a> status so controllers see whether recon is truly ready — not just “mostly tied.”</p>
    <h2>Why this shortens close</h2>
    <p>Teams that resolve exceptions mid-month stop discovering them on day five. Deferred revenue, payout batches, and multi-entity FX stop being fire drills. Pair explainability with the <a href="/guides/setup-reconciliation-agent">Reconciliation Agent setup guide</a> and the <a href="/guides/3-day-close-guide">3-day close guide</a> to move prep into every day of the cycle.</p>
    <h2>What to look for in a demo</h2>
    <p>Ask to see a real break: summary text, linked source lines, and the approval trail after an override. Compare that to a CSV of unmatched amounts. If your auditors would rather sample the former, you are looking at the right layer of product depth — also covered in our <a href="/blog/reconciliation-agent-deep-dive">reconciliation deep dive</a> and <a href="/reconciliation">reconciliation product page</a>.</p>
    <div class="blog-article-cta">
      <h3>See continuous close in action</h3>
      <p>Book a 30-minute demo with your billing and ERP data.</p>
      <a href="/book-a-demo" class="btn-primary">Book a demo</a>
    </div>
    <aside class="related-box" style="margin-top:32px;">
      <h3>Keep reading</h3>
      <ul>
        <li><a href="/blog/manual-recon-cost">The hidden cost of manual reconciliation</a></li>
        <li><a href="/blog/continuous-close-readiness">Continuous close readiness</a></li>
        <li><a href="/blog/cutting-close-three-days">Cutting close by three days</a></li>
      </ul>
    </aside>
"""


def expand_thin_pages() -> None:
    recon = ROOT / "reconciliation.html"
    html = recon.read_text(encoding="utf-8")
    if "Month-end recon is too" not in html:
        html = html.replace(
            '<section class="cta-section" data-nav-theme="dark">',
            RECON_EXTRA + '\n<section class="cta-section" data-nav-theme="dark">',
            1,
        )
        recon.write_text(html, encoding="utf-8")
        print("expanded reconciliation")

    close = ROOT / "close-workflow.html"
    html = close.read_text(encoding="utf-8")
    if "Prep every day. Confirm at" not in html:
        html = html.replace(
            '<section class="cta-section" data-nav-theme="dark">',
            CLOSE_EXTRA + '\n<section class="cta-section" data-nav-theme="dark">',
            1,
        )
        close.write_text(html, encoding="utf-8")
        print("expanded close-workflow")

    ex = ROOT / "blog/exception-explainability.html"
    html = ex.read_text(encoding="utf-8")
    html = re.sub(
        r'<p class="blog-meta">.*?</div>\s*</article>',
        EXCEPTION_BODY + "\n  </div>\n</article>",
        html,
        count=1,
        flags=re.S,
    )
    # Ensure related-box style available
    if ".related-box" not in html:
        html = html.replace(
            "</head>",
            "<style>.related-box{margin:36px 0 8px;padding:20px 22px;border-radius:16px;border:1px solid rgba(15,107,78,0.18);background:rgba(15,107,78,0.04)}.related-box h3{margin:0 0 10px;font-size:16px}.related-box ul{margin:0;padding-left:1.1em}.related-box li{margin:6px 0}.blog-article ul{margin:12px 0 12px 1.2em}.blog-article a{color:var(--accent)}</style>\n</head>",
            1,
        )
    ex.write_text(html, encoding="utf-8")
    print("expanded exception-explainability")


def fix_alts() -> None:
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")
    reps = [
        ('src="assets/logos/coindcx.svg" alt=""', 'src="assets/logos/coindcx.svg" alt="CoinDCX"'),
        ('src="assets/logos/pixis.svg" alt=""', 'src="assets/logos/pixis.svg" alt="Pixis"'),
        ('src="assets/logos/faclon.svg" alt=""', 'src="assets/logos/faclon.svg" alt="Faclon"'),
        (
            'src="https://i.pravatar.cc/104?img=12" alt=""',
            'src="https://i.pravatar.cc/104?img=12" alt="Tingting Fang"',
        ),
        (
            'src="https://i.pravatar.cc/104?img=33" alt=""',
            'src="https://i.pravatar.cc/104?img=33" alt="David Rich"',
        ),
        (
            'src="https://i.pravatar.cc/104?img=45" alt=""',
            'src="https://i.pravatar.cc/104?img=45" alt="Mira Reyes"',
        ),
        (
            'src="https://i.pravatar.cc/104?img=68" alt=""',
            'src="https://i.pravatar.cc/104?img=68" alt="Devan Romano"',
        ),
        (
            'src="https://i.pravatar.cc/104?img=25" alt=""',
            'src="https://i.pravatar.cc/104?img=25" alt="James Okonkwo"',
        ),
        (
            'src="https://i.pravatar.cc/104?img=47" alt=""',
            'src="https://i.pravatar.cc/104?img=47" alt="Sarah Chen"',
        ),
    ]
    for a, b in reps:
        html = html.replace(a, b)
    # decorative logos: remove aria-hidden when we have real alts so names are announced once
    html = html.replace(
        'alt="CoinDCX" width="120" height="24" loading="lazy" decoding="async" aria-hidden="true"',
        'alt="CoinDCX" width="120" height="24" loading="lazy" decoding="async"',
    )
    html = html.replace(
        'alt="Pixis" width="118" height="24" loading="lazy" decoding="async" aria-hidden="true"',
        'alt="Pixis" width="118" height="24" loading="lazy" decoding="async"',
    )
    html = html.replace(
        'alt="Faclon" width="154" height="24" loading="lazy" decoding="async" aria-hidden="true"',
        'alt="Faclon" width="154" height="24" loading="lazy" decoding="async"',
    )
    index.write_text(html, encoding="utf-8")
    print("fixed index alts")


BLOG_RELATED = {
    "3-day-close-playbook": [
        ("/guides/3-day-close-guide", "3-day close implementation guide"),
        ("/close-workflow", "Close workflow product"),
        ("/blog/cutting-close-three-days", "Cutting close by three days"),
    ],
    "3-way-match-ai": [
        ("/agent-suite-ap", "Accounts Payable Agent"),
        ("/procure-to-pay", "Procure-to-pay automation"),
        ("/blog/human-in-the-loop-finance", "Human-in-the-loop finance"),
    ],
    "3-week-onboarding": [
        ("/guides/setup-reconciliation-agent", "Set up Reconciliation Agent"),
        ("/guides/netsuite-integration", "Connect NetSuite"),
        ("/how-it-works", "How Orion works"),
    ],
    "ai-agency-in-finance": [
        ("/agent-suite", "Orion agent suite"),
        ("/blog/human-in-the-loop-finance", "Human-in-the-loop finance"),
        ("/how-it-works", "How it works"),
    ],
    "continuous-close-readiness": [
        ("/continuous-close", "Continuous close product"),
        ("/reconciliation", "Reconciliation"),
        ("/blog/3-day-close-playbook", "3-day close playbook"),
    ],
    "cutting-close-three-days": [
        ("/guides/3-day-close-guide", "3-day close guide"),
        ("/blog/3-day-close-playbook", "CFO playbook"),
        ("/agent-suite-close-management", "Close Management Agent"),
    ],
    "human-in-the-loop-finance": [
        ("/controls-and-audit-trails", "Controls and audit trails"),
        ("/blog/ai-agency-in-finance", "AI agency in finance"),
        ("/security", "Security"),
    ],
    "manual-recon-cost": [
        ("/reconciliation", "Account reconciliation"),
        ("/agent-suite-reconciliation", "Reconciliation Agent"),
        ("/blog/reconciliation-agent-deep-dive", "Agent deep dive"),
    ],
    "reconciliation-agent-deep-dive": [
        ("/guides/setup-reconciliation-agent", "Setup guide"),
        ("/agent-suite-reconciliation", "Reconciliation Agent"),
        ("/blog/exception-explainability", "Exception explainability"),
    ],
    "revenue-integrity-playbook": [
        ("/guides/asc606-revenue-agent", "ASC 606 revenue agent guide"),
        ("/agent-suite-revenue-validation", "Revenue Validation Agent"),
        ("/industry-saas", "Close for SaaS"),
    ],
    "revenue-recognition-scale": [
        ("/blog/revenue-integrity-playbook", "Revenue integrity playbook"),
        ("/guides/asc606-revenue-agent", "ASC 606 guide"),
        ("/industry-saas", "SaaS close"),
    ],
    "soc2-and-your-close-stack": [
        ("/guides/audit-trail-soc2", "Audit trail & SOC 2 guide"),
        ("/trust-center", "Trust Center"),
        ("/security", "Security"),
    ],
}


def fix_blog_authors_and_links() -> None:
    related_css = (
        "<style>.related-box{margin:36px 0 8px;padding:20px 22px;border-radius:16px;"
        "border:1px solid rgba(15,107,78,0.18);background:rgba(15,107,78,0.04)}"
        ".related-box h3{margin:0 0 10px;font-size:16px}.related-box ul{margin:0;padding-left:1.1em}"
        ".related-box li{margin:6px 0}.prose a,.blog-article a{color:var(--accent)}</style>\n"
    )
    for file in sorted((ROOT / "blog").glob("*.html")):
        html = file.read_text(encoding="utf-8")
        html = html.replace("revzio Team", "Revzio Editorial")
        html = re.sub(
            r'(<p class="blog-meta">)([^<]*?)( · \d+ min read</p>)',
            lambda m: m.group(1)
            + m.group(2).replace("Revzio Editorial · ", "").replace(" · Revzio Editorial", "")
            + " · Revzio Editorial"
            + m.group(3)
            if "Revzio Editorial" not in m.group(2)
            else m.group(0),
            html,
            count=1,
        )
        # For blog-meta without author yet
        html = re.sub(
            r'<p class="blog-meta">([^<]*?)·\s*(\d+ min read)</p>',
            lambda m: m.group(0)
            if "Revzio Editorial" in m.group(1)
            else f'<p class="blog-meta">{m.group(1).rstrip()} · Revzio Editorial · {m.group(2)}</p>',
            html,
            count=1,
        )

        slug = file.stem
        links = BLOG_RELATED.get(slug)
        if links and "related-box" not in html:
            items = "\n".join(f'          <li><a href="{href}">{label}</a></li>' for href, label in links)
            box = f"""
      <aside class="related-box">
        <h3>Related reading</h3>
        <ul>
{items}
        </ul>
      </aside>
"""
            if "</article>" in html:
                # insert before closing article prose / before CTA section
                if '<div class="blog-article-cta">' in html:
                    html = html.replace('<div class="blog-article-cta">', box + '\n    <div class="blog-article-cta">', 1)
                elif "</article>" in html:
                    html = html.replace("</article>", box + "\n</article>", 1)
            if related_css not in html and ".related-box" not in html:
                html = html.replace("</head>", related_css + "</head>", 1)
        file.write_text(html, encoding="utf-8")
        print("blog fixed", slug)

    blog_index = ROOT / "blog.html"
    if blog_index.exists():
        t = blog_index.read_text(encoding="utf-8").replace("revzio Team", "Revzio Editorial")
        blog_index.write_text(t, encoding="utf-8")


def fix_reveal() -> None:
    sub = ROOT / "css/subpage.css"
    css = sub.read_text(encoding="utf-8")
    if "js .reveal:not(.in)" not in css:
        css = css.replace(
            """.reveal {
  opacity: 0.02;
  transform: translateY(16px);
  transition: opacity 0.55s ease, transform 0.55s ease;
}

.reveal.in {
  opacity: 1;
  transform: translateY(0);
}""",
            """.reveal {
  opacity: 1;
  transform: none;
  transition: opacity 0.55s ease, transform 0.55s ease;
}

html.js .reveal:not(.in) {
  opacity: 0.02;
  transform: translateY(16px);
}

.reveal.in {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  html.js .reveal:not(.in),
  html.js .reveal-on-scroll:not(.is-visible) {
    opacity: 1 !important;
    transform: none !important;
  }
}""",
        )
        sub.write_text(css, encoding="utf-8")
        print("fixed subpage reveal")

    orion = ROOT / "css/orion-agents.css"
    if orion.exists():
        o = orion.read_text(encoding="utf-8")
        if "html.js .agent-row.reveal:not(.in)" not in o:
            o = o.replace(
                """.agent-row.reveal {
  opacity: 0;""",
                """.agent-row.reveal {
  opacity: 1;""",
                1,
            )
            o = o.replace(
                """.agent-row.reveal.in {
""",
                """html.js .agent-row.reveal:not(.in) {
  opacity: 0;
}
.agent-row.reveal.in {
""",
                1,
            )
            orion.write_text(o, encoding="utf-8")
            print("fixed orion-agents reveal")

    anim = ROOT / "js/animations.js"
    js = anim.read_text(encoding="utf-8")
    if "documentElement.classList.add('js')" not in js:
        js = js.replace(
            "(function () {\n  function injectGlobalStyles() {",
            "(function () {\n  document.documentElement.classList.add('js');\n  function injectGlobalStyles() {",
            1,
        )
        # also make reveal-on-scroll visible by default unless js class
        js = js.replace(
            """.reveal-on-scroll {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.65s ease, transform 0.65s ease;
        will-change: opacity, transform;
      }""",
            """.reveal-on-scroll {
        opacity: 1;
        transform: none;
        transition: opacity 0.65s ease, transform 0.65s ease;
        will-change: opacity, transform;
      }
      html.js .reveal-on-scroll:not(.is-visible):not(.in):not(.visible) {
        opacity: 0;
        transform: translateY(20px);
      }""",
            1,
        )
        anim.write_text(js, encoding="utf-8")
        print("fixed animations.js js class")


def update_vercel() -> None:
    path = ROOT / "vercel.json"
    path.write_text(
        """{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    {
      "source": "/index.html",
      "destination": "/",
      "permanent": true
    },
    {
      "source": "/agent-reconciliation",
      "destination": "/agent-suite-reconciliation",
      "permanent": true
    },
    {
      "source": "/agent-journal-entry",
      "destination": "/agent-suite-journal-entry",
      "permanent": true
    },
    {
      "source": "/agent-ap",
      "destination": "/agent-suite-ap",
      "permanent": true
    },
    {
      "source": "/agent-ar",
      "destination": "/agent-suite-ar",
      "permanent": true
    },
    {
      "source": "/agent-accruals",
      "destination": "/agent-suite-accruals",
      "permanent": true
    },
    {
      "source": "/agent-revenue-validation",
      "destination": "/agent-suite-revenue-validation",
      "permanent": true
    },
    {
      "source": "/agent-close-management",
      "destination": "/agent-suite-close-management",
      "permanent": true
    }
  ]
}
""",
        encoding="utf-8",
    )
    print("updated vercel.json")


def update_agent_suite_links() -> None:
    f = ROOT / "agent-suite.html"
    html = f.read_text(encoding="utf-8")
    # Add “Learn more” links into each agent body if missing
    mapping = [
        ("id=\"reconciliation\"", "/agent-suite-reconciliation", "Reconciliation Agent page"),
        ("id=\"journal-entry\"", "/agent-suite-journal-entry", "Journal Entry Agent page"),
        ("id=\"accounts-payable\"", "/agent-suite-ap", "AP Agent page"),
        ("id=\"accounts-receivable\"", "/agent-suite-ar", "AR Agent page"),
        ("id=\"accruals\"", "/agent-suite-accruals", "Accruals Agent page"),
        ("id=\"revenue-validation\"", "/agent-suite-revenue-validation", "Revenue Validation Agent page"),
        ("id=\"close-management\"", "/agent-suite-close-management", "Close Management Agent page"),
    ]
    for anchor, href, label in mapping:
        if href in html:
            continue
        # insert after the agent paragraph inside that row
        pattern = rf'({anchor}[\s\S]*?<p>)(.*?)(</p>)'
        def repl(m, href=href, label=label):
            return m.group(1) + m.group(2) + m.group(3) + f'\n          <p><a href="{href}">Open {label} →</a></p>'
        new_html, n = re.subn(pattern, repl, html, count=1)
        if n:
            html = new_html
    f.write_text(html, encoding="utf-8")
    print("linked agent-suite to landings")


def main() -> None:
    write_guides()
    write_agents()
    expand_thin_pages()
    fix_alts()
    fix_blog_authors_and_links()
    fix_reveal()
    update_vercel()
    update_agent_suite_links()
    print("done")


if __name__ == "__main__":
    main()
