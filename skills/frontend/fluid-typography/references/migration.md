# Migration Guide: Fixed → Fluid Typography

## Fixed-to-Fluid Mapping

Use this table to find the token for an existing fixed size.

| Fixed | Token | clamp() value |
|-------|-------|---------------|
| 12px | `--text-xs` | `clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)` |
| 14px | `--text-sm` | `clamp(0.875rem, 0.825rem + 0.25vw, 1rem)` |
| 16px | `--text-base` | `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)` |
| 18px | `--text-lg` | `clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)` |
| 20px | `--text-xl` | `clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)` |
| 24px | `--text-2xl` | `clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)` |
| 30px | `--text-3xl` | `clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)` |
| 36px | `--text-4xl` | `clamp(2.25rem, 1.95rem + 1.5vw, 3rem)` |
| 48px | `--text-5xl` | `clamp(3rem, 2.55rem + 2.25vw, 4rem)` |

## Replacing Breakpoint Patterns

A multi-breakpoint block collapses to a single fluid declaration:

**Before:**
```css
.card-title { font-size: 18px; }
@media (min-width: 640px)  { .card-title { font-size: 20px; } }
@media (min-width: 1024px) { .card-title { font-size: 22px; } }
@media (min-width: 1280px) { .card-title { font-size: 24px; } }
```

**After:**
```css
.card-title { font-size: var(--text-2xl); } /* 24px → 30px, one line */
```

## Tailwind CSS Config

**Tailwind v3** (`tailwind.config.js`):
```javascript
module.exports = {
  theme: {
    extend: {
      fontSize: {
        'xs':   'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
        'sm':   'clamp(0.875rem, 0.825rem + 0.25vw, 1rem)',
        'base': 'clamp(1rem, 0.95rem + 0.25vw, 1.125rem)',
        'lg':   'clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)',
        'xl':   'clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)',
        '2xl':  'clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)',
        '3xl':  'clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)',
        '4xl':  'clamp(2.25rem, 1.95rem + 1.5vw, 3rem)',
        '5xl':  'clamp(3rem, 2.55rem + 2.25vw, 4rem)',
      },
    },
  },
};
```

**Tailwind v4** — define tokens in CSS, then reference via theme:
```css
@import "tailwindcss";

@theme {
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg:   clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);
  --text-xl:   clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  /* ...rest of scale */
}
```

## CSS-in-JS (Styled Components, Emotion)

```javascript
// Before
const Heading = styled.h1`
  font-size: 36px;
  @media (min-width: 768px)  { font-size: 42px; }
  @media (min-width: 1024px) { font-size: 48px; }
`;

// After
const Heading = styled.h1`
  font-size: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);
`;
```

## Calculating Custom Values

```
clamp(MIN, PREFERRED, MAX)
PREFERRED ≈ MIN_REM + ((MAX_REM - MIN_REM) / (MAX_VP - MIN_VP)) * 100vw
```

Worked example — 16px at 320px → 20px at 1200px:
- Viewport range: 1200 − 320 = 880px
- Size change: 1.25 − 1 = 0.25rem
- Rate: 0.25 / 880 ≈ 0.000284 per px → 0.0284vw
- PREFERRED = 0.95rem + 0.25vw
- Result: `clamp(1rem, 0.95rem + 0.25vw, 1.25rem)`

### Quick adjustment presets

```css
/* Tighter scaling (less variation) */
--text-base: clamp(1rem, 0.975rem + 0.125vw, 1.0625rem); /* 16px → 17px */

/* More aggressive scaling */
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);       /* 16px → 20px */

/* Custom viewport range (768px–1440px) */
--text-base: clamp(1rem, 0.882rem + 0.294vw, 1.125rem);
```

## Testing Checklist

- [ ] 320px (smallest mobile)
- [ ] 375px (iPhone SE)
- [ ] 768px (tablet)
- [ ] 1024px (small desktop)
- [ ] 1920px (large desktop)
- [ ] Text doesn't break layouts
- [ ] Line-height ratios still read well
- [ ] Body text ≥ 16px (accessibility)
- [ ] Browser zoom at 200%
- [ ] WCAG contrast ratios hold
