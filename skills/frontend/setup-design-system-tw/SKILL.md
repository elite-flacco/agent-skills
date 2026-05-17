---
name: setup-design-system-tw
description: Set up a maintainable Tailwind CSS v4 design system with semantic tokens, fluid typography, badge color palette, and component classes. Invoke this skill when scaffolding a new frontend project or when globals.css doesn't exist yet.
---

# Set Up Tailwind v4 Design System

**Goal**
Set up a maintainable design system in **Tailwind CSS v4** using a two-layer token approach:
- Raw values in `:root` / `.dark` for runtime theming (no rebuild)
- `@theme` to expose them as Tailwind utilities

Includes fluid typography, light/dark mode, base element styles, layout utilities, component classes, and a **constrained badge color palette**.

## Instructions

1. Confirm Tailwind v4 is installed. For Next.js use `@tailwindcss/postcss` — no `tailwind.config.*` needed.
2. Locate the global CSS file (`src/app/globals.css` for Next.js, `src/index.css` for Vite).
3. Copy the reference template from `templates/globals.css` in this skill directory to the project's global CSS file, adapting colors and fonts for the project.
4. Import the stylesheet in the app entry if not already imported.

## Constraints

- **Two-layer token model**: raw values in `:root` / `.dark`, mapped to Tailwind via `@theme`
- **Fluid typography**: all font sizes use `clamp()` — no static px values
- **No `dark:` utility variants** — dark mode works via CSS variable swapping on `.dark`
- **No inline styles, no Tailwind arbitrary values, no raw hex/rgba inside component classes** — component classes use `var(--token)` only
- **`@layer base`** for element resets and typography
- **`@layer components`** for reusable UI patterns
- **Global `*:focus-visible`** defined once in base — not repeated per component
- **`prefers-reduced-motion`** respected
- **Badge colors**: only use the 5 semantic badge tokens (`--badge-{1-5}`) — never raw Tailwind palette colors for badges or category indicators

## Token Model

```
:root / .dark  →  raw values (hex, rgba, clamp)
@theme         →  maps tokens to Tailwind utilities (bg-background, text-foreground, etc.)
```

Tokens:
- `--background`, `--foreground`
- `--muted` (muted background surface), `--muted-foreground` (secondary/dimmed text)
- `--card`, `--card-hover`
- `--border`, `--border-hover`
- `--primary`, `--primary-foreground`
- `--accent` (brand highlight, easily swappable)
- `--badge-1` → `--badge-5` + `--badge-1-foreground` → `--badge-5-foreground` (constrained palette for colorful badges/tags)
- `--text-xs` → `--text-5xl` (fluid clamp values)
- `--leading-tight` → `--leading-loose`
