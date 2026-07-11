# Common Notion Page Block Patterns

This document provides proven block structure patterns for creating well-formatted Notion pages. Each pattern shows how to organize different block types effectively.

## Job Posting Page Pattern

Block structure for documenting job opportunities:

```markdown
# Overview
Paragraph block with company information and role summary.

## Key Details
List blocks when items are truly discrete:
- **Location**: City, State or Remote
- **Type**: Full-time, Contract, etc.
- **Posted**: <mention-date start="YYYY-MM-DD"/>

## Responsibilities
Paragraph block with clear prose describing the role, not bullet points unless specifically requested.

## Requirements
Paragraph block in similar format - clear prose over lists unless needed.

## Application
Paragraph block with application details, including [links](URL) as inline elements.
```

**Block types used**: Heading blocks (H1, H2), paragraph blocks, list blocks (minimal), date mention

## Meeting Notes Pattern

Using the meeting notes block type:

```markdown
<meeting-notes>
	Meeting with [Person/Team] - <mention-date start="YYYY-MM-DD"/>
	<notes>
		## Discussion Points
		Paragraph block with brief summary of what was discussed.
		
		## Action Items
		To-do blocks with context:
		- [ ] Task 1 with context
		- [ ] Task 2 with context
		
		## Next Steps
		Paragraph block describing what happens next.
	</notes>
</meeting-notes>
```

**Block types used**: Meeting notes block (special), heading blocks (H2), paragraph blocks, to-do blocks

## Project Documentation Pattern

Combining multiple block types effectively:

```markdown
# Project Name

Paragraph block with brief project overview in natural prose.

## Context
Paragraph block with background information about why this project exists.

## Current Status
Paragraph block updating where things stand, using natural language.

▶## Timeline
	Toggle block containing child blocks with timeline details.
	
	Paragraph block introducing the timeline.
	
	List blocks for discrete milestones:
	- **Kickoff**: <mention-date start="YYYY-MM-DD"/>
	- **Milestone 1**: <mention-date start="YYYY-MM-DD"/>

## Team
Paragraph block with user mentions:
<mention-user url="{{USER_URL}}"/> - Role description
<mention-user url="{{USER_URL_2}}"/> - Role description

## Resources
Paragraph block or list block with relevant links and references.
```

**Block types used**: Heading blocks (H1, H2), paragraph blocks, toggle heading block, list blocks (for timeline), user mentions

## Research Notes Pattern

```markdown
# Research: [Topic]

## Summary
High-level takeaway in 2-3 sentences.

## Key Findings
Main insights in prose form. Only use bullets if listing distinct findings that benefit from separation.

## Sources
- [Source Name](URL) - Brief description
- [Source Name 2](URL) - Brief description

## Questions
Outstanding questions that need answers.

## Next Actions
What to do with this research.
```

## Decision Log Pattern

```markdown
# Decision: [Topic]

**Date**: <mention-date start="YYYY-MM-DD"/>
**Status**: Proposed | Decided | Implemented

## Context
Why we're making this decision.

## Options Considered
Describe alternatives in prose, highlighting tradeoffs naturally.

## Decision
What we decided and why.

## Impact
Who this affects and how.
```

## Weekly Update Pattern

```markdown
# Week of <mention-date start="YYYY-MM-DD"/>

## Highlights
Top 2-3 accomplishments described clearly.

## Progress
Update on ongoing work in natural language.

## Challenges
Any blockers or issues, with context.

## Next Week
What's coming up.
```

## Technical Documentation Pattern

```markdown
# [Component/System Name]

## Purpose
What this does and why it exists.

## How It Works
Technical explanation in clear prose.

## Usage
How to use it, with code examples in code blocks:

\`\`\`python
# Example code
\`\`\`

## Considerations
Important things to know.

## Related
<mention-page url="{{PAGE_URL}}">Related Page</mention-page>
```

## Personal Notes Pattern

```markdown
# [Topic]

Personal thoughts and notes in natural, conversational prose.

<callout icon="💡">
	Key insight or important point that deserves emphasis.
</callout>

Further thoughts continuing naturally.

## Questions
Things to explore further.

## References
[Link](URL) - Why it's relevant
```

## Formatting Best Practices

1. **Use prose over lists**: Write in natural paragraphs unless the content specifically benefits from list structure
2. **Add context**: Don't just list items - explain why they matter
3. **Link related content**: Use page mentions to connect ideas
4. **Date appropriately**: Use date mentions for temporal references
5. **Strategic toggles**: Use toggles for optional detail that might clutter the main view
6. **Meaningful structure**: Use headings to organize, but keep them minimal
7. **Callouts for emphasis**: Highlight critical information with callouts sparingly
8. **Color intentionally**: Use colors to indicate status or importance, not decoration

## Anti-Patterns to Avoid

❌ **Over-listing**: Not everything needs to be a bullet point
❌ **Excessive formatting**: Too much bold/italic/color is distracting  
❌ **Empty structure**: Headers with no content beneath them
❌ **Redundant titles**: Don't repeat the page title in the content
❌ **Shallow toggles**: Don't use toggles for single lines of text
❌ **Orphaned content**: Include context so content makes sense standalone
