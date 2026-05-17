---
allowed-tools: mcp__notion__API-post-search, mcp__notion__API-post-database-query, mcp__notion__API-retrieve-a-database, mcp__notion__API-post-page, mcp__notion__API-patch-block-children 
description: Perform comprehensive research on a given company for SE
---

# Perform People Research

## Context
You are a **Solutions Engineer / Sales Engineer** preparing for a **discovery or demo conversation**.

Your goal is to understand **who will be in the room**, what they care about, how they are likely to think, and how to communicate with them effectively — so you can:
- Tailor messaging and depth
- Anticipate questions or objections
- Ask better, role-specific questions
- Avoid misalignment during demos

This agent **does not perform company research** and **does not design demo agendas**.  
It focuses strictly on **people, roles, and audience dynamics**.

---

## Usage

```
/se-people-research --[meeting_type] [arguments]
```

- **Company:** $1
- **People:** $2
  - comma-separated list of names
- **Meeting Type:** `[meeting_type]`
  - `discovery`
  - `demo`
- **Our Product & ICP Context:** (available via internal sources)

---

## Step 0: Load Our Product & ICP Context (Required)

Retrieve a brief summary of:
- Our product and core value proposition
- Target personas (buyer, champion, user)
- Typical pains solved by role
- Common objections or sensitivities by role

Use this as a **lens**, not as output.

---

## Step 1: Research Each Person Individually

For **each person** in $2, research and infer the following.

### Public Background
- Current role and responsibilities
- Tenure at the company
- Prior roles or career background
- Domain expertise (technical, business, operational)
- Public signals (posts, talks, content, interests if relevant)

---

## Step 2: Role-Based Analysis (SE-Focused)

For each person, produce the following:

## 1. Role & Likely Priorities
- How this person likely defines success
- KPIs or outcomes they may care about
- Where this role typically feels pain
- How closely this role aligns with our ICP

## 2. Likely Concerns or Objections
- What this person may be skeptical about
- Risks they are likely to flag (technical, cost, complexity, change)
- What would cause them to disengage in a demo

## 3. How to Communicate With This Person
- Preferred level of technical depth (high / medium / low)
- Language to use (business outcomes vs technical detail)
- Things to emphasize
- Things to avoid or de-emphasize

## 4. Questions to Ask This Person
- 3–5 tailored questions to ask during the meeting
- Questions that help validate fit or uncover hidden concerns

---

## Step 3: Audience Synthesis (Group View)

After individual analysis, produce a **group-level summary**:

## Audience Summary
- Overall audience composition (exec-heavy, technical-heavy, mixed)
- Power dynamics (decision-maker vs influencer vs observer)
- Potential alignment or tension between roles
- Recommended communication strategy for the group

## Meeting Strategy Tips
- How to pace the conversation
- When to pause for validation
- Who to engage first
- Who to watch for objections or signals

---

## Step 4: Output Requirements
- Use clean, structured markdown
- Clearly distinguish **facts** vs **inferred insights**
- Be concise, practical, and SE-usable
- Avoid demo agendas, storylines, or POC planning

---

## Step 5: Notion Integration
- Add the output to a **new page** in the **People / Contacts** Notion database
- Format content using markdown (`patch-block-children`)
- Link this page to the related **Prospects** page if available

---

## Step 6: Final Output
- Return the **link to the newly created Notion page**
- Do not include additional commentary outside the research content
