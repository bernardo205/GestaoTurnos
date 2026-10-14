# Gestão de Turnos

**A shift-management application built with Python and Streamlit.** The current version provides basic shift registration, history, editing and statistics. This README also documents the functional requirements agreed for future development; planned functionality is explicitly distinguished from what is currently implemented.

- **Current repository:** [bernardo205/GestaoTurnos](https://github.com/bernardo205/GestaoTurnos)
- **Project language:** Portuguese
- **Current stack:** Python, Streamlit, SQLite, pandas and Plotly

> **Project status:** requirements and planning are in progress. The requirements below do not mean that the corresponding features have already been implemented.

## Contents

- [Current implementation](#current-implementation)
- [Project objective](#project-objective)
- [Planned functional scope](#planned-functional-scope)
  - [Roles and permissions](#roles-and-permissions)
  - [Weekly schedules](#weekly-schedules)
  - [Working hours and breaks](#working-hours-and-breaks)
  - [Work positions and qualifications](#work-positions-and-qualifications)
  - [Training and quality evaluations](#training-and-quality-evaluations)
  - [Days off](#days-off)
  - [Vacations](#vacations)
  - [Notifications and communication](#notifications-and-communication)
  - [Audit trail and data integrity](#audit-trail-and-data-integrity)
- [Out of scope for the first version](#out-of-scope-for-the-first-version)
- [Pending decisions and validations](#pending-decisions-and-validations)
- [Technology and architecture](#technology-and-architecture)
- [Run locally](#run-locally)
- [Development principles](#development-principles)

## Current implementation

The current application provides the following features:

- Register shifts.
- Browse shift history.
- Edit and delete existing records.
- View statistics and charts.

The current repository contains Python modules for the Streamlit application, data access and models, plus a SQLite database setup and seed script. The existing implementation should be assessed before substantial changes. The legacy database and its records must be preserved during future development.

## Project objective

Develop the application into a reliable shift-management tool and a professional portfolio project, demonstrating skills in programming, data management, testing, documentation and deployment.

The planned application will distinguish between **weekly schedule planning** and **operational decisions made during a service**. The application is intended to manage schedules, employee qualifications, training, leave requests and relevant records; it is not intended to track every operational position change during a shift.

## Planned functional scope

### Roles and permissions

A user may hold more than one role. For example, an employee may also be an RP or an authorised trainer; these roles must not require duplicate accounts.

| Role | Planned responsibilities |
|---|---|
| Restaurant manager | Create, edit and publish weekly schedules; approve days-off and vacation requests; manage position qualifications; validate employee autonomy; oversee training and quality. |
| Submanager | Perform the management tasks authorised for the role, including schedule publication, request decisions, qualification management and autonomy validation. |
| Shift manager | View all employee schedules, oversee training and quality within their responsibilities, and manage service operations outside the application's schedule-planning workflow. Cannot publish the global weekly schedule. |
| Trainer | Train employees and evaluate their progress for the specific work positions for which they are authorised. A trainer's recommendation does not itself grant autonomy. |
| RP | A distinct role that may coexist with other roles on one account. Specialised RP workflows are outside the first version. |
| Employee | View their own and other employees' schedules, submit days-off and vacation requests, and participate in training when applicable. |

Permissions must be enforced by the application backend, not only by hiding interface controls. Viewing a schedule does not grant permission to edit or publish it.

There is no formal team entity in the planned data model.

### Weekly schedules

- The schedule week runs from **Monday to Sunday**.
- Schedules are created manually by the manager or submanager, selecting employees, days and working hours. Automatic schedule suggestions are not part of the first version.
- Publication is a deliberate action using a **“Publicar horário”** (Publish schedule) action.
- Only the restaurant manager and submanagers may publish the global weekly schedule.
- Employees can view all employees' schedules, but this does not grant editing permissions.
- Overnight shifts must be supported.
- A published schedule may be changed, with a record of what changed, who changed it and when.
- When a published schedule is changed, the manager must answer: **“Esta alteração já foi comunicada ao funcionário?”** (“Has this change already been communicated to the employee?”).
  - **Yes:** record that the change was communicated.
  - **No:** mark the communication as pending.
- Record who confirmed the communication status and when. There is no employee acceptance/rejection workflow.
- The application will retain the current schedule and a change/audit log; retaining every complete historical schedule version has not been selected as a requirement.
- The initial work position and operational position changes during service are managed outside the application and must not be recorded as operational position changes in the app.

### Working hours and breaks

The agreed planning rules are:

| Contract type | Contractual weekly hours | Planned schedule behaviour |
|---|---:|---|
| Full-time | Exactly 40 hours per week | The weekly target is 40 hours. |
| Part-time | Between 20 and 38 hours per week, according to the contract | Weekly planned hours may vary. Contractual hours remain the reference and are not silently changed by schedule edits. |

Additional requirements:

- If planned hours are below the contractual target, warn the manager but do not block publication solely for that reason.
- If a schedule exceeds an applicable maximum, block publication.
- No automatic schedule suggestions are required in the first version.
- A work period must not exceed five consecutive hours without a break of at least 30 minutes, according to the currently defined business rule.
- Breaks reduce net working time.
- The exact timing of the break, how planned versus actual breaks are represented, and other rest-period rules remain to be finalised and legally checked.

**Important:** these are agreed product requirements, not a claim that every configuration is legally valid. The working-time rules must be checked against applicable Portuguese labour law, the employment contract and any applicable collective agreement before implementation.

### Work positions and qualifications

The first version must retain these **16 existing work positions** without changing their names:

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

Requirements:

- An employee may work autonomously only in positions for which they are qualified.
- Only the restaurant manager and submanagers may modify position qualifications.
- Trainer authorisation is position-specific, not universal.
- An employee in training at a position must be accompanied by a trainer authorised for that position until autonomy has been demonstrated and validated.
- A trainer evaluates progress and recommends autonomy. The restaurant manager or a submanager makes the final validation.
- Only after that final validation is the employee considered qualified for the specific position.
- The application must not infer qualification from attendance or from a quality evaluation.

### Training and quality evaluations

- Managers, submanagers and shift managers can oversee training according to their responsibilities.
- Training records should include the position, trainee, authorised trainer, dates, evaluations and final result.
- Quality evaluations in the first version are ad hoc assessments rather than a mandatory periodic programme.
- A quality evaluation must not automatically grant qualification or autonomy.
- Formal evaluations twice per month are a possible future enhancement, not a first-version requirement.

The evaluation criteria, scale, visibility and correction history still need to be specified.

### Days off

- Employees can request a specific day off.
- Requests appear in notifications and when management prepares the relevant week.
- The restaurant manager and submanagers can approve or reject requests. Shift managers do not have this permission.
- Approval does not automatically change a schedule; management must account for the request when preparing the week.
- Days-off requests are separate from vacation requests.
- Requests should remain available with a status that distinguishes pending and resolved decisions.

The complete set of request statuses and the employee-facing request history still need to be finalised.

### Vacations

The agreed requirements are:

- Employees submit a request with a start date and end date.
- Requests appear in notifications and in a management area that shows the employee, dates, status and approve/reject actions.
- The restaurant manager and submanagers may approve or reject requests.
- Requests remain accessible after a decision, with their status updated.
- Overlapping vacation requests generate a warning, but management may still make the final decision.
- Approved vacations are visible during weekly schedule preparation. Approval does not automatically alter an already-published schedule.
- Employees cannot cancel an approved vacation themselves; they must contact management.
- The application calculates an initial vacation balance from the admission date and available contract data. The manager confirms or corrects the result.
- Manual corrections must record the previous value, new value, responsible person, date and reason.
- Historical vacation periods before the application starts may be entered when the dates are known and verifiable. Missing periods must not be invented or represented as confirmed.
- The reference period is the calendar year, from 1 January to 31 December.
- At year-end, management may decide how many unused days to carry over, within applicable legal and contractual rules. Current-year and carried-over balances must remain distinguishable.
- Decisions about carry-over and historical corrections must be traceable.

The vacation calculation method and legal/contractual edge cases must be validated before implementation. Detailed vacation rules are intentionally not being expanded further at this planning stage.

### Notifications and communication

- Days-off and vacation requests should be surfaced to the relevant managers.
- Vacation decisions should be communicated to the employee both in the application and by email.
- Email requires a configured SMTP server or transactional email provider, secure secret configuration and valid email addresses for users.
- Email delivery failure must not undo or erase a saved decision. Failures should be visible and retryable.
- Emails should contain only the information necessary to communicate the decision.
- Pending schedule-change communications must be identifiable.

The exact notification preferences and handling of duplicate or simultaneous decisions remain to be finalised.

### Audit trail and data integrity

Important changes should be traceable, including:

- Changes to published schedules and their communication status.
- Vacation balance corrections and carry-over decisions.
- Relevant training, qualification and autonomy decisions.
- Other management actions where an audit record is needed.

Records should identify the action, responsible user and timestamp, and include the reason or before/after values where relevant. Historical data must distinguish confirmed information from unknown or unverified information.

## Out of scope for the first version

- Recording operational changes of work position during a service.
- Automatically suggesting or optimising weekly schedules.
- Employee acceptance/rejection of published schedule changes.
- Formal quality evaluations twice per month.
- A birthday-party management module.
- Happy Meal toy-count workflows.
- A formal team entity or team-membership system.
- Contract types beyond the defined full-time and part-time rules, until separately specified.

## Pending decisions and validations

The following items are not yet finalised and must not be treated as implemented requirements:

- Whether a weekly schedule may be published while incomplete.
- Who may edit an already-published schedule, beyond the confirmed restriction on who may publish it.
- How pending schedule-change communications are listed and how long audit records are retained.
- The exact timing of the five-hour break rule, and whether planned or actual breaks are recorded.
- Applicable rest periods and the legal/contractual validity of weekly part-time hour variation.
- The criteria, scale, visibility and correction process for quality evaluations.
- The full request-status lifecycle and whether employees can view their own request history.
- Employee exit dates, contract changes and the related lifecycle of accounts and balances.
- Detailed vacation-calculation edge cases, subject to later legal/contractual validation.

## Technology and architecture

### Current stack

- **Python** — application logic.
- **Streamlit** — user interface.
- **SQLite** — current data storage.
- **pandas** — data handling.
- **Plotly** — charts and statistics.

The current requirements file defines the Python dependencies. Dependency versions are not currently pinned.

### Future architecture considerations

The data model and architecture must be designed only after the functional requirements are sufficiently closed. Any future database migration, framework change or deployment approach is a proposal until explicitly selected.

The legacy SQLite database and its records must be preserved. Existing records must not be converted into richer records when the original data does not support that conversion. Backups and a tested recovery path are required before any potentially destructive migration.

## Run locally

1. Clone the repository and enter the project directory.
2. Install dependencies:

   ~~~bash
   pip install -r requirements.txt
   ~~~

3. Start the application:

   ~~~bash
   streamlit run app.py
   ~~~

Streamlit will print the local URL where the application is available.

> Run instructions describe the current application. They do not imply that planned roles, workflows or future database changes are already available.

## Development principles

- Inspect the current implementation before changing code or configuration.
- Preserve existing data and create backups before potentially destructive changes.
- Clearly distinguish the existing application from any test or deployment environment.
- Enforce permissions in backend logic.
- Keep secrets out of source control and logs.
- Add tests for permissions, scheduling rules, working-time calculations, training, data integrity and backup/restore as those features are implemented.
- Document significant changes and problems.
- Do not describe a change as published until its success has been verified.

---

Built as a practical portfolio project to explore application development, data handling and visualisation with Python.
