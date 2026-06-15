(function () {
  const FREE_EMAIL_DOMAINS = new Set([
    'gmail.com',
    'googlemail.com',
    'yahoo.com',
    'yahoo.co.in',
    'yahoo.co.uk',
    'yahoo.in',
    'hotmail.com',
    'hotmail.co.uk',
    'outlook.com',
    'outlook.in',
    'live.com',
    'msn.com',
    'icloud.com',
    'me.com',
    'mac.com',
    'aol.com',
    'protonmail.com',
    'proton.me',
    'pm.me',
    'mail.com',
    'gmx.com',
    'gmx.net',
    'yandex.com',
    'yandex.ru',
    'rediffmail.com',
    'rocketmail.com',
    'inbox.com',
    'ymail.com',
  ]);

  const EMAIL_FORMAT = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
  const PLACEHOLDER_CALENDLY = /YOUR_USERNAME|YOUR_EVENT/i;

  function getConfig() {
    return window.revzioDemoConfig || {};
  }

  function getEmailDomain(email) {
    const at = email.lastIndexOf('@');
    if (at < 0) return '';
    return email.slice(at + 1).trim().toLowerCase();
  }

  function isBusinessEmail(email) {
    const value = email.trim();
    if (!EMAIL_FORMAT.test(value)) return false;
    const domain = getEmailDomain(value);
    if (!domain || FREE_EMAIL_DOMAINS.has(domain)) return false;
    return true;
  }

  function setFieldError(wrapper, input, hasError) {
    if (!wrapper) return;
    wrapper.classList.toggle('has-error', hasError);
    if (input) input.setAttribute('aria-invalid', hasError ? 'true' : 'false');
  }

  function getFormPayload(form) {
    const data = new FormData(form);
    const first = (data.get('first_name') || '').toString().trim();
    const last = (data.get('last_name') || '').toString().trim();
    const email = (data.get('email') || '').toString().trim();
    const company = (data.get('company') || '').toString().trim();
    const teamSize = (data.get('finance_team_size') || '').toString().trim();
    const revenue = (data.get('company_revenue') || '').toString().trim();
    const countryCode = (data.get('country_code') || '').toString().trim();
    const phone = (data.get('phone') || '').toString().trim();
    const fullPhone = phone ? countryCode + ' ' + phone : '';

    return {
      firstName: first,
      lastName: last,
      name: [first, last].filter(Boolean).join(' '),
      email,
      company,
      teamSize,
      revenue,
      phone: fullPhone,
    };
  }

  /** Meeting notes for Calendly custom question (plain text — not URL-encoded). */
  function buildMeetingNotes(payload) {
    return [
      payload.company && 'Company: ' + payload.company,
      payload.teamSize && 'Finance team: ' + payload.teamSize,
      payload.revenue && 'Revenue: ' + payload.revenue,
      payload.phone && 'Phone: ' + payload.phone,
    ]
      .filter(Boolean)
      .join('\n');
  }

  function buildCalendlyUrl(baseUrl, payload) {
    const cleanBase = (baseUrl || '').split('?')[0];
    const params = new URLSearchParams(
      baseUrl.includes('?') ? baseUrl.split('?')[1] : ''
    );

    const config = getConfig();
    if (config.CALENDLY_HIDE_EVENT_DETAILS) {
      params.set('hide_event_type_details', '1');
    }
    params.set('hide_gdpr_banner', '1');
    params.set('primary_color', '0a1a2f');
    params.set('text_color', '0a0f0c');
    params.set('background_color', 'f4f7f5');

    /* Do not put name, email, or a1 in the URL — spaces become "+" and show
       literally in Calendly. Use initInlineWidget prefill instead. */

    const qs = params.toString();
    return qs ? cleanBase + '?' + qs : cleanBase;
  }

  function buildCalendlyPrefill(payload) {
    const config = getConfig();
    const answerKey = config.CALENDLY_CUSTOM_ANSWER_KEY || 'a1';
    const prefill = {
      email: payload.email || '',
    };

    if (payload.firstName) prefill.firstName = payload.firstName;
    if (payload.lastName) prefill.lastName = payload.lastName;
    if (!payload.firstName && !payload.lastName && payload.name) {
      prefill.name = payload.name;
    }

    const notes = buildMeetingNotes(payload);
    if (notes) {
      prefill.customAnswers = {};
      prefill.customAnswers[answerKey] = notes;
    }

    return prefill;
  }

  function isCalendlyConfigured(url) {
    return Boolean(url && !PLACEHOLDER_CALENDLY.test(url));
  }

  function hideCalendlyPlaceholder(embedEl) {
    const placeholder = embedEl?.closest('.demo-calendar-card')?.querySelector('.calendly-placeholder');
    if (placeholder) placeholder.classList.add('is-hidden');
  }

  function showCalendlyPlaceholder(embedEl) {
    const placeholder = embedEl?.closest('.demo-calendar-card')?.querySelector('.calendly-placeholder');
    if (placeholder) placeholder.classList.remove('is-hidden');
  }

  function loadCalendlyWidget(embedEl, schedulingUrl, payload) {
    const prefill = buildCalendlyPrefill(payload || {});

    const panel = embedEl.closest('.schedule-panel');
    if (panel) {
      const headH = panel.querySelector('.schedule-panel-head')?.offsetHeight || 72;
      const stageH = panel.closest('.schedule-stage')?.offsetHeight || 760;
      embedEl.style.height = Math.max(stageH - headH, 520) + 'px';
    } else if (embedEl.closest('.demo-calendar-card')) {
      embedEl.style.minHeight = '700px';
    }

    window.Calendly.initInlineWidget({
      url: schedulingUrl,
      parentElement: embedEl,
      prefill,
      resize: true,
    });
  }

  function showScheduleStage() {
    const demoCard = document.getElementById('demo-card');
    const scheduleStage = document.getElementById('schedule-stage');

    if (demoCard) demoCard.classList.add('is-hidden');
    if (scheduleStage) {
      scheduleStage.hidden = false;
      scheduleStage.classList.add('is-visible');
      scheduleStage.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    document.querySelector('.demo-page')?.classList.add('demo-page--scheduling');
  }

  function showCalendlyAfterSubmit(form) {
    const config = getConfig();
    const baseUrl = config.CALENDLY_EVENT_URL || '';
    const payload = getFormPayload(form);
    const schedulingUrl = buildCalendlyUrl(baseUrl, payload);

    const fallbackEl = document.getElementById('calendly-fallback');
    const fallbackLink = document.getElementById('calendly-fallback-link');
    const embedEl = document.getElementById('calendly-embed');

    showScheduleStage();

    if (!isCalendlyConfigured(baseUrl)) {
      if (fallbackEl) fallbackEl.classList.add('show');
      if (fallbackLink) {
        fallbackLink.href = '#';
        fallbackLink.textContent = 'Add your Calendly link in js/demo-config.js';
      }
      return;
    }

    if (fallbackLink) fallbackLink.href = schedulingUrl;

    if (config.CALENDLY_OPEN_IN_NEW_TAB) {
      window.open(schedulingUrl, '_blank', 'noopener,noreferrer');
      if (fallbackEl) fallbackEl.classList.add('show');
      return;
    }

    function tryEmbed() {
      if (window.Calendly && embedEl) {
        hideCalendlyPlaceholder(embedEl);
        embedEl.innerHTML = '';
        loadCalendlyWidget(embedEl, schedulingUrl, payload);
        return;
      }
      if (fallbackEl) fallbackEl.classList.add('show');
    }

    if (window.Calendly) {
      tryEmbed();
    } else {
      window.addEventListener('load', tryEmbed, { once: true });
      setTimeout(tryEmbed, 2500);
    }
  }

  function initDirectCalendlyEmbed() {
    const embedEl = document.getElementById('calendly-embed');
    if (!embedEl || document.getElementById('demo-form')) return;

    const config = getConfig();
    const baseUrl = config.CALENDLY_EVENT_URL || '';
    const schedulingUrl = buildCalendlyUrl(baseUrl, {});
    const fallbackEl = document.getElementById('calendly-fallback');
    const fallbackLink = document.getElementById('calendly-fallback-link');

    if (!isCalendlyConfigured(baseUrl)) {
      if (fallbackEl) fallbackEl.classList.add('show');
      if (fallbackLink) {
        fallbackLink.href = '#';
        fallbackLink.textContent = 'Add your Calendly link in js/demo-config.js';
      }
      return;
    }

    if (fallbackLink) fallbackLink.href = schedulingUrl;

    if (config.CALENDLY_OPEN_IN_NEW_TAB) {
      window.open(schedulingUrl, '_blank', 'noopener,noreferrer');
      if (fallbackEl) fallbackEl.classList.add('show');
      return;
    }

    function tryEmbed() {
      if (window.Calendly && embedEl) {
        hideCalendlyPlaceholder(embedEl);
        embedEl.innerHTML = '';
        loadCalendlyWidget(embedEl, schedulingUrl, {});
        return;
      }
      if (fallbackEl) fallbackEl.classList.add('show');
    }

    if (window.Calendly) {
      tryEmbed();
    } else {
      window.addEventListener('load', tryEmbed, { once: true });
      setTimeout(tryEmbed, 2500);
    }
  }

  function init() {
    initDirectCalendlyEmbed();

    const form = document.getElementById('demo-form');
    if (!form) return;

    const emailInput = document.getElementById('email');
    const emailWrapper = document.getElementById('field-email');
    const financeSelect = document.getElementById('finance-team-size');
    const financeWrapper = document.getElementById('field-finance-team');
    const revenueSelect = document.getElementById('company-revenue');
    const revenueWrapper = document.getElementById('field-revenue');

    function validateEmail(showError) {
      const value = emailInput.value.trim();
      let ok = true;
      if (!value) {
        ok = false;
      } else if (!EMAIL_FORMAT.test(value)) {
        ok = false;
        if (showError) {
          document.getElementById('email-error').textContent =
            'Please enter a valid email address.';
        }
      } else if (!isBusinessEmail(value)) {
        ok = false;
        if (showError) {
          document.getElementById('email-error').textContent =
            'Please use your company work email (not Gmail, Yahoo, Outlook, etc.).';
        }
      }
      if (showError || !ok) setFieldError(emailWrapper, emailInput, !ok);
      return ok;
    }

    function validateSelect(select, wrapper) {
      const ok = Boolean(select && select.value);
      setFieldError(wrapper, select, !ok);
      return ok;
    }

    emailInput.addEventListener('blur', () => {
      if (emailInput.value.trim()) validateEmail(true);
    });

    emailInput.addEventListener('input', () => {
      if (emailWrapper.classList.contains('has-error')) validateEmail(true);
    });

    financeSelect.addEventListener('change', () => validateSelect(financeSelect, financeWrapper));
    revenueSelect.addEventListener('change', () => validateSelect(revenueSelect, revenueWrapper));

    const params = new URLSearchParams(window.location.search);
    if (params.get('email') || params.get('first_name')) {
      const first = params.get('first_name') || '';
      const last = params.get('last_name') || '';
      if (first) document.getElementById('first-name').value = first;
      if (last) document.getElementById('last-name').value = last;
      if (params.get('email')) emailInput.value = params.get('email');
      if (params.get('company')) document.getElementById('company').value = params.get('company');
      if (params.get('finance_team_size')) financeSelect.value = params.get('finance_team_size');
      if (params.get('company_revenue')) revenueSelect.value = params.get('company_revenue');
      if (params.get('phone')) document.getElementById('phone').value = params.get('phone');
      window.history.replaceState({}, '', window.location.pathname);
      showCalendlyAfterSubmit(form);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const emailOk = validateEmail(true);
      const financeOk = validateSelect(financeSelect, financeWrapper);
      const revenueOk = validateSelect(revenueSelect, revenueWrapper);

      if (!form.checkValidity() || !emailOk || !financeOk || !revenueOk) {
        if (!form.checkValidity()) form.reportValidity();
        const firstBad =
          form.querySelector(':invalid') ||
          (!emailOk ? emailInput : null) ||
          (!financeOk ? financeSelect : null) ||
          (!revenueOk ? revenueSelect : null);
        if (firstBad && typeof firstBad.focus === 'function') firstBad.focus();
        return;
      }

      showCalendlyAfterSubmit(form);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
