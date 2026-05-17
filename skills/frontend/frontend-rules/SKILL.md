---
name: frontend-rules
description: Rules and constraints for all frontend development in Next.js/React/Tailwind projects. INVOKE THIS SKILL before writing or modifying any UI file, component, CSS, or Tailwind class. Also invoke when scaffolding a new frontend project or reviewing existing UI code for compliance.
---

# Frontend Rules

This skill is **rigid** — follow every rule exactly. Do not adapt or skip.

## 1. Design System Setup (Non-Negotiable Sequence)

**New projects:** Invoke the `setup-design-system-tw` skill as a **standalone step before writing any UI code or dispatching any UI subagent.** Subagents receive instructions, not skill invocations — globals.css with semantic tokens must exist before the UI prompt is written.

**Existing projects:** Read `globals.css` before touching anything. Check what tokens and `@layer components` classes already exist. Never add new raw values — add a token first.

## 2. Tailwind Color Rules

- **Never** use Tailwind's default color palette directly: `text-gray-500`, `bg-blue-200`, `border-red-300`, etc.
- **Always** use semantic tokens: `text-muted-foreground`, `bg-card`, `border-border`, etc.
- If a semantic token doesn't exist for the use case, add it to `:root` in `globals.css` and map it in `@theme inline` first.
- **Colorful badges/tags/category indicators**: use the `.badge-1` through `.badge-5` component classes (backed by `--badge-{n}` / `--badge-{n}-foreground` tokens). Never use raw palette colors like `bg-teal-100 text-teal-800`. Map categories to badge numbers in a `Record<Category, string>` constant.

## 3. No Arbitrary Values

- **Never** use Tailwind arbitrary values: `text-[32px]`, `mt-[22px]`, `text-[#333]`, `w-[420px]`
- **Never** use `text-[length:var(--text-xs)]` or similar to reference typography tokens. The `@theme inline` block maps `--font-size-*` to your fluid variables, so `text-xs`, `text-sm`, `text-lg`, etc. already use the project's fluid scale. Use them directly.
- If a value isn't in the design system, add it as a token. Then use the token.

## 4. No Inline Styles

- **Never** use `style={{ }}` on any element.
- Always use Tailwind utility classes or `@layer components` classes referencing design tokens.

## 5. No className on @layer base Elements

- `@layer base` styles h1–h6, p, a, hr, code, span, etc. automatically.
- **Never** add `className` to these elements to re-apply what base already provides. Common redundancies:
  - `<p className="text-sm">` — base `p` is already `text-sm`. Remove `text-sm`.
  - `<span className="text-xs">` — base `span` is already `text-xs`. Remove `text-xs`.
  - Overrides to a **different** size (e.g., `<p className="text-xs">`) are fine — those intentionally change the base.
- Use `.h1`–`.h6` aliases on non-heading elements when you need heading styles.
- For UI chrome that needs non-standard sizing (e.g. a compact app header), use `<p>` or `<div>` with a named `@layer components` class — not a styled `<h1>`.

## 6. No dark: Variants

- **Never** use `dark:text-white`, `dark:bg-gray-900`, etc.
- Dark mode is handled automatically via CSS variable swapping on `.dark`. Semantic tokens already flip. Using `dark:` utilities fights the design system.

## 7. Component Class Extraction

- **Check `@layer components` first** before writing inline utility combinations. If `.btn`, `.card`, `.badge` etc. exist, use them.
- **Extract to `@layer components`** when a utility combination repeats 3+ times across the codebase. One-off patterns stay inline.

## 8. Border Radius

- **Default to `rounded-md`** (0.375rem) for interactive elements, inputs, and general containers. Never use bare `rounded` (0.25rem) — it's inconsistent with the component classes (`.btn`, `.input`, `.card` all use `rounded-md` or larger).
- `rounded-lg` for cards, panels, and larger containers (already in `.card`).
- `rounded-full` for badges, pills, and avatars (already in `.badge`).

## 9. Button Classes

- **Always** pair `btn` base with a variant: `btn btn-primary`, `btn btn-ghost`, `btn btn-outline`, `btn btn-link`. Never use a variant class without the `btn` base.
- **Only use `btn` on actual action buttons** — not on interactive list items, nav items, card containers, or chip/pill elements that happen to be `<button>` for accessibility.
  - Sidebar nav items, dropdown menu rows, clickable cards → use appropriate layout utilities or `.card`, not `.btn`.
  - Badge-style interactive elements → use `.badge` + variant, not `.btn`.
  - If a button pattern repeats 3+ times and doesn't fit an existing class, extract a new component class (e.g., `.btn-link` for text-style back buttons).

