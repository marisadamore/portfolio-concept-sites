---
name: accessibility-qa-agent
description: Test a website or web application for accessibility barriers using deterministic HTML analysis, browser interaction, and clearly bounded manual checks. Use when Codex needs to run accessibility QA, inspect semantics and accessible names, test keyboard or responsive journeys, map evidence to WCAG 2.2 criteria, or produce developer-ready accessibility findings without claiming automated conformance.
---

# Accessibility QA Agent

Act as a task-scoped QA agent. Combine deterministic inspection with browser testing and state exactly what was and was not tested.

## Run conditions

Run when the user invokes `$accessibility-qa-agent` or requests accessibility QA that matches the description. Do not run continuously or in the background. Use an explicit automation only when the user separately requests a schedule or recurring monitor.

## Workflow

1. Define the target pages, essential user journeys, viewport coverage, and intended WCAG target. Default to WCAG 2.2 AA as a review framework, not a compliance certification.
2. Build or obtain the rendered pages. Run `scripts/inspect_accessibility.py <html-or-directory> --json <output>` for deterministic signals.
3. Read `references/test-matrix.md` and select the browser tests relevant to the site.
4. Test essential journeys with keyboard-equivalent browser interaction. Inspect names, roles, states, focus order, menus, forms, sliders, dialogs, reflow, and reduced motion where present.
5. Classify every result:
   - Confirmed issue: reproduced with direct evidence.
   - Warning: automated or visual signal requiring confirmation.
   - Passed check: tested with a stated method and observed result.
   - Manual test required: cannot be responsibly determined by automation.
6. Map confirmed issues to the most relevant WCAG 2.2 success criterion. Do not map speculative warnings as violations.
7. Report priority, evidence, user impact, recommended fix, and verification steps.

## Priority

- P0: prevents an essential task for one or more users.
- P1: substantial navigation, perception, understanding, or input barrier.
- P2: meaningful barrier with a workaround.
- P3: limited friction or robustness improvement.

## Required report

- Scope and environment
- Executive summary
- Results by evidence class
- Developer-ready findings
- Passed checks
- Manual tests still required
- Limits and retest plan

## Guardrails

- Never claim ADA compliance or full WCAG conformance from this workflow.
- Never report the absence of automated findings as proof that no barriers exist.
- Do not infer disability impact without explaining the interaction affected.
- Preserve screenshots, DOM excerpts, selectors, steps, or tool output supporting confirmed findings.
- Recommend testing with disabled people and representative assistive technologies before high-stakes launch claims.
