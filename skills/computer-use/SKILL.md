---
name: computer-use
description: Read or operate the UI of native desktop applications and the OS itself. Accessibility-first action ladder, observe-act-observe loop, exact app identifiers, main agent only. For web pages, use a browser skill instead.
---

# Computer Use

Operate native apps on the user's own machine: read their UI, click, type, scroll, drag, and verify the result. This is the desktop counterpart to browser automation — anything inside a web page belongs to a browser skill, not here.

## Choose the right tool first

- A dedicated connector, API, CLI or purpose-built skill beats driving pixels. Check for one before touching the UI.
- Browser and web tasks go to browser automation, full stop.
- Do not reach for OS scripting (AppleScript, JXA, System Events, PowerShell UI automation, shell hacks) unless the user explicitly names that technology.
- **Main agent only.** Never delegate desktop operation to a subagent; UI state, focus and coordinates do not transfer.

## The action ladder

Take the highest rung that works; never drop lower for convenience.

1. **Semantic / accessibility path.** Observe the app's element tree, find the target by role, name, title or value, act on it by its identifier. Precise, works on background windows, does not steal the user's focus.
2. **Direct value setting.** For settable fields, set the value rather than simulating typing. Use paste only when the element is not settable or the content is rich text.
3. **Keyboard input.** Only when no element expresses the operation, or the user asked for keyboard interaction. A shortcut being shorter is not a reason to skip an available element action.
4. **Coordinates.** Last resort, for canvas, games and custom-drawn content the semantic tree cannot see. Choose coordinates only from the *current* screenshot raster, integers inside its bounds — never reuse numbers from earlier text, element bounds or window frames.

Do not run two paths for the same action. Pick one, verify, then decide.

## The loop

Observe once, act, then observe again before the next step.

- **Success means the API accepted your action, not that the app acted.** A click can land on a stale element; typing can be accepted and change nothing. Re-observe to confirm the intended state actually appeared.
- **Bind apps by their exact display name.** Copy the name character-for-character — do not translate, localize, normalize, shorten or drop a suffix. A rewritten name resolves to a different app or none at all. If the exact string fails, list running apps once and pick the matching identifier.
- **Batch related actions, close with one observation.** Element identifiers stay valid between actions until the next observation renumbers the tree. Take identifiers only from the newest observation; a vanished element fails closed.
- **Diffs, not dumps.** Observations may return only what changed since the last tree in this session; unchanged rows keep their identifiers. If an observation reports no change, do not repeat it without an intervening action.
- **Watch the window scope.** Observations resolve the front window each time, so a modal that just opened becomes the captured window — when the tree reads like the wrong part of the app, look for a dialog, handle or dismiss it, then re-observe. A missing element is not proof your action worked; it may be proof you are looking at the wrong window.

## Boundaries

Desktop operation is powerful and literal: it clicks what is actually on screen, in the user's session, with the user's permissions. Confirm destructive dialogs instead of autopiloting through them, stay inside the app the user named, and stop when the task's acceptance check is visible on screen — the observation is your evidence.
