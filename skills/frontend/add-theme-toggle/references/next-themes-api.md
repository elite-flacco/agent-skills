# next-themes API Reference

Reference for the `next-themes` package used by the `add-theme-toggle` skill. Consult this when you need props beyond the defaults, the `useTheme` hook details, custom (multi-theme) setups, or hydration handling.

## ThemeProvider Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `attribute` | `string` | `"data-theme"` | HTML attribute to set. Use `"class"` for Tailwind. |
| `defaultTheme` | `string` | `"system"` | Default theme (`"light"`, `"dark"`, `"system"`). |
| `enableSystem` | `boolean` | `true` | Enable system preference detection. |
| `disableTransitionOnChange` | `boolean` | `false` | Disable CSS transitions on theme change. |
| `storageKey` | `string` | `"theme"` | localStorage key for persisting theme. |
| `themes` | `string[]` | `["light", "dark"]` | List of available themes. |
| `forcedTheme` | `string` | - | Force a specific theme (disables switching). |

## useTheme Hook

```tsx
const {
  theme,          // Current theme name (may be "system")
  setTheme,       // Function to set theme
  resolvedTheme,  // Actual rendered theme (useful when theme is "system")
  systemTheme,    // System preference ("light" or "dark")
  themes,         // List of available themes
  forcedTheme,    // Forced theme if set
} = useTheme();
```

Use `resolvedTheme` (not `theme`) when you need the actual rendered theme — important when `theme === "system"`.

## Hydration Mismatch

`next-themes` reads localStorage on the client, so the first server render can differ from the client render. Two mitigations:

1. **Always** add `suppressHydrationWarning` to the `<html>` element (shown in the SKILL.md layout example).
2. In components that read `theme`/`resolvedTheme` to drive conditional rendering, guard on a `mounted` flag:

   ```tsx
   const [mounted, setMounted] = React.useState(false);
   React.useEffect(() => { setMounted(true); }, []);
   if (!mounted) {
     return null; // or a skeleton/placeholder
   }
   ```

## Custom (Multi-Theme) Setup

For more than light/dark, pass `themes` plus a `value` map:

```tsx
<ThemeProvider
  attribute="data-theme"
  defaultTheme="blue"
  themes={["light", "dark", "blue", "purple"]}
  value={{
    light: "light",
    dark: "dark",
    blue: "theme-blue",
    purple: "theme-purple",
  }}
>
```

With corresponding CSS:

```css
[data-theme="theme-blue"] {
  --background: 210 100% 12%;
  --foreground: 210 100% 98%;
}

[data-theme="theme-purple"] {
  --background: 270 100% 12%;
  --foreground: 270 100% 98%;
}
```
