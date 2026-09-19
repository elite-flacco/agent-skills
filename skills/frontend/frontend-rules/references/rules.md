# Frontend Rules — Design System Rules

The complete rule set. The parent `SKILL.md` owns routing; these sections are the rules to follow — and the payload to paste into subagent prompts (see Subagent Handoff there).

## 1. Tailwind Color Rules

- **Never** use Tailwind's default color palette directly: `text-gray-500`, `bg-blue-200`, `border-red-300`, etc.
- **Always** use semantic tokens: `text-muted-foreground`, `bg-card`, `border-border`, etc.
- If a semantic token doesn't exist for the use case, add it to `:root` in `globals.css` and map it in `@theme inline` first.
- **Colorful badges/tags/category indicators**: use the `.badge-1` through `.badge-5` component classes (backed by `--badge-{n}` / `--badge-{n}-foreground` tokens). Never use raw palette colors like `bg-teal-100 text-teal-800`. Map categories to badge numbers in a `Record<Category, string>` constant.

## 2. No Arbitrary Values

- **Never** use Tailwind arbitrary values: `text-[32px]`, `mt-[22px]`, `text-[#333]`, `w-[420px]`
- **Never** use `text-[length:var(--text-xs)]` or similar to reference typography tokens. The fluid type scale lives in unlayered `:root` `--text-*` clamp() variables (see the `fluid-typography` skill), which override Tailwind's theme values — so `text-xs`, `text-sm`, `text-lg`, etc. already use the project's fluid scale. Use them directly.
- If a value isn't in the design system, add it as a token. Then use the token.

## 3. No Inline Styles

- **Never** use `style={{ }}` on any element — one-offs included. Use `className` with Tailwind utility classes or `@layer components` classes referencing design tokens. Inline styles bypass the design system (no token, no dark-mode flip, no responsive/hover variants), so always route styling through `className` even for a single use.
- **Only real exception: runtime-computed values.** A value derived from data/state that no utility class can express — e.g. `width: ${pct}%` for a progress bar, a drag transform, a dynamic grid span — may use `style={{ }}` (or set a CSS var via style), since it cannot be a static class. This is not an out for static one-off values; those go in `className`.
- **Library APIs that require style props** (e.g. Recharts chart sizing) follow the same exception — pass what the API demands, nothing more.

## 4. Where Styling Goes

Pick a value's home by reuse, not convenience — this is what keeps the design system lean.

- **One-off (single consumer):** write Tailwind utility classes directly in `className`. Don't use `style={{ }}` (Section 4), and don't mint a token or `@layer components` class for one use — a single-use token or class is overhead with no payoff. This is where one-off patterns belong.
- **Reusable value (genuinely shared):** add it to the design system — a `:root` token mapped in `@theme inline`, and a `@layer components` class when it's a repeating pattern (Section 8 sets the 3+ threshold).
- **Order of preference:** existing token/class → utility classes in `className` (one-offs) → new token/class (reusable values).

> Where this skill says a pattern "stays inline," it means *utility classes written in `className`* — never `style={{ }}`.

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

## 7. Component Classes (Add & Remove)

- **Check `@layer components` first** before writing a utility combination in `className`. If `.btn`, `.card`, `.badge` etc. exist, use them.
- **Extract to `@layer components`** when a utility combination repeats 3+ times across the codebase. Below that threshold, keep it as utility classes in `className` (Section 5) — don't mint a class for one consumer.
- **Remove classes your changes have orphaned.** When you delete, refactor, or stop using a component, any `@layer components` class (`.btn-link`, `.card-meta`, `.badge-active`, …) or `@layer utilities` helper (`.elev-1`, `.lead`, `.muted`, …) with zero remaining references is dead weight — delete it from `globals.css`. This keeps the design system from accumulating cruft.
  - **Search the whole project first.** Confirm zero hits for the class name (and variant selectors like `.btn-link:hover`) before deleting. Don't trust just the file you edited.
  - **Trace dynamic usage.** Classes built from template literals, `cn(...)`/`clsx`, string concatenation, or `Record` maps (e.g. the badge `Record<Category, string>` lookups) won't match a literal search — verify those paths before concluding a class is unused.
  - **Drop now-unused tokens too.** If you removed the last consumer of a token you introduced (an extra `--badge-6`, a one-off `--text-*`), delete it from `:root`/`.dark` and its `@theme inline` line. Leave the curated shared tokens untouched.
  - **If you can't fully verify, don't delete speculatively.** "May not be used anymore" is not enough — leave it and flag it for review instead of guessing.

