---
name: add-theme-toggle
description: Use when the user asks to add a theme toggle, dark mode, or light/dark color scheme switch to a Next.js app — e.g. "add a dark mode toggle", "add next-themes", "support light/dark theme", "add a color scheme switcher".
---

# Add Theme Toggle

Add a dark mode / theme toggle to a Next.js app using `next-themes`. Adds a toggle (dropdown or simple two-state button) that can be placed in the app header or wherever the user wants. If the user doesn't specify which style, default to the dropdown (it exposes the System option); use the simple button when they want a minimal sun/moon switch.

## Prerequisites

- Next.js 13+ with App Router (recommended) or Pages Router
- Tailwind CSS configured with `darkMode: 'class'`
- shadcn/ui (the toggle below uses `Button` and `DropdownMenu` from `@/components/ui/...`). If the project doesn't use shadcn/ui, either install the components you need or replace them with plain elements. Confirm with the user before introducing a new UI dependency.

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

### 3. Theme toggle component

Create `components/theme-toggle.tsx`. This is the dropdown variant (Light / Dark / System). Place it in the header or wherever the user requests.

```tsx
"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function ThemeToggle() {
  const { setTheme } = useTheme();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon">
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>Light</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>Dark</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>System</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### 4. Alternative: simple toggle button

A minimal two-state toggle (just flips between light and dark, no menu). Use this when the user wants a sun/moon icon button rather than a dropdown. Note it guards on `mounted` because it reads `theme` to render conditional icons — see `references/next-themes-api.md` on the hydration pattern.

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

### 5. Tailwind configuration

For Tailwind v3, set `darkMode: "class"` in `tailwind.config.ts`.

For Tailwind v4, add to your CSS:

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

## Going Further

For the full `ThemeProvider` props table, the `useTheme` hook API, custom multi-theme setups (e.g. light/dark/blue/purple), and the hydration/`mounted` pattern for components that read `resolvedTheme`, see `references/next-themes-api.md`.
