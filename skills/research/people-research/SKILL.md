---
name: people-research
description: Use when the user asks to perform comprehensive research on a given person to prepare for an interview.
---

# Nc People Research

# Perform People Research

## Instructions
1. Identify the interviewer and link to the job description using Notion MCP (ask the user for the relevant Notion page if not provided).
1. Perform comprehensive research on the interviewer to help user prepare for the interview. Return the findings in the following format: -

```markdown
## 1. Quick Snapshot (3–5 bullets)
- Their role and seniority  
- Their core responsibilities or domain  
- Notable background themes (e.g., AI infra, fintech, GTM, dev tools)
- Link to LinkedIn profile

## 2. Professional Background Summary
A concise paragraph summarizing their career path, expertise, and strengths.

## 3. What They Likely Care About in This Interview
Based on their background, role, and the position I'm applying for, provide 3–6 likely focus areas.  
Make the reasoning explicit.

## 4. Conversation Angles & High-Quality Questions
Provide 3–5 ways I can build rapport or start thoughtful conversations, such as:
- Specific projects or topics they’re known for  
- Relevant domain overlap  
- Smart, non-generic questions I can ask

## 5. Watch-Outs / Things to Prepare For
List any interview tendencies or potential pressure points—e.g., deep technical probing, 
preference for structured thinking, sensitivity to vague answers.

## 6. Tailored Prep Checklist
Give me a short checklist of what I should prep based on *their* profile:
- Specific stories (ownership, ambiguity, technical collaboration)  
- Core technical or product concepts to refresh  
- Frameworks or metrics

## Sources
Include links to sources as bullet points
```

2. Return the result in a clean, structured format with clear markdown-style headings and bullet points. Keep it concise but insightful. 
3. Add the research results to the provided Notion page, with the content being properly formatted as markdown (use patch-block-children).