## 8. Component Reuse Before Duplication

The same "reuse first, extract when it repeats" principle from Section 8 applies at the React component layer — not just CSS classes.

- **Audit before you build.** Before writing a new component, search the project's component directories (`components/`, `ui/`, feature folders) for one that already does the job, and reuse it. Common shapes — a preset date-range filter, an empty state, a stat card, a data-table column header — usually already exist somewhere.
- **Extract a shared component instead of copy-pasting.** When the same UI and logic is needed in a second place (e.g. a date-range filter that already exists on one tab is now needed on another), lift it into a reusable component and import it from both. Duplicated JSX drifts out of sync; a shared component doesn't. (Components extract on the second real use — earlier than the 3+ threshold for CSS classes in Section 8.)
- **Generalize via props, not forks.** If an existing component is almost right, extend it with a prop or variant instead of duplicating and editing the copy.
- **Extract at the right boundary.** Genuinely shared components go in the project's shared component dir; route/page-specific pieces stay colocated with their route. If two features share only a sub-piece, extract just that piece.
- **Don't pre-extract for a single consumer.** A single call site stays colocated where it's used — extract when the second use is real or imminent, not speculatively.

## 9. Border Radius

- **Default to `rounded-md`** (0.375rem) for interactive elements, inputs, and general containers. Never use bare `rounded` (0.25rem) — it's inconsistent with the component classes (`.btn`, `.input`, `.card` all use `rounded-md` or larger).
- `rounded-lg` for cards, panels, and larger containers (already in `.card`).
- `rounded-full` for badges, pills, and avatars (already in `.badge`).

## 10. Button Classes

- **Always** pair `btn` base with a variant: `btn btn-primary`, `btn btn-ghost`, `btn btn-outline`, `btn btn-link`. Never use a variant class without the `btn` base.
- **Only use `btn` on actual action buttons** — not on interactive list items, nav items, card containers, or chip/pill elements that happen to be `<button>` for accessibility.
  - Sidebar nav items, dropdown menu rows, clickable cards → use appropriate layout utilities or `.card`, not `.btn`.
  - Badge-style interactive elements → use `.badge` + variant, not `.btn`.
  - If a button pattern repeats 3+ times and doesn't fit an existing class, extract a new component class (e.g. `.btn-link` for text-style back buttons).

## 11. TypeScript

- **Always** use TypeScript for Next.js apps. Never scaffold with `--js` or plain JavaScript.
- Prop interfaces for every component. `Record<string, T>` for dynamic key maps.

## 12. Visual Verification

After making UI changes:

1. Open the affected route in a browser and confirm the requested change is visibly rendered.
2. Check desktop and mobile viewport widths, including nearby layout, wrapping, overflow, and scrolling.
3. Exercise changed interactions and relevant states such as hover, focus, loading, empty, error, and disabled states.
4. Check the browser console for errors introduced by the change.
5. Compare the rendered result with the user's acceptance criteria and iterate until it satisfies them.

Prefer the in-app browser for visual inspection. Use Agent Browser when repeatable navigation or interaction checks are useful. If the app cannot run, report the blocker and clearly distinguish code-only checks from completed visual verification.

## Quick Self-Check Before Committing

- [ ] No `text-{color}-{shade}` or `bg-{color}-{shade}` from Tailwind's default palette
- [ ] No `text-[...]`, `mt-[...]`, or any other arbitrary value (including `text-[length:var(...)]`)
- [ ] No `style={{ }}` except for runtime-computed values that no class can express (or library APIs like Recharts that require it); one-offs use `className` utilities, not a minted token/class
- [ ] No redundant `text-sm` on `<p>` or `text-xs` on `<span>` (base already applies these)
- [ ] No `dark:` variants
- [ ] Colorful badges use `.badge-1` through `.badge-5`, not raw palette colors
- [ ] All `btn-*` variants paired with `btn` base class
- [ ] `btn` only used on action buttons, not nav items or card containers
- [ ] Repeated patterns extracted to `@layer components`
- [ ] Existing reusable components checked before building new ones; duplicated JSX lifted into a shared component on the second real use, not copy-pasted
- [ ] Component classes and tokens orphaned by your changes verified unused and removed from `globals.css` (whole-project search; dynamic usage traced; unverified left flagged, not deleted)
- [ ] TypeScript throughout
- [ ] Changed UI verified in the browser at desktop and mobile widths
- [ ] Relevant interactions and states work without new console errors
