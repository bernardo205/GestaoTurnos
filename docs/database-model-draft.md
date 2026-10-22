# Database model draft

**Status:** Draft for requirements review — not implemented.

This document starts Phase 2 of the roadmap. It proposes a normalized relational model for the agreed requirements while keeping unresolved requirements visible. It does not authorize a schema migration, a PostgreSQL switch, or changes to any existing database.

## Design goals

- Support multiple employees and accounts that can hold more than one role.
- Store the planned schedule and a history of edits; a separate actual-work/actual-hours module is out of scope for this phase.
- Preserve planned-schedule changes (previous value, new value, actor and timestamp) and record that the affected employee was notified after a published schedule changes.
- Keep work positions separate from a shift's operational assignment; position changes during service remain out of scope.
- Preserve the legacy SQLite database and do not infer richer records from its limited data.
- Keep the schema portable between SQLite and PostgreSQL where practical.

## Proposed entities

### People, accounts and permissions

- **employee**: employee identity and lifecycle (name, optional email, admission date, optional end date, active state). Employment/contract terms should be separate dated records so changes do not overwrite history.
- **employment_contract**: employee, contract type (full-time/part-time), contractual weekly hours, validity start/end. Exact full-time and part-time hour limits are not yet confirmed and must not be hard-coded from assumptions.
- **user_account**: login identity and account state, linked optionally to one employee. Authentication mechanism and identity provider are undecided; do not store plaintext passwords.
- **role** and **account_role**: role catalogue and many-to-many assignment, allowing one account to hold several roles. Role names should be stable keys; authorization rules belong in backend code and need their own acceptance criteria.

### Positions, qualifications and training

- **work_position**: stable ID, unique name, active state. Seed the 16 existing position names without renaming them; additional positions await confirmation.
- **employee_qualification**: employee, position, state, effective dates, who recommended and who validated, and validation time. Autonomous assignment requires completed training and a positive FV evaluation. A non-positive FV requires repeat training; do not grant qualification from attendance or quality scores automatically.
- **trainer_authorization**: trainer employee, position and validity period; only an authorized trainer may lead training for that position.
- **training_record**: trainee, position, trainer (which may be an authorised trainer, manager or shift manager), start/end dates, FV evaluation and outcome. A non-positive FV requires repeat training.
- **quality_evaluation**: employee, evaluator, date, criteria/version, result and any correction history. Keep separate from qualification decisions. Criteria and visibility are unresolved.

### Planned schedule and actual work

- **schedule_week**: Monday `week_start_date` (unique), state (`draft`/`published`), creator, publication actor/time, and a monotonically increasing revision. Whether incomplete weeks can be published remains unresolved.
- **planned_shift**: schedule week, employee, start and end instants, created/updated by and timestamps. Store enough timezone information to interpret local shift times and overnight work. The application currently targets one restaurant; the canonical timezone and daylight-saving representation need confirmation before choosing concrete SQL types.
- **planned_break**: planned shift, start/end, and ordering. Breaks are recorded on the planned schedule but are not deducted from hours counted towards contractual hours. A work period must not exceed five consecutive hours without a **continuous break of at least 30 minutes**; the break cannot be split.
- **schedule_change**: affected planned shift/schedule, actor, timestamp, reason where provided, and before/after values. A separate communication record should capture whether the affected employee was notified, by whom and when. Changes to a published schedule always require notifying the affected employee.

A separate `actual_shift`/`actual_break` model is not part of this phase: the selected approach is planned hours with an edit history, not a separate record of actual hours worked.

Use half-open intervals (`start < end`, end excluded) for overlap checks. Represent overnight work with an end instant on the following date, not a negative duration. The final timezone and daylight-saving representation must be settled before implementation.

### Requests and vacation balances

- **day_off_request**: employee, requested date, submission time, status and decision actor/time/reason. Any user may request a day off, including management/training roles. Only a manager or submanager may decide; self-approval is forbidden. When approved, the date is automatically marked as a day off.
- **vacation_request**: employee, inclusive date range, submission time, status and decision actor/time/reason. Overlap warns management but does not itself decide the request.
- **vacation_balance_entry**: employee, calendar year, category (current-year/carry-over/adjustment/usage), quantity, effective date, actor and reason. Keep corrections and carry-over decisions as append-only entries rather than overwriting a single balance. Calculation rules and legal/contractual validation remain open.
- **audit_event**: actor account, action, entity type/ID, timestamp, reason and before/after payload for significant changes. Avoid storing secrets or unnecessary personal data in audit payloads.

Request lifecycle values, employee visibility, cancellation and simultaneous-decision behavior still need to be specified.

## Integrity and access rules

- Use foreign keys and enable SQLite foreign-key enforcement on every connection.
- Prefer `RESTRICT` for deleting referenced employees, positions, accounts and historical records; deactivate records instead of deleting them.
- Add uniqueness for account identity, role assignment, position name, one schedule per week, and one active qualification per employee/position where the chosen history model supports it.
- Add indexes for employee/date, schedule week/status, request status/date, and audit entity/time queries.
- Enforce publication, qualification, role and schedule rules in backend transactions, not only in the Streamlit interface.
- Record actor and timestamp on decisions and changes. Use a transaction for multi-row writes and schedule publication.

## Legacy data and migration plan

1. Keep the existing `data/turnos.db` untouched and take a verified backup before any future migration work.
2. Build a separate development database from an explicit schema version; never point migration code at production by default.
3. Map existing `gerentes`, `postos` and `turnos` only after confirming what each legacy row means. Do not assume a legacy shift is a planned schedule or actual-work record if the source does not establish that.
4. Preserve source IDs and values in a staging/import record where needed; report unmapped and ambiguous rows instead of guessing.
5. Validate row counts, foreign keys, dates, and representative records on a copy, then rehearse restore before considering any production change.
6. Choose SQLite or PostgreSQL only after the data model, deployment target, backup/restore process and operational requirements are agreed. A PostgreSQL migration is currently planned, not approved or implemented.

## Decisions needed before implementation

- Employment identity, email/login provider, account creation and employee departure behavior.
- Exact full-time and part-time contractual-hour limits, contract changes, and legal/contractual validation of the five-hour/30-minute break and rest rules.
- Whether the minimum 30-minute break must be continuous or may be split into shorter breaks.
- Timezone and daylight-saving behavior for overnight shifts.
- Publication must be blocked until the weekly schedule is complete and passes the agreed validations. Detailed editing rights after publication and audit retention remain to be finalised.
- Request lifecycle, notification channels, employee-facing history and duplicate/simultaneous decisions.
- Vacation accrual, carry-over, historical corrections and applicable legal/contractual interpretation.
- Evaluation scale, visibility, corrections and the relationship between training and qualification.
- Deployment database, backup/restore requirements and migration acceptance criteria.

Until these are decided, this remains a proposal. The existing schema and production data must not be changed based on this draft alone.