# Quality records

These files are the start of the design records that medical-device software needs (IEC 62304 for the software life cycle, ISO 14971 for risk management, ISO 13485 for the quality system). They are deliberately lightweight now and will grow into a formal quality system before the CDSCO filing.

| File | What it records | Updated when |
|---|---|---|
| [requirements.md](requirements.md) | What the system must do, and how each requirement is checked | A feature is added or changed |
| [risk-register.md](risk-register.md) | What could harm a patient, and what prevents it | A new risk is found or a control changes; reviewed every Monday |
| [decision-log.md](decision-log.md) | Significant decisions, who made them and why | A design, clinical or process decision is made |
| [../CHANGELOG.md](../CHANGELOG.md) | What changed in each version | Every user-visible change |

Rules: never delete an entry; mark it superseded and add a new one. Every entry has a date.
