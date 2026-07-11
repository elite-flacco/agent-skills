---
name: explore-design-variations
description: Use when the user wants multiple visual variations of a UI (e.g. landing page, dashboard, button) to explore different design directions — e.g. asks for "design variations", "alternatives", "explore styles", "a few takes on", "redesign", "mockups", "show me options", or wants variations side-by-side in the browser.
---

# Explore Design Variations

Create different visual variations of UI components (e.g. landing page, dashboard, or button designs). Each variation must be accessible via its own temporary route so users navigate between them in the browser (no git worktrees, no toggling).

## Tech Assumptions
- Next.js App Router (app/ directory)
- TypeScript + React
- Tailwind (or existing styling approach in repo)
- Use ONLY existing dependencies unless you must add one (if you do, explain why and keep it minimal)

## Requirements
1) Inspect the repo quickly to confirm:
    - Next.js app router exists
    - styling system (Tailwind or other)
2) Create a new route group: app/variants/(ui)/...
3) Add an index page at: app/variants/page.tsx that lists links to all variations with a simple grid of “Variant 01…”.
4) Implement the routes, e.g. 10 routes:
   - app/variants/v01/page.tsx
   - app/variants/v02/page.tsx
   ...
   - app/variants/v10/page.tsx
5) Each variant should differ meaningfully in style/layout/content. Push diversity:
   - copy
   - overall aesthetics
   - typography scale + hierarchy
   - spacing + grid system
   - hero treatment (image/illustration placeholder ok)
   - navigation style
   - card styles / borders / shadows
   - subtle motion/hover states (no heavy animation)
   - light/dark compatibility if the repo supports it
6) Keep the variants DRY:
   - Create a shared data model (e.g., content object) in app/variants/_data.ts
   - Create shared small primitives in app/variants/_components (e.g., Section, StatCard) if helpful
   - Variants should primarily differ in composition + styling, not copy
7) Add a tiny “VariantNav” component rendered on every variant page:
   - previous/next
   - link back to index
   - show current variant label
8) Do NOT break existing routes. Keep everything isolated under /variants.
9) Provide a short summary of what you created, plus the exact routes to visit.
