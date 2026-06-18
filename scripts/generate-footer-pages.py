#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER = """
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo"><span class="logo-dot"></span>revzio</a>
        <p>The reconciled source of truth for modern finance teams.</p>
      </div>
      <div class="footer-col">
        <h5>Product</h5>
        <a href="/reconciliation">Reconciliation</a>
        <a href="/close-workflow">Close workflow</a>
        <a href="/reporting">Reporting</a>
        <a href="/integrations">Integrations</a>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <a href="/about">About</a>
        <a href="/customers">Customers</a>
        <a href="/careers">Careers</a>
        <a href="/contact">Contact</a>
      </div>
      <div class="footer-col">
        <h5>Resources</h5>
        <a href="/blog">Blog</a>
        <a href="/guides">Guides</a>
        <a href="/changelog">Changelog</a>
        <a href="/trust-center">Trust center</a>
      </div>
      <div class="footer-col">
        <h5>Legal</h5>
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
        <a href="/security">Security</a>
        <a href="/dpa">DPA</a>
      </div>
    </div>
    <div class="footer-bottom">
      <motion>© 2026 revzio. All rights reserved.</div>
      <div>Made for finance teams who'd rather be home by six.</div>
    </div>
  </div>
</footer>
"""

