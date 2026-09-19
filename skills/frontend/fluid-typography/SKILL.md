---
name: fluid-typography
description: Use when the user wants fluid or responsive typography that scales smoothly with viewport size in a Tailwind project — e.g. asks for "fluid type", "responsive font sizes", clamp()-based scaling, or wants to eliminate font-size jumps across breakpoints.
---

# Fluid Typography

Implement fluid typography using CSS `clamp()`: font sizes scale smoothly between a min and max based on viewport width, eliminating breakpoint-based font-size jumps.

## When to Read What

- **Always use** — the default scale and the migration flow below.
- **Read when migrating existing code** — `references/migration.md` (fixed→fluid mapping table, Tailwind v3/v4 config, CSS-in-JS examples, custom-value formula, testing checklist).
- **Copy directly** — `references/scale.css` (drop-in `:root` tokens + heading rules).

## Default Scale

Conservative, readable defaults. Viewport range 320px → 1200px:

| Token | Range | clamp() |
|-------|-------|---------|
| `--text-xs` | 12→14px | `clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)` |
| `--text-sm` | 14→16px | `clamp(0.875rem, 0.825rem + 0.25vw, 1rem)` |
| `--text-base` | 16→18px | `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)` |
| `--text-lg` | 18→20px | `clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)` |
| `--text-xl` | 20→24px | `clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)` |
| `--text-2xl` | 24→30px | `clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)` |
| `--text-3xl` | 30→36px | `clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)` |
| `--text-4xl` | 36→48px | `clamp(2.25rem, 1.95rem + 1.5vw, 3rem)` |
| `--text-5xl` | 48→64px | `clamp(3rem, 2.55rem + 2.25vw, 4rem)` |

Full `:root` block (with line-heights and heading rules): `references/scale.css`.

## Implementation

### New project — add the scale
1. Copy the tokens from `references/scale.css` into the project's design-system layer (`globals.css` / `:root`).
2. Apply `font-size: var(--text-base)` to `body`; map headings to tokens (h1→`--text-4xl`, h2→`--text-3xl`, etc. — see `references/scale.css`).

### Existing project — migrate fixed/breakpoint sizes
1. **Audit** — `grep -rn "font-size:" src/` and find `@media` font-size overrides.
2. **Map** each fixed size to the nearest token using the table in `references/migration.md`.
3. **Replace** fixed sizes + remove the media queries. One breakpoint block → one `var(--text-*)`.
4. **Edge cases** — keep elements that must stay fixed (e.g. logos) as-is, or define a custom `clamp()` using the formula in `references/migration.md`.
5. **Framework config** — for Tailwind v3/v4, set the `fontSize` tokens per `references/migration.md`. For CSS-in-JS, inline the `clamp()` value.
6. **Test** across viewport widths using the checklist in `references/migration.md`.

## Best Practices

- Body text: 16–18px max for readability; never below 16px.
- Headings: scale more aggressively than body.
- Pair with `max-width: 65ch` for measure.
- `clamp()` has full support in all modern browsers (Chrome 79+, Firefox 75+, Safari 13.1+). Where `clamp()` is unsupported the whole declaration is dropped, so provide a plain `font-size` fallback declaration before it when supporting old browsers.

## Resources

- Fluid Type Scale Calculator — https://modern-fluid-typography.vercel.app/
- Utopia Fluid Type — https://utopia.fyi/type/calculator/
- clamp() Calculator — https://clamp.font-size.app/
