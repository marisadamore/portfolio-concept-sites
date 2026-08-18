# Small-business website audit skill

A reusable Claude Code skill (`SKILL.md`) that turns a live URL or local site into a prioritized, evidence-based audit for a small-business or nonprofit owner: customer clarity, conversion paths, accessibility, local SEO, trust signals, and technical quality, each finding tied to an observed defect rather than a generic checklist item.

**What's here:**
- `SKILL.md` — the skill definition and audit workflow
- `agents/openai.yaml` — agent-runtime configuration
- `references/audit-rubric.md` — the criteria the audit is scored against
- `scripts/audit_html.py` — deterministic signal collection for a downloaded/local page

Automated checks are treated as one input, not proof of compliance — the skill explicitly separates observed defects from recommendations and items that need manual review.
