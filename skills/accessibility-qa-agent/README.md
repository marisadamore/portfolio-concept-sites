# Accessibility QA agent

A reusable Claude Code skill (`SKILL.md`) that turns an AI coding agent into a task-scoped accessibility QA reviewer: deterministic HTML checks plus bounded, keyboard-driven browser testing, with every finding classified as confirmed, warning, passed, or manual-test-required rather than reported as a pass/fail conformance claim.

**What's here:**
- `SKILL.md` — the skill definition and workflow the agent follows
- `agents/openai.yaml` — agent-runtime configuration
- `references/test-matrix.md` — the browser test matrix the agent selects from
- `scripts/inspect_accessibility.py` — deterministic HTML/semantics analyzer used as the first pass

This skill defaults to WCAG 2.2 AA as a review *framework*, not a certification — it's explicit that automated and manual checks each cover different ground, and states plainly what was and wasn't tested.
