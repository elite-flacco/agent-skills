---
description: Add Theme Toggle to Next.js using next-themes
---

# Add Theme Toggle

Add dark mode / theme toggle functionality to Next.js applications using next-themes. Always add the button to the app header. If not applicable, ask the user how they want to proceed.

## Prerequisites

- Next.js 13+ with App Router (recommended) or Pages Router
- Tailwind CSS configured with `darkMode: 'class'`

## Installation

```bash
npm install next-themes
```

## Usage

To create a single button toggle, just type:
```
/cc-add-theme-toggle
```

To create a dropdown toggle, type
```
/cc-add-theme-toggle --dropdown
```

## Implementation Steps

### 1. Create ThemeProvider Wrapper Component

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

### 2. Wrap Application with ThemeProvider

Update `app/layout.tsx`:

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

### 3. Create Theme Toggle Component

Do this if user typed `cc-add-theme-toggle --dropdown`, otherwise use the single button option below.

Create `components/theme-toggle.tsx`:

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
        <DropdownMenuItem onClick={() => setTheme("light")}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### 4. Alternative: Simple Toggle Button (No Dropdown)

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

## Tailwind CSS Configuration

Ensure `tailwind.config.ts` has dark mode enabled:

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  // ... rest of config
};

export default config;
```

For Tailwind v4, add to your CSS file:

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

## ThemeProvider Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `attribute` | `string` | `"data-theme"` | HTML attribute to set (`"class"` for Tailwind) |
| `defaultTheme` | `string` | `"system"` | Default theme (`"light"`, `"dark"`, `"system"`) |
| `enableSystem` | `boolean` | `true` | Enable system preference detection |
| `disableTransitionOnChange` | `boolean` | `false` | Disable CSS transitions on theme change |
| `storageKey` | `string` | `"theme"` | localStorage key for persisting theme |
| `themes` | `string[]` | `["light", "dark"]` | List of available themes |
| `forcedTheme` | `string` | - | Force a specific theme (disables switching) |

## useTheme Hook Reference

```tsx
const {
  theme,          // Current theme name
  setTheme,       // Function to set theme
  resolvedTheme,  // Actual rendered theme (useful when theme is "system")
  systemTheme,    // System preference ("light" or "dark")
  themes,         // List of available themes
  forcedTheme,    // Forced theme if set
} = useTheme();
```

## Handling Hydration Mismatch

Always handle the mounted state to avoid hydration mismatches:

```tsx
const [mounted, setMounted] = React.useState(false);

React.useEffect(() => {
  setMounted(true);
}, []);

if (!mounted) {
  return null; // or a skeleton/placeholder
}
```

## Custom Themes Example

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

## Notes

- The `suppressHydrationWarning` on `<html>` is required to prevent React hydration warnings
- Use `resolvedTheme` instead of `theme` when you need the actual rendered theme (important when using "system")
- The theme is persisted in localStorage by default
- Icons require `lucide-react`: `npm install lucide-react`
