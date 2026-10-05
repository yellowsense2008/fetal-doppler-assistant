# How we work in this repository

## Branches

- `main` is always working and demo-ready. Nobody pushes to it directly.
- Create one branch per task, named `<area>/<short-description>`, for example `reader/mindray-layout`, `engine/published-ua-chart`, `platform/audit-log`.
- Keep branches short-lived: open a pull request within a few days.

## Commits

- Commit from **your own GitHub account**, with the email address linked to that account (check with `git config user.email`). Shared logins break the audit trail.
- Write the message as what the change does: `Gate vision-only values on formula check`, not `fixes`.

## Pull requests

Every pull request to `main`:

1. Links the GitHub issue it works on (`Closes #12`).
2. Passes `python -m pytest -q`.
3. Is reviewed and approved by the code owner of the files it touches (see `.github/CODEOWNERS`).
4. Updates `CHANGELOG.md` under **Unreleased** if users or the doctor would notice the change.
5. For any change to clinical logic (`engine/rules.py`, `engine/reference_charts.py`, `docs/guideline_rules_rcog_gtg31.md`): records Dr Jini Gupta's approval and adds an entry to `quality/decision-log.md`.

## Definition of done

A task is done when the code is reviewed, tests pass, the change log and quality records are updated where needed, and the linked issue is closed.

## Data

Never commit scan images, report PDFs, patient names or IDs, answer-key sheets, or secrets. If you commit one by mistake, tell Talha immediately: deleting the file in a new commit does not remove it from git history.

## Escalation

A blocker older than two working days goes to Talha. Anything needing money, an outside party or a change of scope goes to Prakhar in that week's status report.