## 10. TypeScript

- **Always** use TypeScript for Next.js apps. Never scaffold with `--js` or plain JavaScript.
- Prop interfaces for every component. `Record<string, T>` for dynamic key maps.

## 11. Subagent Handoff (Critical)

Subagents **cannot invoke skills** — they start fresh without access to the Skill tool. When dispatching a subagent (via the Agent tool) to do UI work, you **MUST include the appropriate rules** in the subagent's `prompt` parameter.

### For scaffolding subagents (new project)

Before dispatching, invoke the `setup-design-system-tw` skill yourself, read the CSS template from it, and include it in the subagent prompt:

```
FRONTEND DESIGN SYSTEM — follow these exactly:
1. Use the globals.css template below as the project's global stylesheet. Do NOT create your own.
2. NEVER use Tailwind's default color palette (text-gray-500, bg-blue-200, etc.) — only semantic tokens.
3. NEVER use Tailwind arbitrary values, inline styles, or dark: variants.
4. For colorful badges/tags/category indicators, use .badge-1 through .badge-5 classes only.
5. Always TypeScript — never scaffold with --js.

globals.css template:
<paste the CSS template from the setup-design-system-tw skill here>
```

### For component/page subagents (existing project)

Paste these rules verbatim into the subagent's `prompt` parameter:

```
FRONTEND RULES — follow these exactly:
1. Read globals.css FIRST. Use only the semantic tokens and @layer components classes defined there. This file IS your design system — it contains all available colors, typography, and component classes.
2. NEVER use Tailwind's default color palette (text-gray-500, bg-blue-200, etc.) — only semantic tokens (text-muted-foreground, bg-card, etc.).
3. NEVER use Tailwind arbitrary values (text-[32px], mt-[22px], text-[#333]).
4. NEVER use inline styles (style={{ }}).
5. NEVER add className to h1-h6, p, or other @layer base elements — base styles apply automatically.
6. NEVER use dark: variants — dark mode is handled by CSS variable swapping.
7. For colorful badges/tags/category indicators: globals.css defines exactly 5 badge classes (.badge-1 through .badge-5) with curated colors and dark mode support. Map your categories to these classes using a Record constant. Example:
   const CATEGORY_STYLES: Record<Category, string> = { "type-a": "badge-1", "type-b": "badge-2", ... };
   Then use: <span className={CATEGORY_STYLES[item.category]}>
   NEVER invent badge colors using raw Tailwind palette (bg-teal-100 text-teal-800, etc.).
8. Check @layer components for existing classes (.btn, .card, .badge, etc.) before writing inline utilities.
9. If a token doesn't exist, add it to :root in globals.css and map it in @theme inline — don't use raw values.
10. NEVER use text-[length:var(--text-xs)] or similar — the @theme inline block maps --font-size-* to the fluid scale, so text-xs, text-sm, etc. work directly.
11. Base `p` is already text-sm and base `span` is already text-xs. Don't re-apply those classes on those elements. Overriding to a DIFFERENT size (e.g., text-xs on p) is fine.
12. Always pair btn base with a variant: btn btn-primary, btn btn-ghost, btn btn-outline, btn btn-link. Never use a variant alone. Only use btn on actual action buttons — not on nav items, card containers, or chips.
```

## Quick Self-Check Before Committing

- [ ] No `text-{color}-{shade}` or `bg-{color}-{shade}` from Tailwind's default palette
- [ ] No `text-[...]`, `mt-[...]`, or any other arbitrary value (including `text-[length:var(...)]`)
- [ ] No `style={{ }}` anywhere (exception: third-party library APIs like Recharts that require style props)
- [ ] No redundant `text-sm` on `<p>` or `text-xs` on `<span>` (base already applies these)
- [ ] No `dark:` variants
- [ ] Colorful badges use `.badge-1` through `.badge-5`, not raw palette colors
- [ ] All `btn-*` variants paired with `btn` base class
- [ ] `btn` only used on action buttons, not nav items or card containers
- [ ] Repeated patterns extracted to `@layer components`
- [ ] TypeScript throughout
