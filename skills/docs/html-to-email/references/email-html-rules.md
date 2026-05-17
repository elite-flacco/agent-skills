# Email HTML Compatibility Rules

## Table of Contents
- [Layout](#layout)
- [CSS](#css)
- [Dark Mode](#dark-mode)
- [Outlook Conditionals](#outlook-conditionals)
- [Images](#images)
- [Typography](#typography)
- [Links and Buttons](#links-and-buttons)
- [Gotchas by Client](#gotchas-by-client)

## Layout

### Use tables for all layout
- `<table>`, `<tr>`, `<td>` — the only reliable cross-client layout method
- Never use `<div>` for structural layout (Outlook ignores most div styling)
- Nest tables for multi-column layouts
- Always set `role="presentation"` on layout tables for accessibility
- Always set `cellpadding="0" cellspacing="0" border="0"` on every table
- Set explicit `width` on tables and cells (pixels preferred, % acceptable)

### Structural skeleton
```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="min-width:100%;">
  <tr>
    <td align="center" style="padding:0;">
      <!-- Inner container, 600px max -->
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width:600px;width:100%;">
        <tr>
          <td>
            <!-- Content here -->
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

### Spacing
- Use `padding` on `<td>` elements for spacing (not `margin` — Outlook ignores margin on most elements)
- For vertical spacing between sections, use empty `<td>` with explicit `height` or `padding-top`/`padding-bottom`
- Never use `<br>` for spacing — inconsistent rendering
- For Outlook copy/paste workflows, keep vertical spacer rows tighter than browser-email spacing because pasted Word HTML often expands perceived gaps

## CSS

### Inline all styles
- Move ALL CSS to inline `style=""` attributes on each element
- Gmail (non-Google Workspace) strips `<style>` blocks in the `<head>`
- Keep a `<style>` block as a progressive enhancement (for clients that support it), but never rely on it

### Supported properties (safe everywhere)
```
background-color, border, border-collapse, border-spacing,
color, direction, font-family, font-size, font-style,
font-weight, height, letter-spacing, line-height, margin (limited),
mso-line-height-rule, padding, table-layout, text-align,
text-decoration, text-transform, vertical-align, width,
max-width, min-width
```

### Avoid these properties
```
flexbox (display:flex), grid (display:grid),
position (absolute/relative/fixed), float,
clip-path, filter, backdrop-filter,
CSS variables (var()), calc() (partial support),
box-shadow (Outlook ignores), border-radius (Outlook ignores),
object-fit, gap
```

### Shorthand vs longhand
- Prefer longhand properties: `padding-top:10px; padding-right:20px;` over `padding:10px 20px;`
- Some clients parse shorthand inconsistently

### Reset styles
Include in `<head>` as progressive enhancement:
```css
body, table, td, p, a, li { -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }
table, td { mso-table-lspace:0pt; mso-table-rspace:0pt; }
img { -ms-interpolation-mode:bicubic; border:0; outline:none; text-decoration:none; }
body { margin:0; padding:0; width:100% !important; -webkit-font-smoothing:antialiased; }
```

## Dark Mode

### Meta tags (add to `<head>`)
```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

### CSS in `<style>` block
```css
:root { color-scheme: light dark; supported-color-schemes: light dark; }

@media (prefers-color-scheme: dark) {
  /* Override background colors */
  .email-body { background-color: #1a1a1a !important; }
  .email-container { background-color: #2d2d2d !important; }

  /* Override text colors */
  .dark-text { color: #ffffff !important; }
  .dark-text-secondary { color: #cccccc !important; }

  /* Override link colors */
  .dark-link { color: #6ea8fe !important; }

  /* Swap images if needed */
  .light-img { display: none !important; }
  .dark-img { display: block !important; }
}
```

### Dark mode strategy
- Add `class` attributes to elements that need dark mode overrides (inline styles cannot be overridden by media queries without `!important` + class selectors)
- Use `!important` in dark mode media query rules to override inline styles
- For Outlook (Windows): dark mode inverts colors unpredictably; add `<!--[if mso]>` overrides or use `[data-ogsc]` / `[data-ogsb]` attribute selectors
- Test transparent PNGs — dark backgrounds can make dark-colored logos/text invisible
- Provide light and dark versions of logos/images when possible

### Outlook dark mode specifics
Outlook on Windows uses its own dark mode algorithm that inverts colors. To control this:
```css
/* Outlook.com / Outlook apps dark mode */
[data-ogsc] .dark-text { color: #ffffff !important; }
[data-ogsb] .email-container { background-color: #2d2d2d !important; }
```

## Outlook Conditionals

### MSO conditional comments
```html
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
<tr><td>
<![endif]-->

<!-- Regular content here (uses max-width for other clients) -->

<!--[if mso]>
</td></tr></table>
<![endif]-->
```

### Common Outlook fixes
```html
<!-- Force Outlook to honor width -->
<!--[if mso]>
<style type="text/css">
  table { border-collapse: collapse; }
  .outlook-width { width: 600px; }
</style>
<![endif]-->

<!-- Outlook-specific line-height fix -->
<td style="line-height:24px; mso-line-height-rule:exactly;">

<!-- Prevent Outlook from adding extra spacing to tables -->
<table style="mso-table-lspace:0pt; mso-table-rspace:0pt;">
```

### Outlook copy/paste specifics
- Copy/paste into Outlook compose is not the same as sending finished email HTML; Outlook routes pasted content through the Word editor
- Prefer table-based pills, badges, and chips instead of inline `span` elements when the user plans to paste into Outlook
- Add `mso-padding-alt` to pill-like and button-like `<td>` cells so padding survives paste
- Use conservative spacer rows between stacked cards, often smaller than what looks right in a browser preview
- Prefer explicit table rows for repeated label/title/body stacks when the layout is card-heavy
- If a layout looks correct in browser preview but too loose after paste, reduce spacer-row height before reducing inner card padding

#### Card layout pattern (Outlook paste-safe)
Cards must be a **direct `<td>`** in the row — NOT a nested wrapper `<table>`. Put the border, background, and padding directly on the card row's `<td>`.

Inside the card, use an inner table with explicit spacer rows to separate badge, title, and description. Do NOT use `margin-top` on elements after a table — the Word engine collapses or ignores it unpredictably:

```html
<tr>
  <td class="card-cell" style="background-color:#ffffff; border:1px solid #d4d4d4; border-radius:12px; padding-top:16px; padding-bottom:16px; padding-left:16px; padding-right:16px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="mso-table-lspace:0pt; mso-table-rspace:0pt;">
      <!-- badge row -->
      <tr>
        <td style="padding:0;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate; mso-table-lspace:0pt; mso-table-rspace:0pt;">
            <tr><td style="...; mso-padding-alt:2px 10px 2px 10px; border-radius:9999px;">Badge Label</td></tr>
          </table>
        </td>
      </tr>
      <!-- spacer between badge and title -->
      <tr><td style="height:12px; font-size:12px; line-height:12px; mso-line-height-rule:exactly;">&nbsp;</td></tr>
      <!-- title row -->
      <tr>
        <td style="padding:0; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; font-size:16px; font-weight:500; line-height:20px; mso-line-height-rule:exactly;">
          <a href="URL" target="_blank" style="color:#0a0a0a; text-decoration:none;">Title text</a>
        </td>
      </tr>
      <!-- spacer between title and description -->
      <tr><td style="height:8px; font-size:8px; line-height:8px; mso-line-height-rule:exactly;">&nbsp;</td></tr>
      <!-- description row -->
      <tr>
        <td style="padding:0; font-size:14px; line-height:22px; mso-line-height-rule:exactly; color:#0a0a0a; font-family:Arial,Helvetica,sans-serif;">Description text.</td>
      </tr>
    </table>
  </td>
</tr>
```

Do NOT use `margin-top` on a `<div>` or `<p>` after a `<table>` inside a card — use a spacer `<tr>` instead.

#### Spacer rows (Outlook paste-safe)
Always set matching `height`, `font-size`, and `line-height` on spacer rows. `font-size:0; line-height:0` is unreliable in the Word engine:

```html
<!-- correct -->
<tr><td style="height:8px; font-size:8px; line-height:8px; mso-line-height-rule:exactly;">&nbsp;</td></tr>

<!-- wrong — collapses unpredictably in Word paste -->
<tr><td style="height:8px; font-size:0; line-height:0;">&nbsp;</td></tr>
```

#### Outer wrapper padding
Use `padding:0` on the outer `<td align="center">` and handle top/bottom page padding with explicit spacer rows. Do NOT use `padding-top:40px` on the outer wrapper — Outlook paste can exaggerate this into large white blocks.

### DOCTYPE and XML namespace
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
```

## Images

- Always set `width`, `height`, `alt`, `border="0"`, `display:block` on `<img>` tags
- Use `display:block` to remove phantom spacing below images
- Outlook may not respect `max-width` on images — use MSO conditional for fixed width
- Avoid SVG — Outlook doesn't support it; use PNG or JPG
- Use absolute URLs for image `src` (relative paths won't work in email)
- Retina: serve 2x images, constrain with `width` attribute

```html
<img src="https://example.com/image.png" width="300" height="200" alt="Description" style="display:block;border:0;outline:none;width:300px;max-width:100%;height:auto;" />
```

## Typography

### Safe font stacks
```css
/* Sans-serif */
font-family: Arial, Helvetica, sans-serif;
font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;

/* Serif */
font-family: Georgia, 'Times New Roman', Times, serif;

/* Monospace */
font-family: 'Courier New', Courier, monospace;
```

- Web fonts: use `@import` or `<link>` in `<head>` only as progressive enhancement; always provide a safe fallback
- Set `font-size` in `px` (not `rem`/`em`) for consistency
- Minimum `font-size: 13px` — some mobile clients enforce this anyway
- Use `mso-line-height-rule:exactly` with `line-height` for Outlook

## Links and Buttons

### Bulletproof buttons (table-based)
```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" style="border-radius:4px;background-color:#0066cc;">
      <a href="https://example.com" target="_blank" style="display:inline-block;padding:12px 24px;font-family:Arial,sans-serif;font-size:16px;color:#ffffff;text-decoration:none;border-radius:4px;background-color:#0066cc;">
        Click Here
      </a>
    </td>
  </tr>
</table>
```

### Paste-safe pill badges
Use this pattern for category badges when Outlook paste fidelity matters:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate; mso-table-lspace:0pt; mso-table-rspace:0pt;">
  <tr>
    <td style="font-size:12px; font-weight:500; line-height:16px; padding-top:2px; padding-bottom:2px; padding-left:10px; padding-right:10px; mso-padding-alt:2px 10px 2px 10px; background-color:#fef3c7; color:#92400e; font-family:Arial, Helvetica, sans-serif; border-radius:999px;">
      API Change
    </td>
  </tr>
</table>
```

### VML buttons for Outlook (pixel-perfect rounded corners)
```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://example.com" style="height:44px;v-text-anchor:middle;width:200px;" arcsize="10%" strokecolor="#0066cc" fillcolor="#0066cc">
  <w:anchorlock/>
  <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;">Click Here</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<a href="https://example.com" style="...">Click Here</a>
<!--<![endif]-->
```

### Link styling
- Always set `color` and `text-decoration` inline on `<a>` tags
- Gmail may override link colors — use inline styles
- `target="_blank"` on all links (email clients may add it anyway, but be explicit)

## Gotchas by Client

### Gmail
- Strips `<style>` in `<head>` for non-Google-Workspace accounts
- Adds `u-` prefix to class names — don't rely on class names alone
- Forces own link styling (blue, underline) — inline styles help but may still be overridden
- Clips emails larger than 102KB — keep file size under this

### Outlook (Windows desktop)
- Uses Word rendering engine — most CSS is ignored
- No support for: `background-image` on `<div>`, `border-radius`, `box-shadow`, `max-width` (use MSO conditionals), CSS animations, `float`, `position`
- VML required for background images on table cells
- `line-height` needs `mso-line-height-rule:exactly`
- Extra spacing added to tables without `mso-table-lspace:0pt; mso-table-rspace:0pt`

### Outlook (Mac / Mobile / Web)
- Much better CSS support than Windows desktop
- Still inline styles recommended for consistency
- Outlook.com has its own dark mode behavior (`[data-ogsc]`, `[data-ogsb]`)

### Apple Mail / iOS Mail
- Best CSS support among email clients
- Supports `<style>` blocks, media queries, web fonts
- Auto-links dates, addresses, phone numbers — can be prevented with `<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">`

### Yahoo Mail
- Strips `<style>` from `<head>` but supports `<style>` in `<body>`
- Adds `yiv` prefix to class names
- Generally decent CSS support otherwise
