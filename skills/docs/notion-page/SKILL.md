---
name: notion-page
allowed-tools: Skill(notion-page), mcp__notion__API-post-search, mcp__notion__API-post-page, mcp__notion__API-patch-block-children, mcp__notion__API-retrieve-a-page, mcp__notion__API-get-block-children, mcp__notion__API-query-data-source, mcp__notion__API-retrieve-a-data-source
description: Create and format Notion pages with proper Notion-flavored Markdown block structure. Use when creating new Notion pages, updating page content, or when the user requests well-formatted documentation in Notion. Handles database pages, standalone pages, and complex block types including toggles, callouts, tables, columns, mentions, and media blocks.
---

# Create Notion Page

Create well-formatted Notion pages with support for markdown content, proper block structure, and rich formatting.

## CRITICAL: MCP Tool Parameter Format

**The Notion MCP tools require specific parameter formats. Follow these patterns exactly:**

### Creating a page under another page (standalone page)

```
mcp__notion__API-post-page with parameters:
- parent: {"page_id": "UUID-HERE"}
- properties: {"type": "title", "title": [{"text": {"content": "Page Title"}}]}
```

### Creating a page in a database

```
mcp__notion__API-post-page with parameters:
- parent: {"database_id": "UUID-HERE"}
- properties: {"type": "title", "title": [{"text": {"content": "Page Title"}}]}
```

### Adding content blocks to a page

```
mcp__notion__API-patch-block-children with parameters:
- block_id: "PAGE-UUID-HERE"
- children: [{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Text here"}}]}}]
```

**KNOWN ISSUE**: The `mcp__notion__API-post-page` tool has a serialization bug where the `parent` object parameter gets converted to a string, causing validation errors like "body.parent should be an object, instead was string".

**Workarounds (in order of preference)**:

1. **Add content to existing page**: If a suitable blank page exists, use `mcp__notion__API-patch-block-children` to add content directly
2. **Create in a database**: Creating pages in databases may work since the parent structure is different
3. **Ask user to create page**: Have the user create a blank page in Notion, share it with the integration, then use `mcp__notion__API-patch-block-children` to populate content

## Instructions

1. **Determine the parent location**:
   - If the user specifies a parent page ID, use that directly
   - If the user provides a page name or search term, use `mcp__notion__API-post-search` to find matching pages
   - Present options to the user if multiple pages match
   - If no parent is specified, create the page at workspace root

2. **Get the page content**:
   - Extract the title from the user's request
   - Identify if the user is providing content inline, referencing a file, or wants to create an empty page
   - If a file path is mentioned, read the file content
   - If the request is unclear, ask the user for clarification

3. **Parse markdown to Notion blocks**:
   - Convert markdown formatting to appropriate Notion block types
   - Support headings, lists, paragraphs, code blocks, quotes, callouts, and dividers
   - Preserve inline formatting like bold, italic, code, and links
   - Handle nested structures properly (nested lists, toggle content)

4. **Create the page**:
   - Use `mcp__notion__API-post-page` to create the page with title and parent
   - If the page has content, use `mcp__notion__API-patch-block-children` to add content blocks
   - For database pages, include required properties in the creation request

5. **Confirm success**:
   - Retrieve and display the created page URL to the user
   - Summarize what was created (title, parent location, number of blocks added)

## Markdown to Notion Block Conversion

### Supported Markdown Elements

- **Headings** (`# H1`, `## H2`, `### H3`):
  - Convert to `heading_1`, `heading_2`, `heading_3` blocks

- **Paragraphs**:
  - Convert to `paragraph` blocks
  - Support inline formatting (bold, italic, code, links)

- **Lists**:
  - Unordered lists (`-`, `*`) → `bulleted_list_item` blocks
  - Ordered lists (`1.`, `2.`) → `numbered_list_item` blocks
  - Nested lists are supported with proper indentation

