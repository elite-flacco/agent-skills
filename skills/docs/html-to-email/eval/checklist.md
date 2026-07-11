# Email HTML Output Checklist

Verify generated email HTML against this checklist before returning it to the
user. The full rules behind each item live in
`references/email-html-rules.md` — this file is for *verification*, not
authoring.

## Structure
- [ ] XHTML Transitional DOCTYPE with MSO XML namespaces.
- [ ] `<meta>` tags: charset, viewport, color-scheme, format-detection.
- [ ] CSS reset block in `<head>` as progressive enhancement.
- [ ] All layout converted to nested `<table role="presentation">` with `cellpadding="0" cellspacing="0" border="0"`.
- [ ] 100%-width outer table + centered 600px inner table.
- [ ] `background-color` set inline on the outer wrapper table, not just on `<body>`.
- [ ] All `margin` spacing replaced with `padding` on `<td>` elements.
- [ ] No `<br>`-based spacing — padded or fixed-height `<td>` elements instead.

## Styles
- [ ] All CSS inlined onto each element's `style` attribute.
- [ ] `<style>` block in `<head>` kept only for dark-mode media queries and resets.
- [ ] No unsupported properties remain (`flexbox`, `grid`, `position`, `float`, CSS variables, `calc`).
- [ ] Longhand CSS properties used where possible.
- [ ] `mso-table-lspace:0pt; mso-table-rspace:0pt` on all tables.
- [ ] `mso-line-height-rule:exactly` alongside any `line-height`.

## Dark Mode
- [ ] `color-scheme` and `supported-color-schemes` meta tags present.
- [ ] `class` attributes added to elements needing dark-mode overrides.
- [ ] `@media (prefers-color-scheme: dark)` rules with `!important`.
- [ ] Outlook `[data-ogsc]` / `[data-ogsb]` selectors added.
- [ ] Transparent PNGs given appropriate dark-mode treatment.

## Outlook
- [ ] MSO conditional wrappers around the container table for fixed-width fallback.
- [ ] MSO `<style>` block for Outlook-specific fixes.
- [ ] Buttons converted to bulletproof table-based buttons (VML for rounded corners if needed).
- [ ] Any `<div>` background images replaced with VML.

## Outlook Paste Mode (only when the user will copy/paste into Outlook compose)
- [ ] Table-cell pills/badges used instead of inline `span` badges.
- [ ] `mso-padding-alt` added on pill-like or button-like cells.
- [ ] Conservative inter-card spacer rows.
- [ ] **Critical — no `font-size:0; line-height:0` on spacer cells** (see `examples/bad`).
- [ ] Every spacer `<td>` has matched `height`, `font-size`, `line-height`, `mso-line-height-rule:exactly`, and `&nbsp;` inside.
- [ ] No explicit `background-color` on spacer cells (breaks dark-mode adaptation).
- [ ] Card layout as own `<tr>` rows; spacer rows between cards, not `margin-bottom`.

## Images
- [ ] `width`, `height`, `alt`, `border="0"`, `style="display:block"` on every `<img>`.
- [ ] No SVG (replaced with PNG/JPG note where present).
- [ ] All `src` URLs absolute.

## Typography
- [ ] Web fonts replaced with safe font stacks as fallback.
- [ ] Web font `<link>` kept as progressive enhancement if present.
- [ ] All `font-size` in `px`.
- [ ] Minimum font size 13px enforced.

## Links
- [ ] `color` and `text-decoration` set inline on all `<a>` tags.
- [ ] `target="_blank"` on all links.

## Final Checks
- [ ] Total HTML size estimated; warn if approaching Gmail's 102KB clip threshold.
- [ ] No unsupported CSS properties remain.
- [ ] All layout is table-based.
- [ ] Comment at top: `<!-- Email-safe HTML generated from {source-file} -->`.
