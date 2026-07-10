---
name: company-research
description: Use when the user asks to research a company — e.g. "research this company", "tell me about company X", "prepare me for an interview with company X" — for interview prep, sales, partnerships, or investing.
---

# Company Research

# Perform Company Research

## Instructions
1. Perform comprehensive research on the company the user names, including information such as below -

```markdown
## 1. Company Overview
- What the company does (industry, products/services, target customers)
- Headquarters and founding year
- Key executives (founders & leadership, advisory board if applicable)
- Company mission and vision statements

## 2. Recent News & Trends
- Relevant news articles or announcements (last 6–12 months)
- Recent milestones (e.g. product launches, acquisitions)
- Industry trends that may impact this company

## 3. Funding & Financial Info (for startups or private companies)
- Total funding raised, latest funding round, date, and lead investors
- Valuation (if available)
- Revenue estimates, growth rate, or financial health indicators

## 4. Products & Strategy
- Product(s), solutions, and use cases
- Client base
- Growth strategy - M&A plans (if applicable), geographic expansion, product development

## 5. Key Competitors
- List of direct competitors
- How the company differentiates itself (product, business model, culture, etc.)

## 6. Company Culture & Work Environment
- Glassdoor review summary (rating, pros, cons)
- Cultural values or known internal practices
- Interview experiences (if available)

## Sources
Include links to sources as bullet points
```

2. Return the result in a clean, structured format with clear markdown-style headings and bullet points. Keep it concise but insightful. 
3. Add the research results to a new page in the Companies Notion database, with the content being properly formatted as markdown (use patch-block-children).
4. Return the link of the new Notion page
