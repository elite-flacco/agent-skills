# Set Up Tailwind Design System

**Goal**
Set up a maintainable design system using Tailwind CSS + a small layer of custom CSS classes.

## Instructions

1. Install Tailwind CSS if needed
2. Create a new design system following the details and examples below

## Constraints

- Use CSS variables as single source of truth for tokens.
- Tailwind theme extends must reference the CSS variables (no hard-coded hex, px, or ad-hoc styles).
- Support dark mode via class (.dark on <html>).
- Create placeholders for alternative font families (system default now, easy to swap later).
- Provide base typography for headings/body and component classes for buttons, cards, inputs, selects, textareas, labels, badges.
- No inline styles in components; only Tailwind utilities and the classes defined below.

## Deliverables

(create or update these files):

- tailwind.config.ts
- src/styles/index.css (imports Tailwind layers and defines tokens + components)

## Details & Acceptance Criteria:

- Tailwind darkMode: 'class'.
- Token model via CSS vars (HSL for colors):
    - --background, --foreground
    - --muted, --muted-foreground
    - --primary, --primary-foreground
    - --secondary, --secondary-foreground
    - --accent, --accent-foreground
    - --destructive, --destructive-foreground
    - --success, --success-foreground
    - --warning, --warning-foreground
    - --border, --input, --ring
    - Fonts: --font-sans, --font-serif, --font-mono (default to system fonts; leave TODO comments for swapping)
    - Spacing scale delegated to Tailwind; can add aliases if needed.

- Extend Tailwind theme to map colors to these vars, e.g. primary.DEFAULT: 'hsl(var(--primary))'.
- Component classes in @layer base (typography reset) and @layer components:
    - .btn (base), .btn-primary, .btn-secondary, .btn-ghost, .btn-destructive, .btn-outline
    - .card, .card-header, .card-body, .card-footer
    - .input, .textarea, .select, .label, .badge

- Respect prefers-reduced-motion for transitions.
- No raw hex/rgba anywhere—only hsl(var(--token)) and Tailwind spacing/typography.
- Include a short “How to change fonts/colors later” section as code comments.


## Example

1. tailwind.config.ts

```ts

import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './src/**/*.{ts,tsx,js,jsx}',
    './pages/**/*.{ts,tsx,js,jsx}',
    './components/**/*.{ts,tsx,js,jsx}',
    './app/**/*.{ts,tsx,js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        success: {
          DEFAULT: 'hsl(var(--success))',
          foreground: 'hsl(var(--success-foreground))',
        },
        warning: {
          DEFAULT: 'hsl(var(--warning))',
          foreground: 'hsl(var(--warning-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        xs: 'var(--radius-xs)',
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
        '2xl': 'var(--radius-2xl)',
        full: 'var(--radius-full)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        serif: 'var(--font-serif)',
        mono: 'var(--font-mono)',
      },
      boxShadow: {
        card: '0 1px 2px rgba(0,0,0,0.06), 0 1px 1px rgba(0,0,0,0.04)',
        focus: '0 0 0 4px hsl(var(--ring) / 0.35)',
      },
      transitionTimingFunction: {
        'soft-out': 'cubic-bezier(.22,.61,.36,1)',
      },
    },
  },
  plugins: [],
}
export default config

```

2. src/styles/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ==========================================================================
   Design Tokens (CSS Variables)
   Swap values here; Tailwind reads them via theme.extend
   ========================================================================== */
