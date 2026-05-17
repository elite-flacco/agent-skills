---
name: fluid-typography
description: Implement fluid typography with tailwind
---

# Fluid Typography Skill

## Overview
This skill implements fluid typography using modern CSS `clamp()` with conservative, readable default values that follow contemporary web design standards.

## Core Concept
Fluid typography scales smoothly between minimum and maximum sizes based on viewport width, eliminating the need for breakpoint-based font size changes.

## Modern Default Scale
Conservative, readable defaults for modern web applications:

```css
/* Base font size: 16px (browser default) */

--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);    /* 12px → 14px */
--text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);     /* 14px → 16px */
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);    /* 16px → 18px */
--text-lg: clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);  /* 18px → 20px */
--text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);      /* 20px → 24px */
--text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);   /* 24px → 30px */
--text-3xl: clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem); /* 30px → 36px */
--text-4xl: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);       /* 36px → 48px */
--text-5xl: clamp(3rem, 2.55rem + 2.25vw, 4rem);         /* 48px → 64px */
```

## Updating Existing Styling

When converting existing fixed or breakpoint-based typography to fluid typography, follow this systematic approach:

### Step 1: Audit Current Typography
Identify all font-size declarations in your codebase:
```bash
# Find all font-size declarations
grep -r "font-size:" your-css-files/
```

Common patterns to look for:
- Fixed sizes: `font-size: 16px;` or `font-size: 1rem;`
- Breakpoint-based: `@media (min-width: 768px) { font-size: 18px; }`
- Utility classes: `.text-lg { font-size: 18px; }`

### Step 2: Map to Fluid Scale
Convert your existing sizes to the nearest fluid typography value:

```
Existing → Fluid Replacement
─────────────────────────────
12px → var(--text-xs)   or clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)
14px → var(--text-sm)   or clamp(0.875rem, 0.825rem + 0.25vw, 1rem)
16px → var(--text-base) or clamp(1rem, 0.95rem + 0.25vw, 1.125rem)
18px → var(--text-lg)   or clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)
20px → var(--text-xl)   or clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)
24px → var(--text-2xl)  or clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)
30px → var(--text-3xl)  or clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)
36px → var(--text-4xl)  or clamp(2.25rem, 1.95rem + 1.5vw, 3rem)
48px → var(--text-5xl)  or clamp(3rem, 2.55rem + 2.25vw, 4rem)
```

### Step 3: Replace Fixed Sizes
**Before:**
```css
h1 { font-size: 36px; }

@media (min-width: 768px) {
  h1 { font-size: 42px; }
}

@media (min-width: 1024px) {
  h1 { font-size: 48px; }
}
```

**After:**
```css
h1 { font-size: var(--text-4xl); }
/* All media queries removed! */
```

### Step 4: Update Utility Classes
**Before:**
```css
.text-sm { font-size: 14px; }
.text-base { font-size: 16px; }
.text-lg { font-size: 18px; }
.text-xl { font-size: 20px; }

@media (min-width: 768px) {
  .text-sm { font-size: 15px; }
  .text-base { font-size: 17px; }
  .text-lg { font-size: 19px; }
  .text-xl { font-size: 22px; }
}
```

**After:**
```css
.text-sm { font-size: var(--text-sm); }
.text-base { font-size: var(--text-base); }
.text-lg { font-size: var(--text-lg); }
.text-xl { font-size: var(--text-xl); }
/* No media queries needed */
```

### Step 5: Handle Edge Cases

**Preserving exact sizes for specific elements:**
```css
/* If you need a specific size that shouldn't scale */
.logo-text {
  font-size: 24px; /* Keep fixed */
}

/* Or create a custom fluid value for special cases */
.hero-title {
  font-size: clamp(2rem, 1.5rem + 2.5vw, 3.5rem); /* Custom range */
}
```

**Converting complex responsive patterns:**
```css
/* Before: Multi-breakpoint pattern */
.card-title {
  font-size: 18px;
}
@media (min-width: 640px) { .card-title { font-size: 20px; } }
@media (min-width: 1024px) { .card-title { font-size: 22px; } }
@media (min-width: 1280px) { .card-title { font-size: 24px; } }

/* After: Single fluid declaration */
.card-title {
  font-size: clamp(1.125rem, 1.05rem + 0.375vw, 1.5rem); /* 18px → 24px */
}
```

