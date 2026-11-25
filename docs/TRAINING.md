# Intern training plan

How we bring three new interns up to speed before they own tracks A, B and C in [docs/TASKS.md](TASKS.md). The plan has four parts: preparation, a structured first week, track-specific ramp-up in weeks 2–3, and checkpoints that tell us whether it worked.

**Assumptions:** the interns know basic Python and Git, and have not built a web app, used SQLAlchemy, or worked in healthcare software. If they know more, shorten the workshops; do not skip the domain day or the security session.

**The goal by Friday of week 1:** each intern has merged a starter task (S1, S2 or S3), can run all checks locally, understands the five rules that must never be broken (see [Day 3](#day-3-testing-and-the-pull-request-workflow)), and can explain a patient's journey through the hospital in their own words.

## Part 1: Before day 1

### Mentor checklist (do this the week before)

- [ ] The three interns have GitHub accounts and are added to the repository with write access to feature branches. Branch protection on `main` requires the **Main gate passed** check ([README](../README.md)).
- [ ] Each intern has a working laptop with Git and a code editor (the setup script installs the rest). Track C also needs a **Windows 10/11 machine or VM** for installer and printing work.
- [ ] A team channel exists, with the stand-up time and the Friday demo time fixed in everyone's calendar.
- [ ] A short **hospital visit** is booked for day 4 (a small clinic or nursing home that agrees to being observed; no patient data is collected). See [Day 4](#day-4-domain-and-security).
- [ ] Starter tasks S1, S2 and S3 are created as GitHub issues, each with its "done when" from TASKS.md.
- [ ] A **practice repository** (a copy of this project in a sandbox) is ready for the git workflow exercise on day 3.
- [ ] The workshop materials in [Part 5](#part-5-materials-to-prepare) are ready or have an owner and a date.

### Interns' pre-work (about 3 hours, sent a week ahead)

1. Read [README.md](../README.md) and [PLAN.md](../PLAN.md) sections 1, 2 and 6 (principles, users, usability).
2. Follow [docs/SETUP.md](SETUP.md) in a fresh clone (install Git, run the setup script). Send the mentor a screenshot of `uv run pytest` passing. If it fails, fix it together on day 1, not in front of the group.
3. Write 5 lines about the last time you used a hospital or pharmacy: what was slow or confusing? We use these on day 4.

## Part 2: Week 1 schedule

Each day is about 6 working hours: workshops in the morning, hands-on work in the afternoon, a 30-minute wrap-up at the end. Every workshop ends with an exercise the interns finish themselves; we do not rely on slides.

### Day 1: Welcome and the big picture

| Time | Session | Output |
|---|---|---|
| 1 h | **Welcome.** Team, rhythm (stand-up, Monday planning, Wednesday pairing, Friday demo), how to ask for help (stuck 2 hours: ask; stuck a day: raise at stand-up) | Everyone knows who to ask |
| 1.5 h | **What we are building and for whom.** Walk through [PLAN.md](../PLAN.md): offline first, one device or many, who uses it, why small hospitals. Look at the [wireframes](wireframes/README.md) | Each intern explains the three deployment tiers in their own words |
| 1.5 h | **Setup clinic.** Follow [docs/SETUP.md](SETUP.md): clone, run the setup script, start the app, run all checks. Fix anything that fails, pair-by-pair | `uv run pytest --cov` green on every laptop |
| 2 h | **Codebase tour.** Walk the repo: `main.py`, `config.py`, `db.py`, the module layout, `tests/conftest.py`. Trace one request, `GET /health`, from route to response | Each intern draws the request path on paper |
| 0.5 h | Wrap-up: what is still unclear? | Questions list for tomorrow |

### Day 2: The tools we build with

| Time | Session | Exercise |
|---|---|---|
| 1.5 h | **FastAPI and HTMX.** Routes, dependencies, Pydantic validation, Jinja2 templates, returning an HTML fragment for HTMX to swap in | Build a throwaway `/greeting` page whose button loads a fragment (in a scratch folder, not the repo) |
| 1.5 h | **SQLAlchemy 2.0.** Models, sessions, queries, transactions, why a session per request | Create a `Note` model, insert and query rows in a test using the `session` fixture |
| 1 h | **Alembic.** Why every schema change needs a migration; autogenerate; batch mode on SQLite | Generate a migration for `Note`, apply it, check it with `alembic check` |
| 2 h | **Hands-on lab.** Combine the three: a `Note` form that saves to the database and lists notes, with a test | Working scratch app and a test; mentor reviews each one |

### Day 3: Testing and the pull request workflow

This is the most important day for habits. The workshops teach the [testing rules in CLAUDE.md](../CLAUDE.md) by doing them.

| Time | Session | Exercise |
|---|---|---|
| 1.5 h | **Unit and integration tests.** What goes where, the shared fixtures, a real SQLite database instead of mocks, naming tests by behaviour | Write one unit test and one integration test for the `Note` lab; run only the unit tests with `-m "not integration"` |
| 1 h | **Property-based tests with Hypothesis.** State an invariant, let the library find the counterexample | Write a Hypothesis test that a function formatting rupees in lakh/crore grouping never loses a digit |
| 1 h | **The Main gate.** What each security check catches (CodeQL, Bandit, dependency audit, secret scanning) and what to do when it fails: fix the finding, never silence it | Deliberately trigger a Bandit finding in the practice repo and fix it properly |
| 2 h | **Git and pull-request workflow in the practice repo.** Branch naming (`<task-id>-<short-name>`), draft PR early, small PRs, squash-merge, review etiquette | Each intern opens a PR; another intern reviews it using the checklist in [Part 4](#part-4-reviewing-each-others-work); the mentor merges |
| 0.5 h | Wrap-up | |

**The five rules every intern must be able to state by the end of day 3:**

1. Clinical and financial records are **append-only**; corrections add a new row.
2. Syncable models inherit `SyncBase`, and **no bulk `update()`/`delete()`** on them.
3. The app works **offline**: no CDN links, no calls to the internet in a request path.
4. **Money is `Decimal`**, never `float`.
5. **Never store full Aadhaar numbers or log patient details.** Test data is always invented.

### Day 4: Domain and security

| Time | Session | Output |
|---|---|---|
| 3.5 h | **Hospital visit** (with the mentor). Watch the front desk, a doctor's consultation if the clinic allows, and the pharmacy counter. No photos of patients, no patient data. Interns note what is slow, what is on paper, and what would go wrong if the power cut | Each intern brings back 5 observations and 2 "how would our system handle this?" questions |
| 1 h | **Debrief.** Compare observations with the wireframes and PLAN.md. What did the wireframes miss? File each gap as a GitHub issue labelled `wireframe-gap` | At least 3 issues filed by the team |
| 1.5 h | **Privacy and security.** Why hospital data is sensitive, DPDP in plain language, what "consent" means here, OWASP basics (sessions, CSRF, injection), why we hash PINs, what an audit log is for | Each intern lists three ways a careless commit could leak patient data |

If a hospital visit is not possible, replace the first two sessions with a recorded walkthrough of the wireframes by someone who has worked in a hospital, and have the interns role-play a reception-to-billing-to-pharmacy journey, with one playing the patient.

### Day 5: Ship something

| Time | Session | Output |
|---|---|---|
| 3.5 h | **Starter tasks.** Each intern works on S1, S2 or S3 (from TASKS.md) with the mentor available. Draft PR opened by lunchtime | Draft PR, green CI |
| 1 h | **Review round.** Each intern reviews the PR of the intern assigned to them in the [review rotation](TASKS.md#tracks-and-ownership) | Review comments given and answered |
| 1 h | **Demo and retro.** Each intern demos a merged starter task (or the working branch) in 5 minutes. Retro: what worked, what to change | Retro notes; the mentor adjusts week 2 |

**Starter tasks are not graded.** If one is not finished on Friday, the intern keeps working on it on Monday and demos it then. The point is to practise the whole workflow once, with help.

## Part 3: Weeks 2–3, track-specific ramp-up

From week 2 each intern starts their first real task. Alongside it, each gets a short deep dive for their track. The deep dives are done in pairs with the mentor and take about half a day each, spread across the two weeks. The mentor does not do the task for the intern; they teach the concepts the task needs.

| Track | First task | Deep dives |
|---|---|---|
| **A: Data and sync core** | A1 (IDs, device identity, `SyncBase`) and A2 (hybrid logical clock) | 1. **UUIDv7 and why IDs are made on the device** (reading: PLAN.md §5.4). 2. **How clocks go wrong** (a PC with a dead CMOS battery, daylight saving) and what a hybrid logical clock fixes. 3. **SQLAlchemy events and mixins** (`before_flush`, `do_orm_execute`), needed by A3. 4. **Hypothesis in depth**: stateful and model-based tests |
| **B: Access and UI** | B1 (UI shell) and B2 (users and roles) | 1. **Jinja2 macros and HTMX patterns**: partial updates, forms, validation errors inline. 2. **Keyboard-first and touch-friendly UI**: focus order, shortcuts, 44 px targets, working at 1366×768. 3. **Authentication done safely**: password hashing, sessions, CSRF, why we do not invent crypto (preparation for the mentor-reviewed B3). 4. **Accessibility basics**: labels, contrast, screen reader checks |
| **C: Platform and print** | C1 (desktop launcher), then C2 (SQLCipher spike) | 1. **How a desktop shell works**: pywebview, running Uvicorn in a thread, shutting down cleanly. 2. **Packaging**: PyInstaller one-folder builds, what Inno Setup does, why antivirus complains. 3. **Printing**: CSS page sizes, thermal printers and ESC/POS, why we test on real paper. 4. **Writing a spike report**: what an ADR is, how to record what failed |

**Pairing rotation.** On Wednesdays the three interns rotate through two pairings, one hour each, so every intern has paired with both others by the end of week 3. The pair works on whatever one of them is stuck on; the aim is to spread knowledge, not to finish tasks.

## Part 4: Reviewing each other's work

Reviewing is a skill we teach, because every pull request needs a second pair of eyes from another intern. Teach this checklist on day 3 and keep it in the PR template once one exists.

**Reviewer checklist:**

- [ ] Does the PR do what the task's "done when" says, and nothing else?
- [ ] Are there tests: unit for logic, integration for routes? Would they fail if the code were wrong?
- [ ] Do records stay append-only? No bulk updates on syncable tables? Money as `Decimal`?
- [ ] No patient data, secrets or CDN links? User-visible text goes through `_()`?
- [ ] Is there an Alembic migration for any schema change?
- [ ] Is it small enough to review (under about 400 changed lines)?
- [ ] Is the code readable: names, no dead code, comments explain *why*?

**How to give feedback:** be specific, ask questions before making demands ("what happens if the clock goes backwards here?"), mark nitpicks as optional, and say what is good. **How to receive it:** answer every comment, push fixes as new commits, do not take it personally.

## Part 5: Materials to prepare

None of these exist yet. Each needs an owner (the mentor, or an experienced developer on the team) before day 1.

| Material | Used on | Notes |
|---|---|---|
| Setup guide with common failures (Windows quirks, proxy settings, uv install) | Day 1 | Start from CONTRIBUTING.md; add what goes wrong in practice |
| Scratch exercises for days 2 and 3 (`Note` lab, rupee formatter, Bandit trap) | Days 2–3 | A small repository or folder of starter files, with solutions held back by the mentor |
| Practice repository for the git workflow | Day 3 | A copy of this project with the Main gate, safe to break |
| Hospital observation sheet (what to look for, what not to record) | Day 4 | One page |
| Glossary: UHID, OPD, IPD, MLC, TPA, PM-JAY, ABHA, ABDM, MAR, H1 register, FEFO | Day 1 onward | Plain-language, one line each; grows during the internship |
| PR template and reviewer checklist | Day 3 | Add `.github/pull_request_template.md` from Part 4 |

## Part 6: Checkpoints

We look at these to decide whether the training worked and where to adjust. They are for the mentor and the team, not exams.

**End of week 1** (every intern can tick all):

- [ ] Runs the app and all checks locally without help.
- [ ] Has opened a PR, reviewed another PR, and merged (or is close to merging) a starter task.
- [ ] Can state the five rules and say why each exists.
- [ ] Can explain a patient's journey from registration to billing to pharmacy.
- [ ] Knows who to ask, and has asked at least one question in the channel.

**End of week 3:**

- [ ] Has merged their first real task (A1, B1 or C1) with tests and a clear PR description.
- [ ] Has given at least three useful reviews, and received and addressed review comments.
- [ ] Has paired with each of the other two interns.
- [ ] Has written down one thing in the docs or an ADR that was missing or wrong.

**If someone is behind:** shorten their next task rather than extending the week, pair them with the mentor for a day, and ask what is blocking them (setup, concepts or confidence), because the fix is different for each.

**Feedback on the training itself.** At the end of weeks 1 and 3, ask each intern anonymously: what was most useful, what was a waste of time, what do you wish we had covered? Update this document and the materials before the next cohort.

## Reference

- Week-by-week tasks and interface contracts: [docs/TASKS.md](TASKS.md)
- Standing rules and testing rules: [CLAUDE.md](../CLAUDE.md)
- Workflow and module layout: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Screens: [docs/wireframes/](wireframes/README.md)
- Tutorials by topic: "Learning resources" at the end of [docs/TASKS.md](TASKS.md)
