# Markdown → Notion Block Conversion

## Block Types

| Markdown | Notion block `type` |
|----------|---------------------|
| `# H1`, `## H2`, `### H3` | `heading_1`, `heading_2`, `heading_3` |
| paragraph | `paragraph` |
| `- item`, `* item` | `bulleted_list_item` |
| `1. item` | `numbered_list_item` |
| ` ```code``` ` | `code` (preserve language) |
| `> quote` | `quote` |
| `---` / `***` | `divider` |
| `> [!toggle] Title` (custom) | `toggle` (with nested content) |
| `> [!note]`, `> [!warning]` (custom) | `callout` (with appropriate emoji) |

Nested lists/toggles are supported via proper indentation.

## Inline Formatting

| Markdown | rich_text annotation |
|----------|---------------------|
| `**bold**` / `__bold__` | `annotations.bold: true` |
| `*italic*` / `_italic_` | `annotations.italic: true` |
| `` `code` `` | `annotations.code: true` |
| `~~text~~` | `annotations.strikethrough: true` |
| `[text](url)` | `text.link: { url }` |

## Rich Text Object Structure

```json
{
  "type": "text",
  "text": { "content": "Hello world", "link": null },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  }
}
```

## Block JSON Examples

Adding content blocks via `mcp__notion__API-patch-block-children`:

```json
{
  "block_id": "PAGE-UUID-HERE",
  "children": [
    { "type": "heading_1", "heading_1": { "rich_text": [{"type":"text","text":{"content":"Title"}}] } },
    { "type": "paragraph", "paragraph": { "rich_text": [{"type":"text","text":{"content":"Body text"}}] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{"type":"text","text":{"content":"Item"}}] } }
  ]
}
```

## MCP Tool Parameter Formats

### Create page under another page
```
mcp__notion__API-post-page
- parent: {"page_id": "UUID-HERE"}
- properties: {"type": "title", "title": [{"text": {"content": "Page Title"}}]}
```

### Create page in a database
```
mcp__notion__API-post-page
- parent: {"database_id": "UUID-HERE"}
- properties: {"type": "title", "title": [{"text": {"content": "Page Title"}}]}
```

For database pages, include required properties — use `mcp__notion__API-retrieve-a-data-source` to get the schema and valid property values.

### Add content blocks
```
mcp__notion__API-patch-block-children
- block_id: "PAGE-UUID-HERE"
- children: [ ...blocks... ]
```

## Known Issue: parent serialization bug

`mcp__notion__API-post-page` may convert the `parent` object to a string, causing `"body.parent should be an object, instead was string"`. Workarounds (in order):

1. Add content to an existing suitable page via `patch-block-children`.
2. Create the page in a database (different parent structure sometimes works).
3. Have the user create a blank page in Notion, share it with the integration, then populate it with `patch-block-children`.

## Error Handling

- **Invalid parent ID** — page not found; ask user to verify the parent page name/ID.
- **Permission denied** — integration needs access; guide them to share the page/workspace with the integration.
- **Invalid markdown** — report the parsing error; ask for corrected content.
- **Rate limits** — retry with backoff; inform the user if retries keep failing.
- **Database property errors** — explain which properties are required or have invalid values.
- **Page created but content empty** — verify markdown format and block conversion; check the API response.
