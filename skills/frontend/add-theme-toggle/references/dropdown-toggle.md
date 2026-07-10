# Dropdown Theme Toggle (Alternative Variant)

A three-option dropdown (Light / Dark / System) instead of the default simple two-state toggle. Use this when the user specifically wants a menu with an explicit System option, or when they ask for the shadcn/ui "official" toggle.

This variant does **not** read `theme` for rendering (the icons cross-fade purely via CSS `dark:` utilities), so it needs no `mounted` guard. The default simple toggle in the SKILL.md does need the guard — see the hydration pattern in `next-themes-api.md`.

## Component

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
        <DropdownMenuItem onClick={() => setTheme("light")}>Light</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>Dark</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>System</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

Requires `DropdownMenu` from shadcn/ui (`@/components/ui/dropdown-menu`). If the project doesn't use shadcn/ui, either add the component or stick with the default simple toggle.