- **Code Blocks** (` ``` `):
  - Convert to `code` blocks
  - Preserve language syntax highlighting

- **Quotes** (`>`):
  - Convert to `quote` blocks

- **Dividers** (`---`, `***`):
  - Convert to `divider` blocks

- **Toggle Blocks** (custom syntax: `> [!toggle] Title`):
  - Convert to `toggle` blocks with nested content

- **Callouts** (custom syntax: `> [!note]`, `> [!warning]`):
  - Convert to `callout` blocks with appropriate emoji

### Inline Formatting

- **Bold** (`**text**` or `__text__`) → bold rich text
- **Italic** (`*text*` or `_text_`) → italic rich text
- **Code** (`` `text` ``) → code rich text
- **Links** (`[text](url)`) → rich text with link annotation
- **Strikethrough** (`~~text~~`) → strikethrough rich text

## Block Structure Best Practices

1. **Organize content hierarchically**:
   - Use headings to create clear sections
   - Use toggle blocks for collapsible content
   - Use callouts to highlight important information

2. **Keep blocks simple**:
   - Each block should represent one logical unit of content
   - Avoid overly long paragraphs (split into multiple paragraph blocks)

3. **Use appropriate block types**:
   - Use `quote` blocks for citations
   - Use `callout` blocks for warnings and notes
   - Use `code` blocks for code snippets with language specified

4. **Preserve whitespace and formatting**:
   - Maintain blank lines between sections
   - Respect indentation for nested lists

## Usage Examples

### Example 1: Create a simple page with inline content

User request:
> Create a Notion page titled "Meeting Notes" in my Projects page with the following content:
> # Meeting Notes - Jan 7, 2026
> ## Attendees
> - Alice
> - Bob
> - Carol

Expected behavior:
- Search for "Projects" page
- Create a new page titled "Meeting Notes"
- Convert the markdown to proper Notion blocks (heading_1, heading_2, bulleted_list_item)
- Return the page URL

### Example 2: Create from a markdown file

User request:
> Create a Notion page from the documentation.md file in my Technical Docs page

Expected behavior:
- Read the content from `documentation.md`
- Search for "Technical Docs" page
- Parse the markdown content and convert to Notion blocks
- Create the page with the filename as the title (or first heading)
- Return the page URL

### Example 3: Create in a database

User request:
> Create a new task in my Tasks database titled "Review API docs" with status "In Progress"

Expected behavior:
- Search for "Tasks" database
- Create a page in the database with title "Review API docs"
- Set the Status property to "In Progress"
- Return the page URL

## Rich Text Formatting

Notion rich text objects support:
- `plain_text`: Basic text content
- `annotations`: Bold, italic, strikethrough, underline, code, color
- `href`: Links to URLs

Example rich text structure:
```json
{
  "type": "text",
  "text": {
    "content": "Hello world",
    "link": null
  },
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

## Advanced Features

### Database Pages

When creating a page in a database, extract property values from the user's request:
- Look for property assignments like "with status In Progress" or "priority: High"
- Use `mcp__notion__API-retrieve-a-data-source` to get database schema and valid property values
- Include properties in the page creation request

### Templates

Support creating pages from markdown file templates:

```markdown
# Project Brief

## Overview
[Brief description]

## Goals
1. Goal 1
2. Goal 2

## Timeline
- Start date:
- End date:

## Resources
- [Resource 1](url)
```

### Nested Content

Use proper indentation to create nested blocks:

```markdown
# Main Topic

## Subtopic 1
- Point 1
  - Subpoint 1
  - Subpoint 2
- Point 2

> [!toggle] Details
> This is collapsible content
> with multiple lines
```

## Error Handling

Handle common errors gracefully:

- **Invalid parent ID**: Inform the user the page wasn't found and ask them to verify the parent page name or ID
- **Permission denied**: Explain the integration needs access to the workspace/page and guide them to share it with the integration
- **Invalid markdown**: Report specific parsing errors and ask the user to provide corrected content
- **API rate limits**: Retry automatically with backoff, inform the user if multiple retries fail
- **Database property errors**: Explain which properties are required or have invalid values

## Tips

1. **Verify permissions first**: If this is the first time using Notion integration, create a simple test page first
2. **Parse markdown carefully**: Pay attention to proper markdown syntax for best conversion results
3. **Handle large documents**: For very large markdown files, consider splitting into multiple pages or warning the user about potential length
4. **Use standard markdown**: Stick to common markdown syntax for most reliable conversion
5. **Provide helpful feedback**: When a page is created, include the direct URL so users can access it immediately

## Troubleshooting

**Issue**: Page created but content is empty
- Check that the markdown is properly formatted
- Verify that block conversion is working correctly
- Review the Notion API response for errors

**Issue**: Some formatting not preserved
- Notion has limitations on certain markdown features
- Complex nested structures may need manual adjustment
- Check Notion's supported block types

**Issue**: Permission errors
- Verify the Notion integration has access to the workspace
- Confirm the parent page is shared with the integration
- Check that the integration has "insert content" capability
