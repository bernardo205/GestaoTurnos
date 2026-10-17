# Gestão de Turnos

> A shift-management application built with Python and Streamlit, evolving from a simple shift log into a structured tool for weekly scheduling, employee qualifications, training and leave management.

**Repository:** [bernardo205/GestaoTurnos](https://github.com/bernardo205/GestaoTurnos)  
**Project status:** Requirements and planning in progress  
**Documentation status:** Current features and future plans are described separately below.

## Overview

Gestão de Turnos is a practical software project focused on restaurant shift management. Its goals are to improve the organisation of weekly schedules while preserving clear permissions, traceable changes and reliable employee records.

The project also serves as a professional portfolio demonstrating application development, database design, testing, documentation and deployment.

> **Status note:** items in the roadmap and planned scope are requirements, not claims that those features are already implemented.

## At a glance

| Area | Current status |
|---|---|
| Basic shift registration, history, editing and deletion | Available in the current application |
| Statistics and charts | Available in the current application |
| Number of employees supported in current use | Currently working for one employee only |
| Additional work positions | To be identified and specified |
| Detailed requirements for scheduling, roles, qualifications and leave | In planning |
| Implementation of the expanded workflows | Not yet confirmed |
| Legal and contractual validation of working-time and vacation rules | Pending |

## Roadmap

The roadmap is an indicative sequence of work. Phases may be adjusted as requirements are clarified. A phase will only be marked complete after the relevant work has been implemented and checked.

### Phase 1 — Requirements and technical assessment

**Status: In progress**

- [x] Document the existing application and its current capabilities.
- [x] Define the main roles and their responsibilities.
- [x] Record the initial requirements for weekly schedules, working hours, breaks and publication.
- [x] Define the initial scope for qualifications, training, days off and vacations.
- [x] Identify legal/contractual questions and unresolved decisions.
- [ ] Resolve the remaining scheduling, evaluation and request-workflow questions.
- [ ] Review the existing code and database before choosing the implementation approach.
- [ ] Clarify the requirements for supporting more than one employee.
- [ ] Collect the names and details of the additional work positions to be added.

### Phase 2 — Data model, access control and foundations

**Status: Planned**

- [ ] Design the data model based on the approved requirements.
- [ ] Define account, role and permission handling, including users with multiple roles.
- [ ] Enforce permissions in backend logic.
- [ ] Plan a safe migration path from the existing SQLite data, if a migration is approved.
- [ ] Add validation and automated tests for core data rules.
- [ ] Document backup and restore procedures before potentially destructive changes.

### Phase 3 — Weekly scheduling

**Status: Planned**

- [ ] Create weekly schedules manually for Monday–Sunday.
- [ ] Support overnight shifts.
- [ ] Apply the agreed full-time and part-time contractual-hour rules.
- [ ] Validate working hours and breaks according to the final, legally reviewed rules.
- [ ] Add manual publication for authorised managers.
- [ ] Record changes to published schedules and whether each change has been communicated.
- [ ] Provide a way to identify pending communications.

### Phase 4 — Employee requests and vacations

**Status: Planned**

- [ ] Implement days-off requests and manager/submanager decisions.
- [ ] Implement vacation requests and manager/submanager decisions.
- [ ] Show approved vacations while preparing weekly schedules without silently rewriting a published schedule.
- [ ] Add in-app and email notifications with visible handling of delivery failures.
- [ ] Implement the agreed initial vacation-balance calculation and manager confirmation/correction.
- [ ] Record historical vacation periods only when the information is known and verifiable.
- [ ] Validate vacation calculations against applicable Portuguese law and contractual rules before release.

### Phase 5 — Qualifications, training and quality

**Status: Planned**

- [ ] Preserve the 16 existing work positions.
- [ ] Confirm and add the additional work positions once their names and requirements have been provided.
- [ ] Manage employee qualifications by position.
- [ ] Authorise trainers for specific positions.
- [ ] Record training progress and evaluations.
- [ ] Require manager/submanager validation before an employee is considered autonomous at a position.
- [ ] Add ad-hoc quality evaluations without automatically granting qualifications.
- [ ] Define evaluation criteria, scales and visibility before implementation.

### Phase 6 — Verification, reliability and release preparation

**Status: Planned**

- [ ] Test permissions and role combinations.
- [ ] Test schedule calculations, overnight shifts and break rules.
- [ ] Test requests, notifications and audit records.
- [ ] Test data integrity and any approved legacy-data migration.
- [ ] Test database backup and restoration.
- [ ] Review configuration and secret handling.
- [ ] Update setup, operation and troubleshooting documentation.
- [ ] Verify the application in a separate test environment before considering production changes.

### Phase 7 — Portfolio presentation

**Status: Planned**

- [ ] Document the architecture and important technical decisions.
- [ ] Provide clear installation and configuration instructions.
- [ ] Add screenshots or a demonstration only after the corresponding features exist.
- [ ] Document testing and deployment results that have actually been verified.
- [ ] Review the README and repository presentation for public sharing.

## Current implementation

The current application is currently being used for **one employee only**. Supporting multiple employees is a requirement to clarify and implement; it should not be understood as an existing capability.

The current application provides:

- Register shifts.
- Browse shift history.
- Edit and delete existing records.
- View statistics and charts.

The repository uses Python modules for the Streamlit application, data access and models, along with SQLite database setup and a seed script. The expanded workflows described in the roadmap are not represented as implemented merely because they are documented here.

## Planned functional requirements

### Roles and permissions

A user may hold multiple roles without needing duplicate accounts.

| Role | Planned responsibilities |
|---|---|
| Restaurant manager | Create, edit and publish weekly schedules; approve days-off and vacation requests; manage position qualifications; validate autonomy; oversee training and quality. |
| Submanager | Perform the authorised management tasks, including schedule publication, request decisions, qualification management and autonomy validation. |
| Shift manager | View all schedules and oversee training and quality within their responsibilities. Cannot publish the global weekly schedule. Operational position changes during service remain outside the application. |
| Trainer | Train employees and evaluate progress for positions for which the trainer is authorised. A trainer's recommendation does not itself grant autonomy. |
| RP | A distinct role that can coexist with another role on one account. Specialised RP workflows are outside the first version. |
| Employee | View their own and other employees' schedules, submit days-off and vacation requests, and participate in training when applicable. |

Permissions must be enforced in backend logic, not only by hiding interface controls. Viewing schedules does not grant editing or publication rights. A formal team entity is not part of the planned data model.

### Weekly schedules

- The schedule week runs from Monday to Sunday.
- Managers and submanagers create schedules manually by selecting employees, days and working hours. Automatic schedule suggestions are outside the first version.
- Publication uses an explicit **“Publicar horário”** action and is restricted to the restaurant manager and submanagers.
- Employees can view all employees' schedules but cannot edit them solely because they have viewing access.
- Overnight shifts must be supported.
- Changes to a published schedule must record what changed, who changed it and when.
- After a change, management must answer: **“Esta alteração já foi comunicada ao funcionário?”**
  - **Yes:** record that the change was communicated.
  - **No:** mark communication as pending.
- Record who confirmed the communication status and when. There is no employee acceptance/rejection workflow.
- Keep the current schedule and an audit/change log. Keeping every complete historical schedule version has not been selected as a requirement.
- The initial work position and position changes during service are managed outside the application and must not be recorded as operational position changes in the app.

### Working hours and breaks

| Contract type | Contractual weekly hours | Planned schedule rule |
|---|---:|---|
| Full-time | Exactly 40 hours | 40 hours is the weekly target. |
| Part-time | 20–38 hours, according to the contract | Planned hours may vary between weeks; contractual hours remain the reference and must not change automatically. |

Additional agreed rules:

- Hours below the contractual target trigger a warning but do not, by themselves, block publication.
- Exceeding an applicable maximum blocks publication.
- A work period must not exceed five consecutive hours without a break of at least 30 minutes, according to the currently defined business rule.
- Breaks reduce net working time.
- The exact timing of the break, whether planned or actual breaks will be recorded, and the applicable rest periods still need to be finalised.

**Legal/contractual validation required:** verify the working-time rules against applicable Portuguese labour law, the individual contract and any applicable collective agreement before implementation. Product requirements alone do not establish legal compliance.

### Work positions and qualifications

The following 16 existing positions must be retained without changing their names:

1. Iniciador
2. Condimentador
3. Finalizador
4. Fritadeira
5. Grelhador
6. Batata
7. Caixa
8. Drive 1
9. Drive 2
10. Speaker 2
11. Bebidas
12. Runner
13. Expedidor
14. Apresentador
15. Sala
16. SAM

- Only the restaurant manager and submanagers may change position qualifications.
- An employee may work autonomously only at positions for which they are qualified.
- Trainer authorisation is position-specific.
- An employee in training must be accompanied by a trainer authorised for that position until autonomy has been demonstrated and validated.
- The trainer evaluates progress and recommends autonomy. The restaurant manager or a submanager validates it.
- Quality evaluations or attendance must not automatically grant a qualification.

### Training and quality evaluations

- Managers, submanagers and shift managers can oversee training according to their responsibilities.
- Training records should include the trainee, position, authorised trainer, dates, evaluations and final result.
- The first version supports ad-hoc quality evaluations.
- Formal evaluations twice per month are a possible future enhancement, not a first-version requirement.
- Evaluation criteria, scale, visibility and correction history still need to be defined.

### Days off

- Employees can request a specific day off.
- Requests appear in notifications and during preparation of the relevant week.
- The restaurant manager and submanagers can approve or reject requests. Shift managers cannot.
- Approval does not automatically modify a schedule; management must account for the request while preparing it.
- Days-off requests are separate from vacation requests.
- Requests should remain available with a status distinguishing pending from resolved decisions.

The full status lifecycle and employee-facing request history remain to be finalised.

### Vacations

- Employees submit a request with a start date and end date.
- Management sees the employee, dates, status and approve/reject actions.
- The restaurant manager and submanagers can approve or reject requests.
- Requests remain accessible after a decision, with their status updated.
- Overlapping requests generate a warning, but management makes the final decision.
- Approved vacations appear during schedule preparation. Approval does not automatically alter an already-published schedule.
- Employees cannot cancel approved vacations themselves; they must contact management.
- The application calculates an initial balance from the admission date and available contract data. The manager confirms or corrects it.
- Manual corrections record the old value, new value, responsible person, date and reason.
- Historical periods may be entered when dates are known and verifiable. Unknown periods must not be invented or presented as confirmed.
- The reference period is the calendar year, 1 January to 31 December.
- Management can decide how many unused days to carry over at year-end within applicable legal and contractual rules. Current-year and carried-over balances remain distinguishable.
- Carry-over decisions and historical corrections must be traceable.

The calculation method and detailed legal/contractual edge cases remain pending validation. Vacation requirements are being left at the current agreed level for now.

### Notifications and communication

- Days-off and vacation requests are surfaced to the relevant managers.
- Vacation decisions are communicated in-app and by email.
- Email requires a configured SMTP server or transactional email provider, secure secret configuration and valid user email addresses.
- Email failure must not undo a saved decision; failures should be visible and retryable.
- Emails should contain only the information needed to communicate the decision.
- Pending schedule-change communications must be identifiable.

Notification preferences and handling of duplicate or simultaneous decisions remain to be finalised.

### Audit trail and data integrity

Important actions should be traceable, including published-schedule changes, communication status, vacation-balance corrections, carry-over decisions, training and qualification decisions. Records should identify the responsible user and timestamp and include reasons or before/after values where relevant.

Historical data must distinguish confirmed information from unknown or unverified information.

## Out of scope for the first version

- Recording operational position changes during a service.
- Automatic schedule suggestions or optimisation.
- Employee acceptance/rejection of published schedule changes.
- Mandatory quality evaluations twice per month.
- Birthday-party management.
- Happy Meal toy-count workflows.
- A formal team entity or team-membership system.
- Additional contract regimes beyond the currently defined full-time and part-time rules, until specified.

## Pending decisions and validations

These items are not yet finalised and must not be treated as implemented features:

- Whether an incomplete weekly schedule can be published.
- Who may edit a published schedule, beyond the confirmed restriction on who may publish it.
- How pending communication is listed and how long audit records are retained.
- Exact timing of the five-hour break rule and whether planned or actual breaks are recorded.
- Legal/contractual validation of part-time weekly variation, working-time limits and rest periods.
- Evaluation criteria, scale, visibility and correction process.
- Full request-status lifecycle and whether employees can see their own request history.
- Employee exit dates, contract changes and related account/balance lifecycle.
- Detailed vacation-calculation edge cases, subject to later legal/contractual validation.

## Technology and architecture

### Current stack

- **Python** — application logic.
- **Streamlit** — user interface.
- **SQLite** — current data storage.
- **pandas** — data handling.
- **Plotly** — charts and statistics.

Dependency versions are not currently pinned.

### Future architecture

The final data model and architecture should be designed after requirements are sufficiently closed. Any database migration or deployment change remains a proposal until explicitly selected.

The legacy SQLite database and its records must be preserved. Do not convert old records into richer records when the original data does not support that conversion. Backups and a tested recovery path are required before potentially destructive changes.

## Run locally

1. Clone the repository and enter the project directory.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   streamlit run app.py
   ```

Streamlit will print the local URL where the application is available. These instructions describe the current application; they do not imply that roadmap features are already available.

## Development principles

- Inspect the current implementation before changing code or configuration.
- Preserve existing data and back up before potentially destructive changes.
- Distinguish the original application from test or deployment environments.
- Enforce permissions in backend logic.
- Keep secrets out of source control and logs.
- Add tests for permissions, scheduling rules, working-time calculations, training, data integrity and backup/restore as features are implemented.
- Document important changes and problems.
- Mark roadmap items complete only after implementation and verification.

---

Built as a practical portfolio project to explore application development, data handling and visualisation with Python.