@layer base {
  :root {
    /* Background & foreground */
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;

    /* Muted */
    --muted: 210 20% 96%;
    --muted-foreground: 215 16% 47%;

    /* Brand */
    --primary: 266 86% 52%;
    --primary-foreground: 0 0% 100%;

    --secondary: 24 92% 52%;
    --secondary-foreground: 0 0% 100%;

    --accent: 206 100% 50%;
    --accent-foreground: 0 0% 100%;

    /* Danger */
    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;

    /* Success */
    --success: 145 100% 50%;
    --success-foreground: 0 0% 100%;

    /* Warning */
    --warning: 26 100% 52%;
    --warning-foreground: 0 0% 100%;

    /* UI */
    --border: 214 32% 91%;
    --input: 214 32% 91%;
    --ring: 266 86% 52%;

    /* Radii */
    --radius-xs: 0.125rem;
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-2xl: 1.25rem;
    --radius-full: 9999px;

    /* Fonts */
    --font-sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto,
      Arial, "Noto Sans";
    --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
      "Liberation Mono";
  }

  .dark {
    --background: 222 47% 11%;
    --foreground: 210 20% 98%;

    --muted: 223 10% 20%;
    --muted-foreground: 215 16% 70%;

    --primary: 266 86% 60%;
    --primary-foreground: 222 47% 11%;

    --secondary: 24 92% 58%;
    --secondary-foreground: 222 47% 11%;

    --accent: 206 100% 56%;
    --accent-foreground: 222 47% 11%;

    --destructive: 0 84% 66%;
    --destructive-foreground: 222 47% 11%;

    --success: 145 100% 56%;
    --success-foreground: 222 47% 11%;

    --warning: 26 100% 56%;
    --warning-foreground: 222 47% 11%;

    --border: 223 10% 25%;
    --input: 223 10% 25%;
    --ring: 266 86% 60%;
  }

  /* Base document styles via Tailwind utilities */
  html,
  body {
    @apply bg-background text-foreground font-sans antialiased;
  }
  h1 {
    @apply scroll-m-20 text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight leading-tight;
  }
  h2 {
    @apply scroll-m-20 text-2xl sm:text-3xl md:text-4xl font-semibold tracking-tight leading-snug;
  }
  h3 {
    @apply scroll-m-20 text-xl sm:text-2xl md:text-3xl font-semibold leading-snug;
  }
  h4 {
    @apply scroll-m-20 text-lg sm:text-xl md:text-2xl font-medium leading-snug;
  }
  h5 {
    @apply scroll-m-20 text-base sm:text-lg font-medium leading-normal;
  }
  h6 {
    @apply scroll-m-20 text-sm sm:text-base font-medium leading-normal;
  }
  p {
    @apply text-xs sm:text-sm md:text-base leading-relaxed text-muted-foreground;
  }
  span {
    @apply text-xs text-muted-foreground;
  }
  a {
    @apply underline-offset-4 hover:underline hover:text-primary;
  }
  hr {
    @apply border-border;
  }

  /* Buttons default pointer */
  button,
  [type="button"],
  [type="submit"],
  [role="button"] {
    @apply cursor-pointer;
  }
}

/* ============================================================
   2) Components (all color/shape via @apply)
   ============================================================ */
@layer components {
  /* Buttons */
  .btn {
    @apply cursor-pointer inline-flex items-center justify-center gap-2 whitespace-nowrap
           rounded-md px-4 py-2 text-sm font-medium
           transition-colors duration-150
           focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
           disabled:opacity-50 disabled:cursor-not-allowed;
  }
  .btn-primary {
    @apply btn bg-primary text-primary-foreground hover:bg-primary/90 active:bg-primary/85;
  }
  .btn-secondary {
    @apply btn bg-secondary text-secondary-foreground hover:bg-secondary/90 active:bg-secondary/85;
  }
  .btn-accent {
    @apply btn bg-accent text-accent-foreground hover:bg-accent/90 active:bg-accent/85;
  }
  .btn-destructive {
    @apply btn bg-destructive text-destructive-foreground hover:bg-destructive/90 active:bg-destructive/85;
  }
  .btn-ghost {
    @apply btn bg-transparent text-foreground hover:bg-muted/70 active:bg-muted;
  }
  .btn-outline {
    @apply btn border border-border bg-transparent text-foreground hover:bg-muted active:bg-muted;
  }
  .btn-sm {
    @apply btn h-8 px-3 text-xs;
  }
  .btn-lg {
    @apply btn h-11 px-6 text-base;
  }

  /* Card */
  .card {
    @apply p-4 bg-background text-foreground border border-border rounded-lg shadow-md;
  }
  .card-header {
    @apply p-4 border-b border-border;
  }
  .card-body {
    @apply p-4;
  }
  .card-footer {
    @apply p-4 border-t border-border;
  }
  .card.hoverable {
    @apply transition-shadow transition-colors hover:shadow-lg hover:border-border/80;
  }

  /* Form controls */
  .label {
    @apply mb-1 block text-sm font-medium text-foreground;
  }
  .input,
  .textarea,
  .select {
    @apply w-full rounded-md border border-input bg-background text-foreground
           px-3 py-2 text-sm shadow-sm transition-colors
           focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-ring
           placeholder:text-muted-foreground;
  }
  .input:hover,
  .textarea:hover,
  .select:hover {
    @apply border-foreground/20;
  }
  .input {
    @apply h-10;
  }
  .textarea {
    @apply min-h-[120px] resize-y;
  }
  .select {
    @apply h-10;
  }

  /* Badge */
  .badge {
    @apply inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium bg-muted text-muted-foreground;
  }
}

/* ============================================================
   3) Utilities (optional extras)
   ============================================================ */
@layer utilities {
  .elev-0 {
    box-shadow: none;
  }
  .elev-1 {
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  }
  .elev-2 {
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  }
}

/* Accessibility: respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

/* HOW TO SWAP FONTS LATER:
   1) Install fonts (e.g., via @next/font, Google Fonts, or self-host w/ @font-face).
   2) Update the tokens:
      :root { --font-sans: "YourBrandSans", ui-sans-serif, system-ui, ...; }
   3) Done. All components will pick it up automatically.
*/

```