### Step 6: Update Framework Configurations

**Tailwind CSS Migration:**
```javascript
// Before: tailwind.config.js
module.exports = {
  theme: {
    fontSize: {
      'sm': '14px',
      'base': '16px',
      'lg': '18px',
      'xl': '20px',
      '2xl': '24px',
    }
  }
}

// After: tailwind.config.js
module.exports = {
  theme: {
    fontSize: {
      'sm': 'clamp(0.875rem, 0.825rem + 0.25vw, 1rem)',
      'base': 'clamp(1rem, 0.95rem + 0.25vw, 1.125rem)',
      'lg': 'clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)',
      'xl': 'clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)',
      '2xl': 'clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)',
    }
  }
}
```

**CSS-in-JS (Styled Components, Emotion):**
```javascript
// Before
const Heading = styled.h1`
  font-size: 36px;
  
  @media (min-width: 768px) {
    font-size: 42px;
  }
  
  @media (min-width: 1024px) {
    font-size: 48px;
  }
`;

// After
const Heading = styled.h1`
  font-size: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);
`;
```

### Step 7: Testing Checklist
After converting to fluid typography:

- [ ] Test at 320px (smallest mobile)
- [ ] Test at 375px (iPhone SE)
- [ ] Test at 768px (tablet)
- [ ] Test at 1024px (small desktop)
- [ ] Test at 1920px (large desktop)
- [ ] Verify text doesn't break layouts
- [ ] Check line-height ratios still work
- [ ] Ensure accessibility (minimum 16px for body text)
- [ ] Test with browser zoom at 200%
- [ ] Validate against WCAG contrast ratios

### Migration Script Example
```javascript
// Node.js script to help identify candidates for conversion
const fs = require('fs');
const path = require('path');

function findFontSizes(dir) {
  const files = fs.readdirSync(dir);
  const results = [];
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && !file.includes('node_modules')) {
      results.push(...findFontSizes(filePath));
    } else if (file.endsWith('.css') || file.endsWith('.scss')) {
      const content = fs.readFileSync(filePath, 'utf8');
      const matches = content.match(/font-size:\s*[\d.]+(?:px|rem|em)/g);
      
      if (matches) {
        results.push({
          file: filePath,
          sizes: [...new Set(matches)]
        });
      }
    }
  });
  
  return results;
}

// Usage
console.log(JSON.stringify(findFontSizes('./src'), null, 2));
```

## Implementation Pattern

### 1. CSS Custom Properties (Recommended)
```css
:root {
  /* Viewport range: 320px (mobile) to 1200px (desktop) */
  
  /* Body text */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);
  
  /* Headings */
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);
  --text-3xl: clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem);
  --text-4xl: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);
  --text-5xl: clamp(3rem, 2.55rem + 2.25vw, 4rem);
  
  /* Line heights (unitless) */
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}

/* Usage */
body {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}

h1 { font-size: var(--text-4xl); line-height: var(--leading-tight); }
h2 { font-size: var(--text-3xl); line-height: var(--leading-tight); }
h3 { font-size: var(--text-2xl); line-height: var(--leading-snug); }
h4 { font-size: var(--text-xl); line-height: var(--leading-snug); }
h5 { font-size: var(--text-lg); line-height: var(--leading-normal); }

.caption { font-size: var(--text-sm); }
.small { font-size: var(--text-xs); }
```

### 2. Tailwind CSS Integration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontSize: {
        'xs': 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
        'sm': 'clamp(0.875rem, 0.825rem + 0.25vw, 1rem)',
        'base': 'clamp(1rem, 0.95rem + 0.25vw, 1.125rem)',
        'lg': 'clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)',
        'xl': 'clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)',
        '2xl': 'clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)',
        '3xl': 'clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)',
        '4xl': 'clamp(2.25rem, 1.95rem + 1.5vw, 3rem)',
        '5xl': 'clamp(3rem, 2.55rem + 2.25vw, 4rem)',
      }
    }
  }
}
```

### 3. React/JSX Inline Usage
```jsx
// Utility component
const FluidText = ({ size = 'base', children, ...props }) => {
  const sizes = {
    xs: 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
    sm: 'clamp(0.875rem, 0.825rem + 0.25vw, 1rem)',
    base: 'clamp(1rem, 0.95rem + 0.25vw, 1.125rem)',
    lg: 'clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem)',
    xl: 'clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)',
    '2xl': 'clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem)',
    '3xl': 'clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem)',
    '4xl': 'clamp(2.25rem, 1.95rem + 1.5vw, 3rem)',
    '5xl': 'clamp(3rem, 2.55rem + 2.25vw, 4rem)',
  };
  
  return (
    <span style={{ fontSize: sizes[size] }} {...props}>
      {children}
    </span>
  );
};

