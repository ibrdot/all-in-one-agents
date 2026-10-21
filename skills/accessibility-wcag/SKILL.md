---
name: accessibility-wcag
description: "Use when building or reviewing any user-facing UI for accessibility - WCAG AA essentials, keyboard flow, ARIA done right, and the failures that most often block real users."
---

# Accessibility (WCAG)

Accessibility is not a checklist bolted on at the end; it is whether your product works for someone who cannot see the screen, use a mouse, or parse dense text. Target WCAG 2.2 AA as the floor.

## The non-negotiables

1. **Keyboard everything.** Every interactive element reachable and operable with Tab/Enter/Space/arrows; visible focus indicator that is never `outline: none` without a replacement. Tab through the page - if focus vanishes into a drawer or modal trap, it is broken.
2. **Labels, not placeholders.** Every input has a real `<label>`; placeholder-only labels fail screen readers and vanish on type.
3. **Contrast 4.5:1** for normal text (3:1 for large), including text over images. Trust a contrast checker, not your eyes.
4. **Semantic HTML first.** Native `<button>`, `<nav>`, `<table>` get ARIA for free. `div` with a click handler and `role="button"` is a smell - use the real element.
5. **ARIA is the last resort**, and a wrong ARIA state is worse than none. If you use `aria-*`, wire its state changes too.

## The usually-missed ones

- Focus management on route change and modal open/close: move focus into the modal, return it on close, announce page changes.
- Form errors are announced: `aria-live` or error summary linked to fields, described in text, not red color alone.
- Zoom to 200% and reflow at 320px width - no horizontal scroll, no clipped content.
- `prefers-reduced-motion` respected; auto-playing carousels have pause controls.
- Alt text that conveys meaning ("chart: revenue up 12% Q3"), not "image of chart."

## Review flow

Test in this order: keyboard only, then 200% zoom, then a screen reader pass on the top journey. Fix in HTML/structure before reaching for ARIA patches.
