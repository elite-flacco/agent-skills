---
description: Summarize learnings from the conversation and save to /learning
---

You are helping the user capture and preserve knowledge from your conversation. Your task is to extract the key learnings, insights, and takeaways and save them to a structured markdown file.

## Instructions

1. Review the current conversation to identify:
   - Key concepts explained
   - New techniques or approaches learned
   - Important facts or information shared
   - Code patterns or examples worth remembering
   - Gotchas, caveats, or common pitfalls discussed

2. Ask the user for a topic name using AskUserQuestion:
   - Suggest a default based on the main subject of the conversation
   - This will be used for the filename

3. Create the learning file at `/learning/<topic-name>.md` with the following structure:
   - Title and date
   - Summary (1-2 sentences)
   - Key Learnings (bullet points)
   - Details (expanded explanations where helpful)
   - Code Examples (if applicable)
   - References (links or sources mentioned)

4. If the `/learning` directory doesn't exist, create it first

5. Confirm the file was created and show the path

## Input

Optional topic hint: $ARGUMENTS

## Output Format

```markdown
# Learning: <Topic Name>

**Date:** YYYY-MM-DD

## Summary

<1-2 sentence overview of what was learned>

## Key Learnings

- Learning 1
- Learning 2
- Learning 3

## Details

<Expanded explanations, context, or nuance>

## Code Examples

<If applicable, include relevant code snippets>

## References

- <Any links or sources mentioned>
```

## Rules

- Focus on actionable, memorable takeaways
- Keep the summary concise but complete
- Include code examples when they were central to the learning
- Use clear, descriptive filenames (lowercase, hyphens for spaces)
- Don't include conversation meta-details, just the knowledge gained
