# Обрій — SaaS features page

A one-page, Ukrainian-language "Features" page for a fictional SaaS product: Обрій, a finance and workflow
tool for small businesses with an AI assistant. Built as a portfolio piece. The structure and interactions were
studied from a public Framer SaaS template; the brand, logo, copy, interface mock-ups and photos are original.

## Sections

| Section | What it does |
|---|---|
| Hero | Twinkling starfield on canvas, headline, and a tilted app window with a live-looking dashboard (animated bars, shimmer) |
| Trust | Founder quote card, two rolling-digit counters (12k+, 98 %), endless marquee of fictional partner logos |
| Editor | A full report-builder mock (blocks, data sources, AI hint, canvas with a website, inspector) drawn in HTML/CSS and scaled to the column; three key benefits |
| Tools | Four ARIA tabs (arrow / Home / End keys) — templates library, overview KPIs, team approvals chat, payments ring |
| Reviews | Photo + quote slider with arrows, swipe, autoplay that pauses on hover |
| FAQ | Accordion, one item open at a time |
| CTA | Tilted product screens and two buttons |
| Footer | Links, office, placeholder phone |

The navigation hides while you scroll down and comes back on scroll up; on phones it becomes a burger menu.
Every "Почати / Зв'язатися" button opens a modal with a validated sign-up form (focus trap, Escape to close).

## Stack

- Plain **HTML + CSS + vanilla JS**, no build step and no dependencies
- **Inter** variable font with the optical-size axis (Display cuts at large sizes), Cyrillic + Latin, self-hosted (SIL OFL)
- Interface mock-ups are HTML/CSS; the planet horizon and the three review portraits were generated with an
  AI image model (WaveSpeed, nano-banana 2.1)

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Tests (Playwright)

```bash
pip install playwright && python -m playwright install chromium
python tests/test_site.py
```

78 checks at 1440 / 768 / 375 px: JS errors, overflow, images, fonts, anchors, starfield, hide-on-scroll nav and
burger menu, counters, marquee, editor scaling, tabs and keyboard, slider, FAQ, modal validation and the toast.
