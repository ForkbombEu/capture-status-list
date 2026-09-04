# Credimi — Brand & Design Guidelines

> **Credimi** is the trustworthy compliance checker for decentralized identity solutions, built and operated by **Forkbomb BV** (Amsterdam) under the NGI TRUSTCHAIN programme. This document is the canonical reference for anyone designing or developing on the brand: product designers, marketers, agency partners, and engineers writing components.

If this is the first time you're touching Credimi: read this top-to-bottom once, then keep it open as a reference. Everything in here is enforceable — tokens live in [`colors_and_type.css`](./colors_and_type.css), assets in [`assets/`](./assets/), worked examples in [`ui_kits/webapp/`](./ui_kits/webapp/) and [`preview/`](./preview/).

---

## Table of contents

1. [Brand principles](#1-brand-principles)
2. [Voice & tone](#2-voice--tone)
3. [Logo](#3-logo)
4. [Color](#4-color)
5. [Typography](#5-typography)
6. [Spacing, radii, elevation](#6-spacing-radii-elevation)
7. [Layout & grid](#7-layout--grid)
8. [Iconography & illustration](#8-iconography--illustration)
9. [Motion](#9-motion)
10. [Components](#10-components)
11. [Patterns](#11-patterns)
12. [Do & Don't](#12-do--dont)
13. [Asset index](#13-asset-index)

---

## 1. Brand principles

Credimi sits in a serious, technical, EU-regulated market. Our brand reflects that — but it should never feel **bureaucratic**, **cold**, or **opaque**.

| Principle | What it means in practice |
|---|---|
| **Calm, not corporate** | Generous whitespace, restrained color, no exclamation marks. A reader should feel like they're in expert hands, not a sales funnel. |
| **Honest about complexity** | We don't simplify domain language ("conformance", "OID4VCI Draft 13", "mDoc"). We do explain it inline when context demands. |
| **Numbers earn their place** | Stats, scores, percentages, dates appear unsoftened (`80% compliant`, `20 over 30 tests passed`, `24/04/2026`). Never round, never hide. |
| **Evidence over claims** | Status chips, scoreboards, audit trails — design surfaces verifiable facts, not adjectives. |
| **EU-formal, not EU-stiff** | We address users in 2nd person ("Your trustworthy compliance checker…"). Dates are `DD/MM/YYYY`. Tone is "Stripe docs", not "government portal". |

---

## 2. Voice & tone

### Sentence case, always

- Buttons: `Start a new test` — not `Start A New Test`, not `START A NEW TEST`.
- Section headers carry a trailing colon: `Apps:`, `Test results:`, `Find credentials:`.
- Never SHOUTY CASE outside of eyebrow labels (which are tracked +14% and uppercase by typography rule, not by content).

### Imperatives for CTAs

`Start a new test` · `Explore Marketplace` · `Test interop and conformance` · `See pipelines` · `See history` · `See all ↗`

The "See all ↗" link with an arrow-up-right glyph is the canonical "more of this elsewhere" pattern.

### Domain vocabulary is non-negotiable

Keep these terms **exact**, never paraphrase:

> credential issuer · verifier · wallet · conformance · interoperability · OpenID4VC · OID4VCI · OpenID4VP · EUDI · EUDIW · mDoc · SD-JWT VC · JWT · ES256 · jwk · cose_key · Draft 13 · Temporal · trust list · EUDI ARF

### Numbers, dates, formatting

| Type | Format | Example |
|---|---|---|
| Percentage | `N% compliant` | `80% compliant` |
| Run counts | `N over M tests passed` | `20 over 30 tests passed` |
| Date | `DD/MM/YYYY` | `24/04/2026` |
| Date + time | `DD MMM YYYY, HH:mm` (24h) | `20 May 2026, 14:32` |
| Identifier | monospace, all-caps | `OID4VCI · DRAFT 13` |
| Version | semver, monospace | `v2.4.1` |

### Emoji policy

**Never** in the product UI. They're acceptable only in the GitHub README for nav purposes (📋, 🛠️). Empty/error states use illustrations, not emoji.

### Examples taken from the live product

> _"EUDIW Conformance, Interoperability and Marketplace"_ — hero title
>
> _"Explore the marketplace and try credentials, wallets and services. Test the conformance and interoperability of your EUDIW solution."_ — hero sub
>
> _"Hi, Andrea1234test"_ — dashboard greeting
>
> _"Didimo — your gateway to decentralized identity management and secure communication."_ — service description

---

## 3. Logo

### Lockups

| File | Use case |
|---|---|
| [`assets/credimi_logo.svg`](./assets/credimi_logo.svg) | **Wordmark** with indigo→blue→purple gradient. Default. Light backgrounds only. |
| [`assets/credimi_logo_white.svg`](./assets/credimi_logo_white.svg) | **Wordmark, white**. Indigo / dark backgrounds, footer, cover slides. |
| [`assets/credimi_logo_mark.svg`](./assets/credimi_logo_mark.svg) | **Mark / symbol**. Square use: favicon, social avatar, app icon. |

### Minimum size

- **Wordmark**: 22px tall in product UI (topbar), 28px in marketing headers.
- **Mark**: 32px square minimum. Smaller than that, switch to a vector at @1x — don't rasterize.

### Clear space

Reserve clear space equal to the height of the lowercase "c" on all four sides. Don't place the logo against busy imagery; if you must, use the white wordmark on a dark scrim.

### Don't

- Don't recolor either lockup.
- Don't recreate the gradient — always use the SVG. The gradient stops are tuned and shouldn't be paraphrased in code.
- Don't outline, drop-shadow, emboss, or apply effects.
- Don't place the wordmark next to another wordmark without ≥24px gap.
- Don't use the logo as decorative texture or repeat it.

---

## 4. Color

All colors live in [`colors_and_type.css`](./colors_and_type.css) as CSS custom properties. Always reference the variable, never inline a hex.

### Primary — deep indigo

```css
--brand-primary:      #220E7E;   /* rgb(34,14,126) — Figma button fill */
--brand-primary-700:  #1A0A66;   /* hover */
--brand-primary-600:  #150753;   /* active */
--brand-accent:       #3D1FC4;   /* rgb(61,31,196) — wordmark gradient, link accent */
--brand-accent-vivid: #9747FF;   /* rgb(151,71,255) — dashed callout border */
```

Deep indigo carries everything important: primary CTAs, the footer slab, indigo-on-light section accents, the gradient origin in the wordmark. It's the only color allowed to dominate a layout (e.g. the entire footer band, a hero slab). The brighter `--brand-accent` is reserved for the wordmark gradient and link accents.

### Secondary — lavender

```css
--brand-secondary:        #EEEAFE;   /* rgb(238,234,254) — page wash + input bg */
--brand-secondary-mid:    #E2DCF8;   /* rgb(226,220,248) — ownership row stripe */
--brand-secondary-strong: #D8CFFF;   /* rgb(216,207,255) — sidebar accent, badge wash */
--brand-secondary-deep:   #CFC7EB;   /* rgb(207,199,235) — secondary button fill */
```

Lavender is the **page tint** behind content. White is reserved for cards, popovers, inputs. _Never_ put content directly on a pure-white page background — always use the lavender wash + white cards combo.

### Neutrals

```css
--bg:           #FFFFFF;
--bg-muted:     #F6F6F6;   /* rgb(246,246,246) — code/logo placeholder bg */
--bg-off-white: #FAFAFA;   /* rgb(250,250,250) — text on indigo */
--fg:           #2F294B;   /* rgb(47,41,75)    — body + heading ink */
--fg-muted:     #9A97B5;   /* rgb(154,151,181) — secondary text, rules */
--fg-subtle:    #606083;   /* rgb(96,96,131)   — caption text */
--border:       #E4E4E7;   /* rgb(228,228,231) — input/card hairline */
--border-strong:#9A97B5;   /* rgb(154,151,181) — table cell divider */
```

### Semantic / status

Status chips have **exact, named colors**. Don't invent new statuses — propose extensions if you need them.

| Token | Hex/oklch | Used for |
|---|---|---|
| `--success` / `--success-bg`     | green   | Verifier · compliant · pass · "Stable" score band |
| `--warning` / `--warning-bg`     | amber   | Issuer · flaky · 60–79% score band |
| `--destructive` / (`#FDE7E7`)    | red     | Errors · destructive actions · <30% score band |
| `--wallet` / `--wallet-bg`       | purple  | Wallet chip |
| `--credential` (`#A04D0F`) / (`#FFE9D6`) | orange | Credential chip · 30–59% band |
| `--info`                         | indigo  | Conformance · neutral info chip |

### Score bands (scoreboard / pipelines)

| Range | Label | Color band |
|---|---|---|
| ≥ 80% | **Stable** — safe to integrate against | green |
| 60–79% | **Flaky** — works most of the time, expect retries | amber |
| 30–59% | **Failing** — regressions in flight | orange |
| < 30% | **Broken** — see the detail page | red |
| no data | **—** | grey |

### Gradients

**Only** the wordmark uses a gradient (indigo → blue → purple, locked in the SVG). Everything else is solid color. If you find yourself reaching for a gradient on a card, button, or background — stop. Use solid lavender or solid indigo.

---

## 5. Typography

### Family

**Inter** is the only sans family. Loaded from Google Fonts at weights 400 / 500 / 600 / 700 / 800 / 900. Used everywhere in the Figma masters (657 instances across the components library).

**Source Code Pro** for monospace — used in the code-editor frame, test-ID rows, and inline identifiers. Loaded at 400 / 500 / 700.

### Scale (matches Figma node `3:6974`)

| Token | Size / line-height | Weight | Tracking | Used for |
|---|---|---|---|---|
| `--fs-display` | 48 / 48 | 700 | -0.012em | Page title on hero |
| `h1` / `--fs-4xl` | 46 / 50 | 700 | -0.012em | Marketing H1 |
| `h2` / `--fs-3xl` | 30 / 36 | 700 | -0.007em | Section headers, newsletter title |
| `h3` / `--fs-2xl` | 24 / 32 | 700 | -0.006em | Subsection / card titles |
| `h4` / `--fs-xl` | 20 / 28 | 700 | -0.005em | Card titles, lead body |
| `h5` / `--fs-lg` | 18 / 28 | 700 | 0 | "large" label, link card title |
| `--fs-md` | 16 / 28 | 400 | 0 | Body (paragraphs) |
| `--fs-base` | 14 / 20 | 400/500 | 0 | Body small, button label, input value |
| `--fs-xs` | 12 / 17 | 500 | +0.14em | Eyebrows, uppercase labels |

### Display weights

Figma headings are **700 Inter** with negative tracking that scales with size (~-0.012em at display down to -0.005em at h4). Don't drop below 500 for any title. Italic is not used in product UI.

### Eyebrow pattern

```html
<p class="eyebrow">YOUR WORKSPACE</p>
<h1>Hi, Andrea1234test</h1>
```

- 12px, weight 500, letter-spacing 0.14em, uppercase.
- `--fg-muted` on lavender, `--brand-secondary-strong` on indigo.
- Always paired with a heading directly below.

### Numbers in display contexts

Monospace (Source Code Pro) for any number that's an **identifier** (run counts, versions, IDs, timestamps, test names like `sd_jwt_vc:did:request_uri_unsigned:direct_post`). Sans (Inter) for any number that's a **measure** (percent, totals, durations).

```
312/412 runs       ← monospace (counts as identifier)
80% compliant      ← sans, weight 500 (measure)
v2.4.1             ← monospace
20/05/2026         ← monospace
1m 52s             ← sans
```

---

## 6. Spacing, radii, elevation

### Spacing scale

```css
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;
--space-4: 16px;  --space-5: 20px;  --space-6: 24px;
--space-8: 32px;  --space-10: 40px; --space-12: 48px;
--space-16: 64px; --space-20: 80px;
```

Use the scale. Don't pick `15px` because it "looks right". Common multiples in product UI:

- Card internal padding: `16px` or `20px` (`--space-4` / `--space-5`)
- Section gap: `24px` (`--space-6`)
- Page vertical rhythm: `32px` (`--space-8`)
- Hero padding: `40–56px`

### Corner radii

```css
--radius-xs:    4px    /* badges, status chips */
--radius-sm:    5px    /* callout containers */
--radius:       6px    /* CANONICAL — buttons, inputs, cards */
--radius-md:    8px    /* alerts, avatar squares */
--radius-lg:   10px    /* hero cards (rare) */
--radius-xl:   12px    /* large feature blocks (rare) */
--radius-pill: 999px   /* pills, segmented controls */
```

**6px is the canonical radius.** Reach for `--radius` for buttons, inputs and cards. Chips/badges use `--radius-xs` (4px). Alerts use `--radius-md` (8px). Larger radii are exceptions.

### Shadow / elevation

Credimi is **almost flat**. Use shadows sparingly — most surfaces have none, relying on the 1px hairline border instead.

```css
--shadow-sm:  0 1px 2px rgba(0,0,0,.04)            /* focus rings, input hover */
--shadow:     0 1px 3px rgba(0,0,0,.08)            /* popovers, tooltips */
--shadow-md:  0 4px 6px rgba(0,0,0,.08)            /* dropdowns, menus */
--shadow-lg:  0 10px 15px rgba(0,0,0,.08)          /* modals, toasts */
```

If you're using anything above `--shadow-md`, ask yourself if the element really needs to "lift" — usually it doesn't.

---

## 7. Layout & grid

### Container

- **Max content width**: 1280px (`max-w-7xl` in Tailwind terms), centered.
- **Page side padding**: 24–32px on desktop. 16px on mobile.
- **Topbar**: sticky, white, 1px hairline bottom border, no shadow.
- **Footer**: deep-indigo slab, full-bleed, with a `rgba(0,0,0,0.3)` overlay bottom strip reading "Proudly developed by ForkBomb BV". The only sanctioned use of translucency.

### Page chrome pattern

```
┌─────────────────────────────────────────────┐
│  topbar (sticky · white · 1px border)       │
├─────────────────────────────────────────────┤
│  hero / header band                         │
│  (lavender · diagonal-fold motif top-right) │
├─────────────────────────────────────────────┤
│  main content                               │
│  (lavender wash · max-w-7xl · white cards)  │
├─────────────────────────────────────────────┤
│  footer (deep indigo · forkbomb sub-bar)    │
└─────────────────────────────────────────────┘
```

### Section header pattern

The most-used pattern in the product. Memorize it.

```html
<div class="cd-section-header">
  <h2>Test results <span class="count">3</span>:</h2>
  <a class="cd-link">See all <span aria-hidden>↗</span></a>
</div>
```

- H2 title with trailing colon (always).
- Optional inline count chip in lavender-grey.
- 1px bottom border in `--border`.
- Optional "See all ↗" link on the right, underlined, indigo, with the arrow-up-right glyph.

### Card grid density

| Surface | Grid | Card padding |
|---|---|---|
| Dashboard | 2 columns | 16px |
| Marketplace | 3 columns | 16px |
| Hub / catalogue | 4 columns | 14px |
| Scoreboard list | 1 column (full-width cards) | 18px |

### Diagonal-fold motif

A faint criss-cross pattern (two thin diagonals, opacity 0.06–0.10) lives in the **top-right of hero / page-header bands**. Echo it as a smaller watermark in the top-right of feature cards if the slide/page needs the visual continuity.

> Use it on **page headers and marketing surfaces**. Never use it as decoration in body content, never as a full-bleed texture. If it competes for legibility, kill it.

---

## 8. Iconography & illustration

### Icons

- **Lucide** is the only icon family (`@lucide/svelte` in the codebase, CDN bundle for prototypes).
- Stroke width `1.5px`, line style.
- Default size: 16–20px in product UI, 14–16px in dense tables.
- Color: inherit from text (`currentColor`). Don't fill, don't tint.
- Stock names used across the codebase: `ArrowDown`, `ArrowUp`, `ArrowUpRight`, `LayoutDashboardIcon`, `BadgeCheck`, `ShieldCheck`, `ClockIcon`, `CogIcon`, `HandIcon`.

### Status chip icons

Use the Lucide filled variant only inside status chips (`BadgeCheck` inside Verifier). Outside chips, prefer text labels over icon-only buttons.

### Illustrations

Two scenes ship today, used only for **error / empty states**:

- [`assets/404-computer.svg`](./assets/404-computer.svg) — 404 / not-found.
- [`assets/maintenance.svg`](./assets/maintenance.svg) — outage / maintenance.

They're flat multi-color vectors. Don't generate new ones with AI. If you need a new illustration, commission a vector artist and match the existing style (flat, restrained palette, no gradients).

### Hero imagery

Hero photography exists in [`assets/hero.png`](./assets/hero.png) but is rare — used behind the indigo header band, desaturated. Default to the diagonal-fold motif on lavender; photography is an exception.

### Avatars

Default avatars in the Hub are **Auth0-style geometric identicons** — gradient squares with abstract glyphs. See [`uploads/prototypes/Services-Auth0-Identicons*.svg`](./uploads/prototypes/) for the reference set. Real org logos override the identicon when available.

---

## 9. Motion

Credimi motion is **functional, not decorative**. The only package the codebase uses is `tw-animate-css`.

| Motion | Duration | Easing | Used for |
|---|---|---|---|
| Hover state | 150ms | `ease-out` | Buttons, links, cards |
| Focus ring | 200ms | `ease-out` | Inputs, focusable rows |
| Popover / dropdown | 200ms | `ease-out` | + 8px slide-up + fade |
| Toast | 220ms | `ease-out` | `svelte-sonner` defaults |
| Page transition | none | — | We don't do page transitions |

### Forbidden

- Bounces, spring physics, parallax.
- Animations longer than 250ms in the product UI (slides/marketing get more rope).
- Auto-playing video, scroll-jacked animation, mouse-tracked effects.

### Loading

`svelte-loading-spinners` default rings, indigo color. No skeleton shimmer animations — skeletons are static `--bg-muted` blocks.

---

## 10. Components

Worked references live in [`ui_kits/webapp/`](./ui_kits/webapp/). Open `ui_kits/webapp/index.html` for a clickable preview of every primitive in context.

### Buttons

| Variant | Use case | Fill | Text |
|---|---|---|---|
| **Primary** | The page's main CTA. One per surface. | `--brand-primary` (#220E7E) | `--fg-on-primary` (#FAFAFA) |
| **Secondary** | Adjacent to a primary. Soft action. | `--brand-secondary-deep` (#CFC7EB) | `--brand-primary` |
| **Outline** | Tertiary actions. | `#fff` + 1px `--border` | `--fg` |
| **Ghost** | Toolbar buttons, dense surfaces. | transparent | `--fg` |
| **Destructive** | Confirm-delete only. | `--destructive` | `#fff` |
| **Link** | Inline / "See all ↗". | transparent | `--brand-primary` + underline |

Sizes from Figma: `sm` (28px), `md` (40px default), `lg` (48px). All buttons use `--radius` (6px). Font is Inter 500 / 14 / 20.

### Alerts

| Variant | Border | Text | Icon |
|---|---|---|---|
| **Success** | `#096D46` (`--success-border`) | `#096D46` | `check-check` |
| **Destructive** | `#EF4343` (`--destructive`) | `#EF4343` | `triangle-alert` |
| **Info** | `--brand-primary` | `--brand-primary` | `circle-info` |

Alerts are 1px-bordered, 8px-radius rectangles with a 60% white background (`rgba(255,255,255,0.6)`), 17px padding, Inter 500/16 heading + Inter 400/14 body, and an 18×18 lucide icon in the top-left.

### Popovers / MegaMenu

White background, 6px radius, 1px `--border-strong` (`#9A97B5`), `--shadow-md`. Internal padding 16–24px. MegaMenu has a 600×358 grid of 4 `Link` cards in a 2×2.

### Status chips

Pill shape (`--radius-pill`), 12×12 colored dot + 11px label, exact colors from the semantic palette. Available kinds: `verifier · wallet · issuer · credential · custom-check`.

### Cards

White background, 10px radius, 1px hairline border, **no shadow** by default. Internal padding `16–20px`. Top row of a service card is always:

```
[avatar] [name] [badge]                    [actions →]
```

On hover: border darkens to `--border-strong`. No `transform` lift.

### Inputs

- 36px tall.
- 10px radius.
- 1px hairline border.
- White background.
- Focus: `border-color: var(--brand-primary)` + 3px indigo ring at 18% alpha.
- Placeholder copy uses sentence case + trailing colon: `Find applications, features and services:`

### Section headers

See [§7](#7-layout--grid).

### Compliance pills

Score % + band label, color-banded per [§4](#4-color). Always paired with the band label in the small `eyebrow` style next to the number.

### Topbar, footer

Reference implementations in `ui_kits/webapp/Topbar.jsx` and `Footer.jsx`.

---

## 11. Patterns

### Service / app card

Avatar → name → status chip → 1-line description → optional compliance pill. Used in Marketplace, Dashboard "My apps", Hub.

### Test result row

```
Name              Last check       Pass ratio
DIDroom · OID4VCI 24/04/2026       20 over 30 tests passed   [80% compliant]
```

Always: name in sans-bold, dates in monospace, pass-ratio in sans + monospace fraction, score pill on the right.

### Pipeline detail

Universal drill-down pattern. Top: the flow chain (wallet → credential → issuer → verifier). Body: step-by-step results grouped by stage (Issuance / Presentation / Trust). Right column: recent runs + claimed specs. Bottom: a colored **failure callout** when state is `failing`/`broken` that names the root cause and offers an action.

### Empty / error states

Center-aligned illustration (`404-computer.svg` or `maintenance.svg`) above a sentence-case headline + one CTA. Never use copywriting alone to express empty state — pair with the illustration.

### Cross-cutting "See all" pattern

Section header + `See all ↗` link on the right. Always underlined, indigo, with the arrow-up-right glyph (Lucide `ArrowUpRight`).

---

## 12. Do & Don't

### Do

- ✓ Use the lavender wash + white card combo.
- ✓ Keep cards hairline-bordered, shadow-less.
- ✓ Use Inter at 700 for display, 400–500 for body.
- ✓ Use `DD/MM/YYYY` for dates, monospace for IDs.
- ✓ Match status colors exactly to the semantic palette.
- ✓ Use the diagonal-fold motif sparingly, only in page headers.
- ✓ Show numbers unsoftened ("20 over 30 tests passed").
- ✓ Pair every eyebrow with a heading directly below.

### Don't

- ✗ Use gradients anywhere except the wordmark.
- ✗ Use emoji in product UI.
- ✗ Use SHOUTY CASE in titles or button labels.
- ✗ Use AI-generated illustrations.
- ✗ Use Roboto, Arial, or system-default fonts. (Inter IS the brand sans — use it.)
- ✗ Use Manrope as the body font. (It was a former substitution — the Figma source is Inter.)
- ✗ Use shadows on cards by default.
- ✗ Use rounded corners with a left-border accent color.
- ✗ Use icons inside buttons unless the icon is semantically required.
- ✗ Use exclamation marks anywhere in the product UI.
- ✗ Use the diagonal-fold pattern as body decoration.
- ✗ Recolor or modify the logo.

---

## 13. Asset index

| Path | What |
|---|---|
| [`colors_and_type.css`](./colors_and_type.css) | All design tokens (color, type, radius, shadow, spacing). |
| Inter (Google Fonts) | Brand sans — loaded from Google Fonts. Weights 400 / 500 / 600 / 700 / 800 / 900. |
| Source Code Pro (Google Fonts) | Brand monospace — weights 400 / 500 / 700. |
| [`assets/credimi_logo.svg`](./assets/) | Wordmark — gradient, light backgrounds. |
| [`assets/credimi_logo_white.svg`](./assets/) | Wordmark — white, dark backgrounds. |
| [`assets/credimi_logo_mark.svg`](./assets/) | Mark / symbol, square. |
| [`assets/404-computer.svg`](./assets/) | Empty-state illustration. |
| [`assets/maintenance.svg`](./assets/) | Maintenance-state illustration. |
| [`assets/hero.png`](./assets/) | Hero photography (rare use). |
| [`preview/`](./preview/) | Standalone preview cards for Type / Colors / Spacing / Components / Brand. |
| [`ui_kits/webapp/`](./ui_kits/webapp/) | Clickable React recreation of the live web app surface. |
| [`scoreboard/`](./scoreboard/) | UX proposals for the public scoreboard. |
| [`slidev-theme-credimi/`](./slidev-theme-credimi/) | Slidev theme matching the brand. |
| [`uploads/prototypes/`](./uploads/prototypes/) | Original Figma exports — reference only. |

---

## Versioning & contribution

- **This document is the spec.** When it conflicts with a one-off implementation, the document wins.
- Propose changes via PR. Anyone modifying the palette, type scale, or component primitives needs sign-off from Design + Engineering.
- When a new component graduates from prototype → production, add it to [§10](#10-components) and ship a worked example into `ui_kits/webapp/`.
- Tokens are the source of truth. Never inline a hex or a px value that already has a token.

---

_Maintained by Forkbomb BV · Last updated: 20 May 2026_
