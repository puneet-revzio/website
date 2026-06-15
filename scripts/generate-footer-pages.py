#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER = """
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo"><span class="logo-dot"></span>revzio</a>
        <p>The reconciled source of truth for modern finance teams.</p>
      </div>
      <div class="footer-col">
        <h5>Product</h5>
        <a href="reconciliation.html">Reconciliation</a>
        <a href="close-workflow.html">Close workflow</a>
        <a href="reporting.html">Reporting</a>
        <a href="integrations.html">Integrations</a>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <a href="about.html">About</a>
        <a href="customers.html">Customers</a>
        <a href="careers.html">Careers</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h5>Resources</h5>
        <a href="blog.html">Blog</a>
        <a href="guides.html">Guides</a>
        <a href="changelog.html">Changelog</a>
        <a href="trust-center.html">Trust center</a>
      </div>
      <div class="footer-col">
        <h5>Legal</h5>
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
        <a href="security.html">Security</a>
        <a href="dpa.html">DPA</a>
      </div>
    </div>
    <div class="footer-bottom">
      <motion>© 2026 revzio. All rights reserved.</div>
      <div>Made for finance teams who'd rather be home by six.</div>
    </div>
  </div>
</footer>
"""

