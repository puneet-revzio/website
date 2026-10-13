(function () {
  var STORAGE_KEY = "revzio_newsletter_subscribed";
  var section = document.getElementById("newsletter");
  var form = document.getElementById("newsletter-form");
  if (!section || !form) return;

  var emailInput = document.getElementById("newsletter-email");
  var consentInput = document.getElementById("newsletter-consent");
  var errorEl = document.getElementById("newsletter-error");
  var successEl = document.getElementById("newsletter-success");

  function showError(message) {
    if (!errorEl) return;
    errorEl.textContent = message || "";
    errorEl.classList.toggle("is-visible", !!message);
  }

  function showSuccess() {
    section.classList.add("is-subscribed");
    if (successEl) {
      successEl.classList.add("is-visible");
      successEl.focus && successEl.setAttribute("tabindex", "-1");
      try {
        successEl.focus();
      } catch (e) {}
    }
    try {
      localStorage.setItem(STORAGE_KEY, "1");
    } catch (e) {}
  }

  try {
    if (localStorage.getItem(STORAGE_KEY) === "1") showSuccess();
  } catch (e) {}

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    showError("");

    var email = (emailInput && emailInput.value ? emailInput.value : "").trim();
    var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailOk) {
      showError("Please enter a valid email address.");
      if (emailInput) emailInput.focus();
      return;
    }
    if (consentInput && !consentInput.checked) {
      showError("Please consent to the privacy policy to subscribe.");
      consentInput.focus();
      return;
    }

    var btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Subscribing…";
    }

    // Lead capture endpoint can be wired later; UI confirms immediately for now.
    window.setTimeout(function () {
      if (typeof window.gtag === "function") {
        window.gtag("event", "generate_lead", {
          lead_source: "newsletter",
          page_path: location.pathname,
        });
      }
      showSuccess();
    }, 250);
  });
})();
