# Substantive gap closure

Do not chase Superpowers file counts or equate volume with quality.

1. Build an objective 50-task benchmark corpus spanning executable Python
   solutions and structured infrastructure outputs. Use hidden-from-prompt
   assertions, offline replay + explicit opt-in network generation, per-task
   reports, baseline comparison and reproducible metadata. No auto-execution of
   model Python without separate consent; resource limits are not a sandbox.
2. Implement real DOCX/XLSX/PDF/PPTX generation and read-back tests as optional
   dependency fixtures, not untested guide presence. Keep output local/private.
3. Strengthen coding playbooks with original task/review/debugging templates,
   practical recovery rules, host truth boundaries and acceptance mapping.
4. Test installers across all declared destinations and hook behavior with real
   temporary directories. Distinguish install smoke from native host sessions.
5. Independent review, full regressions, measured inventory, clear remaining
   external gates (provider billing, marketplace approval, native host access).

## Verification and review receipt

- Observed missing-module RED for task grader and document pipeline. Observed
  five failing symlink install cases and two modified-content/force cases before
  their fixes. Reference calibration initially 49/50: diagnosed an escaped
  backreference bug in the author fixture, corrected it; no grader weakening.
- Independent reviewer identified shared-runner contamination, misleading hash
  seed, payload-driven provenance and recursive input risks; reproduced/fixed
  fresh-per-check runner and source labels, dropped ineffective hash seed and
  recorded non-sandbox constraints directly in reports. HTTPS/timeouts/output
  validation already live in the provider and were not duplicated as fake fixes.
- Final: 260 pytest checks pass; 140 skills valid; smoke checks pass; generated
  catalog current; whitespace diff clean; 50/50 existing contracts, 50/50 author
  reference calibrations. Live provider intelligence score NOT measured.
- External gates remain provider choice/spend, native CLI/desktop sessions,
  restricted execution sandbox, marketplace approval and a real service operator.
- Rollback: revert this increment. Installer --force is an explicit replacement
  override, not a backup service; back up modified local installs first.
