/**
 * Demo booking → Calendly
 * Replace CALENDLY_EVENT_URL with your scheduling link from Calendly:
 *   Calendly → Event types → your event → Copy link
 * Example: https://calendly.com/your-team/revzio-demo
 */
window.revzioDemoConfig = {
  CALENDLY_EVENT_URL: 'https://calendly.com/contact-revzio/30min',

  /** If true, opens Calendly in a new tab instead of embedding on the page */
  CALENDLY_OPEN_IN_NEW_TAB: false,

  /**
   * Keep false for the full Calendly layout: host avatar, event details,
   * month picker, and scrollable time slots after a date is selected.
   */
  CALENDLY_HIDE_EVENT_DETAILS: false,

  /** Calendly invitee question key for “Please share anything…” (usually a1) */
  CALENDLY_CUSTOM_ANSWER_KEY: 'a1',
};