// Usage
<FluidText size="2xl">Responsive Heading</FluidText>
```

## Customization Guide

### Calculating Your Own Values
Use this formula for custom fluid typography:

```
clamp(MIN, PREFERRED, MAX)

Where PREFERRED = MIN_REM + (MAX_REM - MIN_REM) * (100vw - MIN_VP) / (MAX_VP - MIN_VP)
```

**Simplified formula:**
```
PREFERRED ≈ MIN_REM + ((MAX_REM - MIN_REM) / (MAX_VP - MIN_VP)) * 100vw
```

**Example calculation:**
- Min size: 16px (1rem) at 320px viewport
- Max size: 20px (1.25rem) at 1200px viewport

```
Viewport range: 1200 - 320 = 880px
Size change: 1.25 - 1 = 0.25rem
Rate: 0.25 / 880 = 0.000284 per px
In vw: 0.000284 * 100 = 0.0284vw ≈ 0.03vw per 1%

PREFERRED = 1rem + 0.03vw * (difference calculation)
Simplified: 0.95rem + 0.25vw

Result: clamp(1rem, 0.95rem + 0.25vw, 1.25rem)
```

### Quick Adjustment Parameters
```css
/* Tighter scaling (less size variation) */
--text-base: clamp(1rem, 0.975rem + 0.125vw, 1.0625rem); /* 16px → 17px */

/* More aggressive scaling */
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem); /* 16px → 20px */

/* Custom viewport range (768px to 1440px) */
--text-base: clamp(1rem, 0.882rem + 0.294vw, 1.125rem);
```

## Best Practices

1. **Keep body text conservative**: 16-18px for optimal readability
2. **Scale headings more aggressively**: They can handle larger size ranges
3. **Match line-height to font size**: Smaller text needs more line-height
4. **Test on actual devices**: Simulators don't always reflect real rendering
5. **Consider content width**: Pair with `max-width: 65ch` for readability
6. **Accessibility**: Ensure minimum sizes meet WCAG standards (16px+ for body)

## Complete Example

```css
:root {
  /* Fluid typography scale */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);
  --text-3xl: clamp(1.875rem, 1.65rem + 1.125vw, 2.25rem);
  --text-4xl: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);
  --text-5xl: clamp(3rem, 2.55rem + 2.25vw, 4rem);
  
  /* Fluid spacing (bonus) */
  --space-xs: clamp(0.5rem, 0.45rem + 0.25vw, 0.625rem);
  --space-sm: clamp(0.75rem, 0.7rem + 0.25vw, 1rem);
  --space-md: clamp(1rem, 0.9rem + 0.5vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1.3rem + 1vw, 2.5rem);
  --space-xl: clamp(2rem, 1.6rem + 2vw, 4rem);
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: var(--text-base);
  line-height: 1.6;
  max-width: 65ch;
  margin: 0 auto;
  padding: var(--space-md);
}

h1 {
  font-size: var(--text-4xl);
  line-height: 1.1;
  margin-bottom: var(--space-md);
}

h2 {
  font-size: var(--text-3xl);
  line-height: 1.2;
  margin-bottom: var(--space-sm);
}

p {
  font-size: var(--text-base);
  line-height: 1.6;
  margin-bottom: var(--space-sm);
}

.caption {
  font-size: var(--text-sm);
  color: #666;
}
```

## Browser Support
- **Full support**: All modern browsers (Chrome 79+, Firefox 75+, Safari 13.1+, Edge 79+)
- **Fallback**: Browsers without `clamp()` support will use the middle value
- **Progressive enhancement**: Start with fixed sizes, enhance with clamp()

## Tools & Resources
- **Fluid Type Scale Calculator**: https://modern-fluid-typography.vercel.app/
- **Utopia Fluid Type**: https://utopia.fyi/type/calculator/
- **clamp() Calculator**: https://clamp.font-size.app/
