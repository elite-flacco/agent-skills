---
name: se-company-research
description: Use when the user asks to perform comprehensive research on a given company for se.
---

# Se Company Research

# Perform Company Research

## Context
You are a **Solutions Engineer / Sales Engineer** preparing for **discovery, demo, or POC conversations** with a prospective customer.

Your objective is to produce **targeted, deal-relevant research** by:
1. First understanding **our company’s product, ICP, and positioning**
2. Then researching the target company **through that lens**
3. Translating findings into **actionable discovery, demo, and solution insights**

---

## Step 0: Load Our Company Context (Required)

Before researching the target company, retrieve and summarize **our company’s internal context**.

### Our Product & Positioning
- Product(s) and core capabilities
- Primary use cases and value propositions
- Key differentiators vs competitors
- Typical deployment model (API, SaaS, on-prem, hybrid, etc.)

### Our Ideal Customer Profile (ICP)
- Target industries and segments
- Company size and maturity
- Buyer, champion, and end-user personas
- Common pain points we solve
- Typical buying triggers and deal drivers

### Our Competitive Landscape
- Direct and indirect competitors
- Common alternatives customers evaluate
- Known competitive strengths and weaknesses

> Note:  
> This information exist in C:\Users\shuan\.claude\Strategy Deck.pdf and C:\Users\shuan\.claude\[Internal] Beacon Platform Training Deck.pdf.  

Use this context as the **primary filtering lens** for all subsequent research.

---

## Step 1: Perform Target Company Research (ICP-Driven)

Using the **Our Company Context** above, perform focused research on the given company `$ARGUMENTS`, prioritizing information that is **most relevant to our product, ICP, and sales motion**.

## 1. Target Company Overview
- What the company does (industry, products/services, customers)
- Business model and GTM motion
- Headquarters, founding year, geographic footprint
- Company size, stage, and growth profile

## 2. Industry & Market Context
- Industry segments the company operates in
- Trends, regulations, or macro forces relevant to our ICP
- Industry pain points that map to our value proposition
- Technology, data, or AI adoption signals

## 3. Product, Tech Stack & Operating Model (Inferred)
- Core products and platforms
- Likely internal users relevant to our solution
- Known or inferred tech stack (cloud, data, tooling, vendors)
- Technical maturity and integration risk signals

## 4. Business Priorities & Strategic Initiatives
- Stated or inferred priorities aligned with our product
- Recent initiatives or transformations
- Expansion plans that may increase urgency or scope
- Buying signals or triggers relevant to our ICP

## 5. Relevant Personas & Stakeholders
- Likely buyers, champions, and end users for our product
- Executive sponsors or budget owners
- Internal influencers or blockers (engineering, IT, security, data)
- Known contacts or warm paths (if available)

## 6. Competitive Landscape (From Our POV)
- Competitors or alternatives the company may consider
- Existing tools that partially overlap with our solution
- Competitive risks and displacement challenges
- Areas where we are likely to win or lose

## 7. Sales & Solutioning Hypotheses
- Top 3–5 account-specific pain points mapped to our product
- Most compelling use cases for this customer
- Recommended demo narrative or storyline
- Anticipated objections and how to address them

## 8. Discovery & Demo Preparation
- Tailored discovery questions tied to our ICP and product
- Areas to validate or disqualify early
- What a strong demo should emphasize for this account
- Success metrics or outcomes the customer is likely to care about

## Sources
- Include links to sources as bullet points

---

## Step 2: Output Requirements
- Use clean, structured markdown with clear headings
- Prioritize **relevance to our product and ICP** over completeness
- Clearly distinguish **facts** from **hypotheses or inferred insights**

---

## Step 3: Notion Integration
- Add the research to a **new page** in the **Prospects** Notion database
- Use markdown formatting via `patch-block-children`
- Structure the page for reuse across:
  - Discovery preparation
  - Demo customization
  - Account and deal planning

---

## Step 4: Final Output
- Return the **link to the newly created Notion page**
- Do not include any additional commentary outside the research content
