(function () {
  'use strict';

  function rootPrefix() {
    return /\/blog\//.test(window.location.pathname) ? '../' : '';
  }

  /** Display label → logo file slug (without .svg) */
  var BRAND_SLUGS = {
    stripe: 'stripe',
    netsuite: 'netsuite',
    salesforce: 'salesforce',
    quickbooks: 'quickbooks',
    'quickbooks online': 'quickbooks',
    'quickbooks desktop': 'quickbooks',
    xero: 'xero',
    hubspot: 'hubspot',
    snowflake: 'snowflake',
    workday: 'workday',
    avalara: 'avalara',
    okta: 'okta',
    sap: 'sap',
    oracle: 'oracle',
    gusto: 'gusto',
    rippling: 'rippling',
    adp: 'adp',
    brex: 'brex',
    ramp: 'ramp',
    zuora: 'zuora',
    recurly: 'recurly',
    paddle: 'paddle',
    braintree: 'braintree',
    square: 'square',
    deel: 'deel',
    databricks: 'databricks',
    fivetran: 'fivetran',
    pipedrive: 'pipedrive',
    zoho: 'zoho',
    'zoho crm': 'zoho',
    dualentry: 'dualentry',
    'dual entry': 'dualentry',
    razorpay: 'razorpay',
    paypal: 'paypal',
    'pay pal': 'paypal',
    coindcx: 'coindcx',
    'coin dcx': 'coindcx',
    pixis: 'pixis',
    'pixis.ai': 'pixis',
    faclon: 'faclon',
    'faclon labs': 'faclon',
    'falcon labs': 'faclon',
    plaid: 'plaid',
    mercury: 'mercury',
    paychex: 'paychex',
    sage: 'sage',
    'sage intacct': 'sage',
    coupa: 'coupa',
    gmail: 'gmail',
    outlook: 'outlook',
    taxjar: 'taxjar',
    vertex: 'vertex',
    freshbooks: 'freshbooks',
    onelogin: 'onelogin',
    bamboohr: 'bamboohr',
    remote: 'remote',
    redshift: 'redshift',
    dbt: 'dbt',
    chase: 'chase',
    'jpmorgan chase': 'chase',
    sox: 'sox',
    fasb: 'fasb',
    ifrs: 'ifrs',
    'google sso': 'google',
    'microsoft azure ad': 'microsoft',
    'microsoft dynamics': 'microsoft',
    'bank of america': 'chase'
  };

  function normalizeLabel(text) {
    return String(text || '')
      .replace(/^[◎•]\s*/, '')
      .trim()
      .toLowerCase();
  }

  function slugForLabel(label) {
    if (!label) return null;
    if (BRAND_SLUGS[label]) return BRAND_SLUGS[label];
    var first = label.split(/[(\/]/)[0].trim();
    if (BRAND_SLUGS[first]) return BRAND_SLUGS[first];
    return null;
  }

  function isBadgeSlug(slug) {
    return slug === 'sox' || slug === 'fasb' || slug === 'ifrs';
  }

  function applyLogo(el, slug, label) {
    var prefix = rootPrefix();
    var src = prefix + 'assets/logos/' + slug + '.svg';
    var img = document.createElement('img');
    img.className = 'int-logo__img';
    img.src = src;
    img.alt = label;
    img.loading = 'lazy';
    img.decoding = 'async';
    el.textContent = '';
    el.appendChild(img);
    el.classList.add('int-logo--brand');
    if (slug) {
      el.setAttribute('data-brand', slug);
    }
    if (el.classList.contains('int-logo') && el.style.borderRadius) {
      el.classList.add('int-logo--pill');
    }
    if (isBadgeSlug(slug)) {
      el.classList.add('int-logo--badge');
    }
    if (!el.getAttribute('aria-label')) {
      el.setAttribute('aria-label', label);
    }
  }

  function hydrateIntegrationLogos() {
    var nodes = document.querySelectorAll('.int-logo:not(.int-logo--brand), .mock-knowledge-orbit:not(.int-logo--brand)');
    nodes.forEach(function (el) {
      var slugAttr = el.getAttribute('data-brand');
      var label = (el.getAttribute('data-label') || el.textContent || '').trim();
      var labelNorm = normalizeLabel(label);
      var slug = slugAttr || slugForLabel(labelNorm);
      if (!slug) return;
      if (el.classList.contains('int-logo--brand')) return;
      var displayLabel = label.replace(/^[◎•]\s*/, '').trim() || slug;
      applyLogo(el, slug, displayLabel);
    });
  }

  window.revzioIntegrationLogos = {
    hydrate: hydrateIntegrationLogos,
    slugForLabel: slugForLabel
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateIntegrationLogos);
  } else {
    hydrateIntegrationLogos();
  }
})();
