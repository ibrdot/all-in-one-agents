# PostToolUse Hook

Fires after tool calls. Lightweight — heavy checks belong to Stop.

## Action

When the agent is about to claim a task is complete, trigger
`verification-before-completion`:

- Require actual command output (tests, build, acceptance check) in the message.
- "It should work" is not evidence. Output or it didn't happen.

Otherwise: no action, keep the loop fast.
