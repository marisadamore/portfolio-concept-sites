---
name: small-business-website-audit
description: Audit a small-business or nonprofit website for customer clarity, conversion paths, accessibility, local SEO, technical quality, trust, and content gaps. Use when Codex needs to review a live URL or local site, prioritize website improvements, run an accessibility-focused QA pass, or create an evidence-based audit report for an owner or developer.
---

# Small Business Website Audit

Produce a practical audit tied to business goals and observable evidence. Do not treat automated checks as proof of full accessibility compliance.

## Workflow

1. Establish the business type, primary audience, location or service area, and desired action. Infer these from the site when the user does not provide them and label the inference.
2. Inspect the homepage plus the most decision-relevant pages: services/menu, about, contact, booking/donation, and one representative detail page.
3. For a local or downloaded HTML page, run `scripts/audit_html.py <file> --json <output>` to collect deterministic signals. For a live page, use browser inspection and supplement it with available accessibility or link-checking tools.
4. Apply the criteria in `references/audit-rubric.md`. Separate observed defects from recommendations and manual checks.
5. Rank findings by user impact and effort:
   - P0: blocks access, contact, purchase, booking, or donation.
   - P1: creates significant accessibility, trust, discovery, or conversion risk.
   - P2: meaningful improvement with moderate impact.
   - P3: polish or optional optimization.
6. Cite the page, element, text, or test result supporting every defect. Do not invent analytics, search rankings, legal compliance, or customer behavior.
7. Deliver the report using the format below.

## Required report

### Executive summary

State the business goal, strongest current quality, biggest risk, and the three highest-value next actions.

### Scorecard

Score each area from 1–5 and explain the score in one sentence:

- Customer clarity
- Calls to action and conversion
- Accessibility
- Local SEO and discoverability
- Trust and content
- Mobile and technical quality

Scores summarize evidence; they are not standardized certifications.

### Prioritized findings

For each finding include:

- Priority and category
- Evidence
- Why it matters
- Specific fix
- Verification method

### Accessibility QA

Separate:

- Confirmed issues
- Automated warnings needing review
- Manual tests still required

Always include keyboard navigation, focus visibility, zoom/reflow, form errors, screen-reader naming, and motion review among manual checks when relevant.

### Action plan

Group work into quick wins, next sprint, and later improvements. End with measurable acceptance checks.

## Guardrails

- Preserve the business's voice and operational reality.
- Prefer a few high-confidence findings over a long generic checklist.
- Never claim WCAG conformance from automated inspection alone.
- Never recommend deceptive urgency, fake testimonials, fake scarcity, or hidden fees.
- Treat health, legal, financial, privacy, and donation claims as high-risk content requiring human verification.
