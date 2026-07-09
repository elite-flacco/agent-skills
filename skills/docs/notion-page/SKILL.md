---
name: notion-page
description: Use when the user asks to create or update a Notion page, write formatted content into Notion, add Notion blocks (toggles, callouts, tables, columns, mentions, media), or persist research/docs to a Notion database.
---

# Create Notion Page

Create well-formatted Notion pages from markdown content with proper block structure and rich formatting.

## When to Read What

- **Always follow** — the workflow below.
- **Read when converting content / building API calls** — `references/block-conversion.md` (markdown→block type table, inline formatting, rich-text JSON, MCP parameter formats, known serialization bug + workarounds, error handling).
- **Read when structuring a specific page type** — `references/common-patterns.md` (ready-made templates: job posting, meeting notes, project doc, research notes, decision log, weekly update, technical doc, personal notes).

## Workflow

1. **Determine the parent location**
   - User gives a parent page ID → use it directly.
   - User gives a name/search term → find it with `mcp__notion__API-post-search`; present options if multiple match.
   - No parent specified → create at workspace root.

2. **Get the content**
   - Extract the title from the request.
   - Content inline, from a file path, or empty page? Read the file if a path is mentioned; ask if unclear.

3. **Parse markdown → Notion blocks**
   - Convert headings/paragraphs/lists/code/quotes/dividers to the matching Notion block types.
   - Preserve inline formatting (bold, italic, code, links, strikethrough).
   - Handle nested structures (nested lists, toggle content).
   - See `references/block-conversion.md` for the full type mapping and JSON shapes.

4. **Create the page**
   - `mcp__notion__API-post-page` with title + parent.
   - For database pages, include required properties (check schema with `mcp__notion__API-retrieve-a-data-source`).
   - Add content via `mcp__notion__API-patch-block-children`.

5. **Confirm** — return the created page URL and a short summary (title, parent location, blocks added).

## Custom Syntax Supported

- `> [!toggle] Title` → collapsible toggle block
- `> [!note]` / `> [!warning]` → callout blocks

## Tips

- Verify integration permissions with a simple test page first.
- For very large markdown files, consider splitting across multiple pages.
- Stick to common markdown syntax for the most reliable conversion.
- If `post-page` hits the parent-serialization bug, use the workarounds in `references/block-conversion.md`.
