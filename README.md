# revzio — Marketing Website

A 4-page static marketing website for a fictional B2B finance SaaS called **revzio** (revenue reconciliation / continuous close). Built as a single, no-build-step set of HTML files — open any file in a browser and it works.

## Project structure

```
revzio-website/
├── index.html        # Home page (hero + product mockup + features + testimonial + CTA)
├── platform.html     # Product capabilities page
├── solutions.html    # By-role + by-industry page
├── resources.html    # Blog / guides / customer stories page
└── README.md
```

Each page is self-contained: HTML, CSS (inline `<style>`), and a small bit of JavaScript live in the same file. There's no build step, no bundler, no package.json. Open `index.html` in a browser to view.

## Design system

A consistent visual language runs across all four pages.

### Colors

| Token | Value | Used for |
| --- | --- | --- |
| `--bg` | `#FAFAF7` | Light page background (warm off-white) |
| `--bg-alt` | `#F2F1EC` | Alternating section background |
| `--ink` | `#0E1410` | Primary text, dark CTA sections |
| `--ink-soft` | `#4A524C` | Body copy, secondary text |
| `--ink-muted` | `#8A918C` | Labels, captions |
| `--line` | `#E5E3DC` | Borders, dividers |
| `--accent` | `#0F6B4E` | Primary accent (emerald) — light-mode highlights |
| `--accent-soft` | `#E8F1ED` | Accent backgrounds (pills, icon tiles) |
| `--gold` | `#C49A4B` | Secondary accent on dark CTA sections |
| `--hero-bg` | `#0A1A2F` | Dark navy hero background |
| `--hero-mint` | `#7FCFAA` | Mint accent for dark-hero italics & eyebrow |

### Typography

- **Display / headlines:** [Fraunces](https://fonts.google.com/specimen/Fraunces) — serif, italic emphasis on key words via `<em>` tags
- **Body / UI:** [Inter](https://fonts.google.com/specimen/Inter) — clean sans

Both loaded from Google Fonts via `<link>` in each page's `<head>`.

### Layout patterns

- **Sticky nav:** transparent over the dark hero, transitions to opaque light bar with dark text once you scroll past the hero (see the JS at the bottom of each file).
- **Dark hero:** dark navy with subtle radial gradients. Italic-serif emphasis word in headlines.
- **Light body sections:** alternating between `--bg` and `--bg-alt` for visual rhythm.
- **Dark CTA section:** before the footer, dark background with gold-accented italic.
- **Scroll-reveal:** elements with class `reveal` fade up using `IntersectionObserver`.

## Key components

| Class | Purpose |
| --- | --- |
| `.container` | 1180px max-width wrapper with horizontal padding |
| `.hero` | Dark navy hero section |
| `.eyebrow` | Small pill above hero headline |
| `.section-eyebrow` | Small uppercase label above section headings |
| `.btn-primary` / `.btn-secondary` / `.btn-ghost` | Three button styles |
| `.cards` | 3-column responsive grid of feature cards |
| `.card` | Individual feature card with icon + title + body |
| `.row` / `.row.reverse` | 2-column content + visual layout |
| `.cta-section` | Dark CTA section before footer |
| `.reveal` | Scroll-reveal animation hook |

## Working with Cursor (or another AI editor)

When asking Cursor to make changes, give it context like:

> "This is a 4-page static HTML site for a fictional B2B SaaS called revzio. All CSS is inline in each file. The design system uses CSS custom properties — see `--bg`, `--ink`, `--accent`, `--hero-bg`, etc. defined in `:root` at the top of each file. Fonts are Fraunces (serif, display) and Inter (sans, body). Keep the dark navy hero / light body / dark CTA section structure consistent across pages."

Examples of changes Cursor can make easily:

- **Color scheme swap:** "Change `--accent` from emerald to indigo (`#3F51B5`) across all four pages."
- **New page:** "Create a `pricing.html` matching the design language of the existing pages, with three tiers."
- **Copy edits:** "On `index.html`, change the hero headline to '...'."
- **Layout tweaks:** "Make the cards grid 2 columns instead of 3 on `platform.html`."
- **New section:** "Add a 'Trust' section after the testimonial on `index.html` with three security badges."

## Things to know before editing

- **CSS duplication is intentional.** Each file has its own `<style>` block so the pages are fully self-contained. If you change a color or pattern, ask Cursor to apply it across all four files.
- **Links between pages use `href="platform.html"` style** (relative, same-directory) — keep them this way unless you set up routing.
- **No JavaScript framework.** Just vanilla JS for the scroll-reveal and nav transition. Anything dynamic (forms, search, etc.) would need to be added.
- **Hosting:** drag any of these files into [netlify.com/drop](https://app.netlify.com/drop) for a free live URL in 30 seconds, or use Vercel / GitHub Pages / Cloudflare Pages.

## Quick local preview

Open `index.html` directly in your browser, or run a local server from this folder:

```bash
# Python 3
python3 -m http.server 8000

# Then open http://localhost:8000
```

## Notes on the content

The copy is original placeholder content written for a fictional company called revzio (revenue reconciliation / continuous close for finance teams). All customer names, testimonials, statistics, and case studies are fabricated for demo purposes. Replace with your own before using for anything real.
