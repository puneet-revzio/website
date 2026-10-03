/**
 * Google Analytics 4 — production hosts only.
 * Loads on www.revzio.ai / revzio.ai; skipped on localhost and Vercel previews.
 */
(function () {
  var host = window.location.hostname;
  if (host !== "www.revzio.ai" && host !== "revzio.ai") return;

  var MEASUREMENT_ID = "G-Q4LKKLTR1H";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
  document.head.appendChild(script);

  gtag("js", new Date());
  gtag("config", MEASUREMENT_ID);

  window.revzioTrackGenerateLead = function (params) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", "generate_lead", params || {});
  };
})();
