---
name: setup-design-system
description: Use when the user asks to set up a Tailwind (v3) design system with CSS-variable tokens, dark mode, and component classes.
---

# Set Up Tailwind Design System

Set up a maintainable design system using Tailwind CSS + a small layer of custom CSS classes, with CSS variables as the single source of truth.

> For **Tailwind v4**, use the `setup-design-system-tw` skill instead.

## When to Read What

- **Copy directly** — `templates/tailwind.config.ts` and `templates/index.css` into the project (adapt paths).
- **Always follow** — the constraints and token model below.

## Constraints

- CSS variables are the single source of truth for tokens.
- Tailwind theme extends must reference the CSS variables — no hard-coded hex, px, or ad-hoc styles.
- Support dark mode via class (`.dark` on `<html>`).
- No inline styles in components — only Tailwind utilities and the classes defined below.
- Respect `prefers-reduced-motion`.

## Token Model (HSL)

Color tokens (light defined in `:root`, dark overrides in `.dark`):

`--background`, `--foreground`, `--muted`, `--muted-foreground`, `--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--accent`, `--accent-foreground`, `--destructive`, `--destructive-foreground`, `--success`, `--success-foreground`, `--warning`, `--warning-foreground`, `--border`, `--input`, `--ring`

Plus: `--radius-*` scale, `--font-sans`/`--font-serif`/`--font-mono` (system defaults, with TODO comments for swapping).

## Component Classes

Defined in `@layer components`:

- **Buttons:** `.btn` (base), `.btn-primary`, `.btn-secondary`, `.btn-accent`, `.btn-destructive`, `.btn-ghost`, `.btn-outline`, `.btn-sm`, `.btn-lg`
- **Card:** `.card`, `.card-header`, `.card-body`, `.card-footer`, `.card.hoverable`
- **Forms:** `.label`, `.input`, `.textarea`, `.select`
- **Misc:** `.badge`

## Deliverables

Create or update:

1. **`tailwind.config.ts`** — `darkMode: 'class'`, `theme.extend` mapping colors/borderRadius/fontFamily/boxShadow to the CSS vars. Use `templates/tailwind.config.ts`.
2. **`src/styles/index.css`** — `@tailwind` layers + `:root`/`.dark` tokens + base typography reset + component classes + reduced-motion guard. Use `templates/index.css`.

## Implementation

1. Install Tailwind CSS if not already present.
2. Copy `templates/tailwind.config.ts` → project root (adjust `content` globs to match the project layout).
3. Copy `templates/index.css` → `src/styles/index.css` (or the project's chosen stylesheet path).
4. Import the stylesheet once in the app root (e.g. `app/layout.tsx` or `pages/_app.tsx`).
5. Adapt the brand token values (the `--primary`/`--secondary`/`--accent` HSLs) to the project's palette if known; otherwise the defaults are usable as-is.

## Customization Notes

- **Change fonts later:** install the font, then update `--font-sans` (etc.) in `:root`. All components pick it up automatically — see the comment block at the bottom of `templates/index.css`.
- **Add a new component class:** add it under `@layer components` using only `@apply` with tokens — no raw hex/rgba.
- **Spacing:** delegated to Tailwind's default scale; add aliases only if needed.
