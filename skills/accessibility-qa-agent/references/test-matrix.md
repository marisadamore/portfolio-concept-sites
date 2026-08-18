# Accessibility test matrix

## Deterministic inspection

- Document language and unique title
- One descriptive H1 and logical heading sequence
- Landmarks and main content
- Image alternative attributes
- Accessible names for links, buttons, inputs and iframes
- Duplicate IDs and unresolved ARIA references
- Positive tabindex and autofocus
- Media autoplay and iframe titles

## Browser journeys

- Tab through the page in visual and logical order
- Operate menus, sliders, forms and dialogs without pointer input
- Confirm focus visibility and focus return after overlays
- Test 200% zoom and 320 CSS-pixel reflow
- Confirm controls expose state changes such as expanded, selected and current
- Enable reduced motion and confirm nonessential animation stops or can be paused
- Check error identification, instructions and recovery for forms

## Manual assistive-technology review

- Screen-reader reading order and landmark navigation
- Alternative-text usefulness in context
- Voice-control naming and target discoverability
- Contrast for all states using verified computed colors
- Cognitive clarity, timing and error recovery
- Usability with representative disabled participants
