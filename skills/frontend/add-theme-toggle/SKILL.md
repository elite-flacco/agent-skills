---
name: add-theme-toggle
description: Use when the user asks to add a theme toggle, dark mode, light/dark color scheme switch, or a theme provider to a Next.js app — e.g. "add a dark mode toggle", "add next-themes", "support light/dark theme", "add a color-scheme switcher", "add next-themes ThemeProvider".
---

# Add Theme Toggle

Add a dark mode / theme toggle to a Next.js app using `next-themes`. The default is a minimal two-state button (light/dark flip). If the user wants an explicit System option or a dropdown menu, use the dropdown variant in `references/dropdown-toggle.md` instead. Place the toggle in the app header or wherever the user requests.

## Prerequisites

- Next.js 13+ with App Router (recommended) or Pages Router
- Tailwind CSS configured with `darkMode: 'class'`
- shadcn/ui (the toggle below uses `Button` from `@/components/ui/button`). If the project doesn't use shadcn/ui, replace it with a plain `<button>`. The dropdown variant additionally needs `DropdownMenu`. Confirm with the user before introducing a new UI dependency.

## Installation

```bash
npm install next-themes
```

## Implementation

### 1. ThemeProvider wrapper

Create `components/theme-provider.tsx`:

```tsx
"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

### 2. Wrap the app

Update `app/layout.tsx`. The `suppressHydrationWarning` on `<html>` is **required** — `next-themes` sets the class before hydration and React will warn without it.

```tsx
import { ThemeProvider } from "@/components/theme-provider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### 3. Theme toggle component (default: simple two-state)

Create `components/theme-toggle.tsx`. A minimal sun/moon button that flips between light and dark. This is the default — it guards on `mounted` because it reads `theme` to render conditional icons; see `references/next-themes-api.md` for the hydration pattern.

```tsx
"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="outline" size="icon" disabled>
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      </Button>
    );
  }

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      {theme === "dark" ? (
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      ) : (
        <Moon className="h-[1.2rem] w-[1.2rem]" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

For a dropdown variant (Light / Dark / System menu) — e.g. when the user wants an explicit System option or asks for the shadcn/ui "official" toggle — see `references/dropdown-toggle.md`.

### 4. Tailwind configuration

For Tailwind v3, set `darkMode: "class"` in `tailwind.config.ts`.

For Tailwind v4, add to your CSS:

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

## Going Further

For the full `ThemeProvider` props table, the `useTheme` hook API, custom multi-theme setups (e.g. light/dark/blue/purple), and the hydration/`mounted` pattern for components that read `resolvedTheme`, see `references/next-themes-api.md`.
