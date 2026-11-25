# VSHMS: Hospital Management System for Small Hospitals

**Status:** Draft plan, v0.1 (2026-11-25)
**Target:** Indian hospitals and nursing homes with 5–50 beds, and clinics with a day-care or minor-OT setup.

---

## 1. Product principles

1. **Offline first, sync optional.** A single PC with no internet must run the whole hospital. Networking adds features but nothing depends on it.
2. **Each install is a complete node.** One codebase, one data format, and the same app on every device. A hospital grows from 1 to N devices by pairing them, with no migration.
3. **Built-in compliance.** Statutory registers, record retention, consent and audit trails come from normal daily use. Staff don't fill them in as a separate job.
4. **Usable by a receptionist on day one.** Common tasks take no more than three screens. The app works keyboard-first for billing staff and touch-friendly for nurses and doctors. It runs in English and a regional language.
5. **Fits cheap hardware and unreliable power.** It runs on a 4 GB RAM Windows 10 PC, survives power cuts without data loss, and prints on whatever printer the hospital already owns.
6. **Clinical records are append-only.** A record is corrected by adding an amendment. Nothing is overwritten. This makes the records medico-legally defensible and also makes sync conflicts mostly disappear (§5).

---

## 2. Users and scope

| Role | Main jobs |
|---|---|
| Reception / front office | Register patients, issue OPD tokens and appointments, collect deposits, admit patients |
| Doctor | Review the OPD queue, write consultation notes and prescriptions, place orders, do IPD rounds, write discharge summaries |
| Nurse | Take vitals, chart medications (MAR), keep intake/output, write nursing notes, manage beds |
| Pharmacist | Dispense against prescriptions, sell over the counter, manage stock, batches and expiry, keep Schedule H1/X registers |
| Lab technician | Collect samples, enter results, print reports |
| Billing / accounts | Run IPD running bills, packages, insurance/TPA and PM-JAY claims, day-end cash closing, Tally export |
| Owner / administrator | Masters and rate lists, users, MIS dashboards, NABH indicators, backups |

In a small hospital one person often holds several of these roles, so a user can hold several roles at once and switch between them quickly.

**Out of scope for v1:** full PACS (DICOM viewing), HR and payroll, full financial accounting (the app exports to Tally instead), diet/kitchen, laundry, and blood bank. Full ICU device integration is also out; vitals are entered by hand.

---

## 3. Functional modules

| # | Module | Key features | Phase |
|---|---|---|---|
| M1 | **Patient registration** | UHID; ABHA number/address field; search by mobile number (one phone often serves a whole family), name or UHID. Age can be entered as years, months or days when the date of birth is unknown. Records C/o (S/o, D/o, W/o) and guardian, address with PIN code, state and district, and patient category (General/BPL/Staff/PM-JAY/TPA). Photo capture | 1 |
| M2 | **OPD** | Token queue per doctor, appointments, walk-ins, vitals at triage, consultation template, follow-up dates, revisit fee rules | 1 |
| M3 | **E-prescription** | Generic name first (NMC guidance), brand optional. Favourites and per-doctor templates, "repeat last Rx", drug-allergy warning, dose/frequency shorthand (1-0-1, BD, TDS, SOS) with regional-language instructions on the printout. Doctor's registration number printed | 1 |
| M4 | **Billing** | Service rate list (several tariffs: general, TPA, PM-JAY, CGHS), OPD bills, receipts, refunds, discounts with approval, and a UPI QR on the bill (generated offline). GST-compliant invoice series per device. Day-end cash/UPI/card closing | 1 |
| M5 | **Pharmacy** | Item master with HSN/GST, batches, expiry, MRP, barcode scanning, FEFO picking, sales against Rx or over the counter, returns, Schedule H1/X/NDPS registers produced automatically, purchase/GRN, near-expiry and reorder alerts | 1 |
| M6 | **Reports and MIS** | Daily census, collections, doctor-wise revenue, pharmacy sales/stock, outstanding dues, export to Excel/PDF | 1 |
| M7 | **Admin and setup** | Setup wizard, masters, users and roles, print-template designer, backup/restore, audit log viewer | 1 |
| M8 | **IPD / ADT** | Admission (with deposit), bed board (ward/room/bed with status), transfers, automatic daily bed/nursing/visit charges, running bill, discharge workflow with clearance checklist | 2 |
| M9 | **Nursing** | Vitals charting with trends, MAR (medication administration record), intake/output, nursing notes, shift handover, care plans | 2 |
| M10 | **Clinical documentation** | Initial assessment (within the NABH time limit), progress notes, doctor's orders, consent forms (bilingual, signed on screen or scanned), discharge summary in the NABH-recommended format | 2 |
| M11 | **Laboratory** | Test master with reference ranges by age and sex, sample barcodes, result entry, delta check, critical-value flag, report printing with authorised signatory, outsourced-lab tracking | 2 |
| M12 | **Insurance / TPA / PM-JAY** | Payer master, pre-authorisation checklist and document bundle, package billing (PM-JAY HBP packages), claim status tracking, co-pay split, deduction reconciliation | 2 |
| M13 | **Statutory registers** | MLC register and police-intimation print, birth and death register (data for the CRS portal), MCCD (Form 4/4A, ICD-coded), notifiable-disease and IDSP/IHIP lists, Nikshay (TB) notification list | 2 |
| M14 | **Multi-device sync (LAN)** | Device pairing by QR code, hub on the LAN, conflict review screen | 3 |
| M15 | **Cloud relay** | Off-site encrypted backup, remote dashboard for the owner/doctor, multiple branches, internet bridge for ABDM | 4 |
| M16 | **ABDM** | M1 (create/verify ABHA, Scan & Share registration), M2 (HIP: link care contexts, share FHIR records with consent), M3 (HIU: fetch records), HFR/HPR IDs | 4 |
| M17 | **OT** | OT scheduling, WHO surgical safety checklist, anaesthesia record, implant/consumable capture, OT notes | 5 |
| M18 | **Special registers** | PC-PNDT Form F (if the hospital has USG), MTP registers (kept confidential), biomedical waste daily log and Form IV annual report | 5 |
| M19 | **Quality (NABH)** | Quality indicator capture (most counted automatically from transactions), incident reporting, patient feedback, monthly indicator report | 5 |
| M20 | **Integrations** | NHCX claims, lab analyzer interfacing (ASTM/HL7), SMS (TRAI DLT templates)/WhatsApp notifications, tablet-optimised layouts | 5+ |

---

## 4. Indian standards and regulations compliance map

> Legal details must be checked with a healthcare compliance consultant and the hospital's CA before release. State-level Clinical Establishments rules vary, so retention periods and similar values are **configurable** with conservative defaults.

| Standard / law | What the system does |
|---|---|
| **NABH**: Entry-Level / SHCO standards and the 5th-edition hospital standards | Initial assessment timestamps, standard discharge summary, informed consent in the patient's language, medication management (high-alert and look-alike/sound-alike drug flags, MAR), patient rights display, quality indicators (M19), access-controlled medical records, audit trail. Ships an "NABH readiness" checklist report |
| **MoHFW EHR Standards for India (2016)** | Coding with **ICD-10** (ICD-11 ready) for diagnoses, **SNOMED CT** (free through the India NRC) for clinical terms, **LOINC** for lab tests, **FHIR R4** for exchange. Unique patient ID (UHID), audit trail, role-based access |
| **ABDM** (Ayushman Bharat Digital Mission) | ABHA linking, HFR facility ID, HPR doctor IDs, consent-based record sharing using the NRCeS FHIR profiles (OPConsultation, Prescription, DischargeSummary, DiagnosticReport, Invoice). Eligible for DHIS incentives once certified |
| **Clinical Establishments (Registration & Regulation) Act 2010** and state Acts | Rate list display/printout, keeping and producing medical records, standard treatment protocol templates |
| **MCI (Professional Conduct) Regulations 2002 / NMC regulations** | Records kept at least 3 years (default retention much longer, see §7), copy of records issued within 72 h of a request (tracked workflow), doctor's registration number on prescriptions, generic names. Configurable so it can follow NMC regulation changes |
| **Drugs & Cosmetics Act 1940 / Rules 1945** | Schedule H1 register (patient, prescriber, drug, quantity; kept 3 years) and Schedule X register produced automatically from sales; drug licence number on invoices; batch/expiry traceability |
| **NDPS Act** | Separate narcotics stock register with double sign-off for dispensing and wastage |
| **GST** | Healthcare services by a clinical establishment are exempt. Pharmacy and non-exempt items are taxed by HSN. Rule engine covers cases like room rent above the threshold (currently ₹5,000/day non-ICU at 5%). Invoice numbers are unique per financial year (April–March) and at most 16 characters, with a separate series per device |
| **DPDP Act 2023 + DPDP Rules 2025** (phased commencement) | Purpose-specific consent notice at registration (bilingual), consent records, data principal request workflow (access/correction; erasure limited by medical retention law), breach register and notification workflow, data minimisation |
| **IT Act 2000 / SPDI Rules 2011** | Reasonable security practices: encryption, access control, audit logs |
| **Aadhaar Act** | Full Aadhaar numbers are **never stored**. Aadhaar is used only for ABHA creation through ABDM APIs. Other ID proofs are stored masked |
| **RBD (Amendment) Act 2023** | Birth/death register, MCCD Form 4/4A, data ready to enter on the CRS portal within 21 days |
| **PC-PNDT Act** | Form F records with mandatory fields, monthly report, kept for the statutory period |
| **MTP Act** | Admission register and consent forms, hidden from general search |
| **Biomedical Waste Management Rules 2016** | Daily bag-weight log by colour category, Form IV annual report |
| **IDSP/IHIP, Nikshay** | Worklists of notifiable cases created automatically from diagnosis codes |
| **Telemedicine Practice Guidelines 2020** (later) | Teleconsult consent and record format, if teleconsults are added |

---

## 5. Architecture

### 5.1 Deployment tiers (one app, three configurations)

```
Tier 1: SOLO                 Tier 2: CLINIC LAN                       Tier 3: CONNECTED
┌───────────────┐            ┌────────────┐  Wi-Fi/LAN  ┌──────────┐    ┌────────────────────┐
│  Reception PC │            │ Hub PC     │◄───────────►│ Pharmacy │    │ Cloud relay (India │
│  (full node)  │            │ (full node,│◄──────┐     │ (node)   │    │ region)            │
│  SQLite       │            │  serves    │       │     └──────────┘    │ • encrypted backup │
│  USB backup   │            │  browsers) │  ┌────┴──────────┐          │ • remote dashboard │
└───────────────┘            └────────────┘  │Doctor tablet  │          │ • ABDM callbacks   │
                                   ▲         │(browser/thin) │          └─────────▲──────────┘
                                   └─────────┴───────────────┘                    │ internet
                                                                       Tier-2 hub ┘ (when available)
```

- **Tier 1 (Solo):** one PC, no network. Backups go to a USB drive or second disk automatically.
- **Tier 2 (LAN):** one PC is the **hub**. Other devices are either:
  - **full nodes** (app installed, own local database, keep working if Wi-Fi drops, sync when it returns), or
  - **thin clients** (any browser or tablet on the LAN opens the hub's address; nothing to install).
  The LAN needs no internet.
- **Tier 3 (Connected):** the hub also syncs to a cloud relay when internet is available. Needed for remote access, multiple branches, off-site backup, and **ABDM** (the ABDM gateway calls back to a public HIP endpoint, which a PC behind a home router cannot provide).

### 5.2 Node internals

```
┌───────────────────────── VSHMS node ─────────────────────────┐
│  UI: server-rendered HTML (Jinja2 templates + HTMX/Alpine),  │
│      plus SQLAdmin master-data screens, shown in a pywebview │
│      desktop window or any browser                           │
│        │  HTTP (localhost, or LAN for thin clients)          │
│  Local server: FastAPI on Uvicorn                            │
│   ├─ Domain modules (patients, opd, billing, pharmacy, ...)  │
│   ├─ Rules (GST, tariffs, packages, retention, permissions)  │
│   ├─ Sync engine (outbox/inbox, HLC, merge rules)            │
│   ├─ Print engine (HTML templates → A4/A5, ESC/POS thermal)  │
│   ├─ Job queue: Huey on SQLite (ABDM, SMS, backups; retried) │
│   └─ Audit log (append-only, hash-chained)                   │
│  SQLite (WAL mode) encrypted with SQLCipher + file store     │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 Technology choices

| Concern | Choice | Why |
|---|---|---|
| Language | **Python 3.12+**, with type hints checked by mypy | The team's choice. Mature libraries for every need below |
| Web framework | **FastAPI** | Pydantic types end to end and auto-generated OpenAPI docs, which suit the sync protocol, ABDM/FHIR and any later mobile or React client. Each module has HTML routes for the UI and JSON routes for sync and integrations |
| ORM and migrations | **SQLAlchemy 2.0** (typed ORM) + **Alembic** | One code path for SQLite on devices and PostgreSQL on the relay. Session events give a reliable hook for the sync outbox (§5.4) |
| Master-data screens | **SQLAdmin** | Ready-made list/create/edit screens for drugs, lab tests, rate lists, wards and beds, doctors and users, protected by the app's own login and role checks. Day-to-day workflows (registration, billing, dispensing) get purpose-built screens instead |
| UI | **Jinja2 templates + HTMX + Alpine.js**, with a small JS hotkeys layer | The UI stays almost entirely in Python, with no separate front-end build. Pages are light enough for 4 GB PCs and thin-client tablets, and work the same in the desktop window and LAN browsers |
| Forms and validation | **Pydantic** models validate form posts. Shared Jinja2 macros render fields and errors | One validation layer for HTML forms and JSON APIs |
| Auth and security | Session cookies (Starlette `SessionMiddleware`), **argon2-cffi** password and PIN hashing, a role/permission table checked by a FastAPI dependency (`require("billing.refund")`), CSRF tokens sent by HTMX in a header | FastAPI has no built-in login system, so this is built in Phase 0 and gets a security review before the pilot |
| i18n | **Babel** with the Jinja2 i18n extension (gettext `.po` files) | Standard translation workflow for Hindi and regional languages |
| App server | **Uvicorn** (without uvloop on Windows) | The standard FastAPI server, works on Windows and Linux. It serves localhost and, on the hub, the LAN |
| Desktop shell | **pywebview** window pointing at the local server, packaged with **PyInstaller** and an **Inno Setup** installer | A native window that uses the system's WebView2, not a bundled browser, so the installer stays small. Minimum OS: Windows 10/11 64-bit, Ubuntu 22.04+ |
| Local DB | **SQLite** in WAL mode, `synchronous=FULL` for financial tables, encrypted with **SQLCipher** through SQLAlchemy's built-in `sqlite+pysqlcipher` dialect and the `sqlcipher3` driver | Zero administration, survives power cuts, a single file that is easy to back up. SQLAlchemy supports SQLCipher directly; Phase 0 only has to confirm the driver packages cleanly on Windows (§11) |
| Background jobs | **Huey** with SQLite storage | No Redis needed. Queues ABDM calls, SMS, backups and sync retries |
| Cloud relay | The same FastAPI app on **PostgreSQL**, hosted in an Indian region | Reuses the code. Keeping data in India suits ABDM and hospital expectations |
| Sync | **Custom change-log replication** in Python (§5.4) | Medical data needs domain-specific merge rules (stock ledgers, invoice series, beds). Off-the-shelf CRDT or sync services fit these poorly. A small, auditable protocol is safer |
| Interoperability | `fhir.resources` (Pydantic FHIR R4 models) with NRCeS profile mappings | Needed for ABDM and NHCX. Only a mapping layer, so the internal schema stays simple |
| Printing | HTML/CSS print templates printed through the webview's print dialog. **python-escpos** prints receipts silently on thermal printers. Server-side PDF (WeasyPrint or ReportLab) for saved and shared documents | Hospitals use pre-printed letterheads, A5 prescriptions and 80 mm receipts, and templates must be editable |
| Other libraries | `openpyxl` (Excel import/export), `lxml` (Tally XML), `qrcode` (UPI and pairing QR codes), `uuid6` (UUIDv7; in the standard library from Python 3.14) | Well-maintained and pure Python or wheel-available on Windows |
| Testing | **pytest**, **Hypothesis** for property-based sync tests, Playwright for UI flows | Hypothesis suits the randomized multi-device sync simulation |
| Updates | Signed update packages that install online **or from a USB drive** | Many sites have poor internet |

### 5.4 Data model and sync design

The design rules below are fixed from day 1, even though multi-device sync ships in Phase 3.

**Identity**
- Every row has a primary key generated on the device that created it (**UUIDv7**), plus `site_id`, `device_id`, `created_at`, `updated_hlc` (hybrid logical clock) and `deleted` (a tombstone instead of a hard delete).
- Human-readable numbers never need central coordination:
  - UHID: `<site code><device code>-<seq>` (for example `KM1-004512`). A short alias is printed on the patient card.
  - Invoice and receipt numbers: a GST-valid series per device per financial year (for example `R1/26-27/00123`).
  - OPD tokens: per doctor per day. Assigned by the hub when it is reachable, otherwise by the device with a device prefix.

**Classes of data and their merge rules**

| Class | Examples | Rule |
|---|---|---|
| **A. Append-only facts** | Vitals, notes, orders, prescriptions, results, payments, charges, stock movements, audit entries | Never updated. A correction is a new row that amends or voids the original. **Conflicts cannot occur** |
| **B. Ledgers** | Stock on hand, patient account balance, deposits | Stored as derived sums of class-A movements, so concurrent sales merge correctly. Negative stock after a merge raises an alert instead of blocking |
| **C. Mutable records** | Patient demographics, masters (items, rates, doctors) | Per-field last-writer-wins by HLC. If two devices change the same field while offline, the older value goes to a **conflict review** screen |
| **D. Exclusive resources** | Bed occupancy, OT slots | The hub takes a soft lock when it is reachable. If two devices allot the same bed while offline, both are kept and a conflict is raised for a person to resolve. The bed board shows these conflicts clearly |

**Protocol**
1. Every syncable model inherits from a common `SyncBase` mixin (ID, HLC, tombstone and device fields). A SQLAlchemy `before_flush` session event stamps the HLC and writes an `outbox` entry for each new, changed or deleted row, so the row and its outbox entry commit in the same transaction. Bulk `update()`/`delete()` statements skip the ORM's flush, so a `do_orm_execute` event **rejects** them on syncable tables.
2. A node **pushes** its outbox to the hub over HTTPS (TLS certificate pinned at pairing). The hub gives each change a monotonic `server_seq`.
3. A node **pulls** changes after its last `server_seq`, applies the merge rules and records the new cursor. Changes are applied idempotently, keyed by change ID.
4. The hub syncs to the cloud relay with the same protocol (the hub is a client of the relay).
5. Files (scans, photos, PDFs) are content-addressed by SHA-256 and synced lazily after the metadata.
6. **Pairing:** the hub shows a QR code containing a one-time token and its certificate fingerprint. The new device scans it or types a code. An administrator can revoke a device, which wipes its local data the next time it connects.
7. Schema migrations are versioned. A node with an older schema can still push but is told to upgrade before it pulls.

### 5.5 Core entities (simplified)

`Patient` · `Encounter` (OPD / IPD / Emergency / Daycare) · `Practitioner` · `Department` · `Appointment/Token` · `Observation` (vitals, lab values) · `ClinicalNote` · `Diagnosis` (ICD/SNOMED) · `MedicationOrder` · `MedicationAdministration` · `ServiceOrder` (lab, radiology, procedure) · `Result` · `Bed`/`BedAssignment` · `Consent` · `Document` · `ChargeItem` · `Invoice` · `Payment`/`Deposit`/`Refund` · `Package` · `Payer`/`Claim` · `Item`/`Batch`/`StockMovement` · `Supplier`/`PurchaseOrder`/`GRN` · `User`/`Role`/`Device` · `AuditEvent` · `StatutoryRegisterEntry`

Each entity has a documented FHIR mapping (for example `Encounter` → FHIR Encounter, `MedicationOrder` → MedicationRequest).

---

## 6. Usability design

**Per-role home screens.** After login each role sees only its own work queue. A pharmacist sees pending prescriptions; a nurse sees the patients due for medicines.

**Speed for front-desk staff**
- Keyboard-first flows with consistent shortcuts (Tally-style, which billing staff already know): `F2` new registration, `F3` search, `F5` bill, `Ctrl+P` print, `Esc` back.
- Registering a patient and printing a token: **under 30 seconds**. Searching by the last 4+ digits of the mobile number shows a family list.
- Billing re-uses the last tariff and payer, and the UPI QR appears automatically on the bill.

**Low-typing clinical entry**
- Prescription and note templates, favourites, "copy from last visit", and voice dictation (where available).
- Dose shorthand expands automatically (`1-0-1 x5d AF` → *one tablet morning and night for 5 days after food*) and prints in the patient's language.
- Large touch targets and a tablet layout for ward rounds and nursing.

**Indian context built in**
- Languages: English and Hindi at launch, with a pluggable language-pack system for Bengali, Marathi, Tamil, Telugu, Kannada, Gujarati and others. Printouts can be bilingual.
- Indian formats: ₹ amounts in lakh/crore grouping, DD-MM-YYYY dates, financial-year-aware numbering, and a PIN code → district/state lookup that works offline.
- Approximate age, family/guardian fields, and staff/BPL/free-treatment categories.

**Forgiving**
- Drafts autosave every few seconds, so a power cut loses at most a few seconds of typing.
- Undo within 10 minutes for non-financial mistakes. Financial corrections follow a void-and-reissue flow with a reason.
- Fast user switching with a **4-digit PIN** on shared PCs (very common), and auto-lock when idle.

**Onboarding**
- A setup wizard (target: under 30 minutes) with **pre-loaded masters**: ICD-10, a common lab-test master with reference ranges, a generic drug list, a sample service rate list, and print templates. Existing patient and item lists can be imported from Excel.
- In-app guided tours and short regional-language training videos. A "practice mode" sandbox database for staff training.

**Hardware assumptions:** Windows 10, i3 processor, 4 GB RAM, SSD recommended. Works with an 80 mm thermal printer, any A4/A5 printer, a USB barcode scanner and a webcam for patient photos. A UPS is strongly recommended.

---

## 7. Security, privacy and data safety

- **Encryption:** SQLCipher at rest; backups encrypted with the hospital's recovery key (printed and stored offline at setup); TLS for all sync.
- **Access control:** role-based permissions, with stricter rules for sensitive categories (MTP, PC-PNDT, HIV and psychiatric records are hidden from general search; opening one is logged with a reason).
- **Audit trail:** every view, create, amend and print of clinical or financial data is logged in an append-only, **hash-chained** log that lets an auditor detect tampering.
- **Retention:** configurable per record type. Defaults: medical records kept for at least the statutory 3 years, but **not purged automatically** (MLC, pediatric, MTP and PC-PNDT records need longer). Old records are archived, never deleted silently.
- **Backups (3-2-1):** an automatic local snapshot every few hours plus daily, a daily reminder to copy to a USB drive (enforced by a status banner), and optional cloud backup. **Monthly test restores** are verified automatically against checksums. Restore is a one-screen wizard.
- **DPDP:** a consent notice at registration, consent records, a data-principal request tracker, a breach register, and least-privilege defaults.
- **Device loss:** devices can be remotely revoked (Tier 3), and data on stolen devices is encrypted.

---

## 8. Integrations (all optional, run from a queue, never blocking)

| Integration | Notes |
|---|---|
| **Tally** | Day-wise voucher export (sales, receipts, purchases) as Tally XML. Most small hospitals already have an accountant using Tally |
| **UPI** | A dynamic `upi://pay` QR on the bill, generated offline. Settlement is reconciled by hand in v1; payment-gateway webhooks come later |
| **SMS / WhatsApp** | Appointment reminders and report-ready alerts. SMS needs TRAI DLT template registration |
| **ABDM** | Phase 4, through the cloud relay (§5.1) |
| **PM-JAY TMS / NHCX** | v1 supports package billing, the pre-auth document checklist and a claim-file bundle. API integration through NHCX comes later |
| **Lab analyzers** | ASTM/HL7 interface for common semi-automatic and automatic analyzers, Phase 5+ |

---

## 9. Roadmap

Rough sizes assume a team of 3–4 developers plus 1 domain or QA person.

| Phase | Scope | Exit criteria | Size |
|---|---|---|---|
| **0. Foundations** | FastAPI app skeleton, SQLAlchemy models with the `SyncBase` mixin (IDs, HLC, outbox, tombstones), Alembic migrations; audit log; login, sessions, CSRF, roles/permissions and PIN switching; SQLAdmin wired to that login; Babel i18n; print engine; backup/restore; PyInstaller + pywebview + Inno Setup installer. **Spikes first:** `sqlcipher3` packaged on Windows, packaged-app start time and RAM on a 4 GB PC, printing through WebView2 | Empty app installs on Windows 10 and Ubuntu; backup and restore round-trip passes; power-cut test passes; cold start under 5 s; auth passes a security review | ~8 wks |
| **1. Solo MVP (OPD + Pharmacy + Billing)** | M1–M7 | A pilot clinic runs **one full week of OPD** on one PC with no paper fallback | ~12 wks |
| **2. IPD and compliance** | M8–M13 | A pilot hospital with 10–30 beds runs admissions to discharge, including an insurance case; statutory registers are reviewed by a compliance consultant | ~14 wks |
| **3. LAN multi-device** | M14, thin clients, conflict review | Three or more devices for two weeks; a randomized sync test suite passes; no data loss after cutting Wi-Fi for a day | ~8 wks |
| **4. Connected** | M15, M16 (ABDM M1→M2→M3 sandbox, then certification), remote dashboard | ABDM sandbox certification; off-site restore drill | ~10 wks |
| **5. Depth** | M17–M20 | Driven by pilot feedback | ongoing |

Multi-device sync ships in Phase 3, but the **data layer is sync-ready from Phase 0**. Adding it later is a configuration change, not a migration.

---

## 10. Quality and testing

- **Sync correctness:** property-based tests with N simulated devices, random partitions, clock skew and replays. Invariants: all nodes converge, no lost class-A rows, ledger totals match, invoice numbers are unique per financial year.
- **Durability:** a kill-the-process / pull-the-plug test loop during billing and dispensing. Database integrity checks run at every start.
- **Migrations:** every schema migration is tested on a copy of a real anonymised pilot database.
- **Print tests:** visual regression tests of the A4, A5 and 80 mm templates.
- **Usability:** time-on-task benchmarks with real reception staff, for example "register and bill in under 60 s". Retest every release.
- **Clinical safety:** a review checklist for anything that touches dose calculation, allergy alerts or critical values.
- **Pilots:** two or three hospitals of different sizes (Solo, LAN, Connected) from Phase 1 onward.

---

## 11. Key risks and mitigations

| Risk | Mitigation |
|---|---|
| Sync bugs corrupt data | Append-only design, idempotent changes, conflict review screen, extensive simulation tests, sync ships only after the single-device version is stable |
| Staff resist change and fall back to paper | Role-based simplicity, Tally-like shortcuts, practice mode, regional-language training, rollout one module at a time (OPD first) |
| Regulatory drift (NMC, DPDP rules, GST rates) | Rules and retention kept in configuration, not code; quarterly compliance review |
| Hardware failure on a single PC | Automatic snapshots, enforced USB backups, one-click restore to a new PC |
| ABDM needs a public endpoint | The cloud relay provides it; solo sites can still do M1 (ABHA verification) when online |
| Drug master licensing | Ship a generic list; hospitals import their own brand list or supplier price lists |
| Packaging Python for Windows (antivirus false positives on PyInstaller builds, slow start) | Code-sign the installer, use one-folder (not one-file) builds, measure start time in the Phase 0 spike. Fall back to Nuitka if needed |
| `sqlcipher3` may lack ready-made Windows wheels | Spike in Phase 0: build the wheel in CI if needed. Fallbacks: OS disk encryption (BitLocker) plus encrypted backups, or field-level encryption for the most sensitive tables |
| Home-built login, sessions, CSRF and permissions (FastAPI has none built in) | Use proven libraries (Starlette sessions, argon2-cffi), keep the code small and central, write tests for every permission, get a security review before the first pilot |
| Python on Android | Tablets stay browser thin clients. A full offline Android node would be a separate app and is not planned |

---

## 12. Proposed repository layout

```
vshms/
├── pyproject.toml          # Dependencies (managed with uv), ruff, mypy, pytest config
├── alembic.ini
├── migrations/             # Alembic migration scripts
├── src/vshms/
│   ├── main.py             # FastAPI app factory: routers, middleware, SQLAdmin mount
│   ├── config.py           # Pydantic settings for desktop, hub and relay modes
│   ├── db.py               # Engine (SQLite/SQLCipher or PostgreSQL), session, sync events
│   ├── core/               # SyncBase mixin, HLC, UUIDv7, audit log, auth, permissions, PIN login
│   ├── admin/              # SQLAdmin views for master data, using the app's login
│   ├── sync/               # Outbox/inbox, push/pull API, merge rules, device pairing
│   │                       # Each domain module below has models.py, schemas.py,
│   │                       # services.py, routes.py and its own templates/
│   ├── patients/           # Registration, UHID, consent
│   ├── opd/                # Tokens, appointments, consultations
│   ├── prescriptions/
│   ├── billing/            # Tariffs, invoices, payments, GST rules, day-end closing
│   ├── pharmacy/           # Items, batches, stock ledger, H1/X/NDPS registers
│   ├── ipd/  nursing/  lab/  insurance/  registers/   # Phase 2
│   ├── fhir/               # FHIR R4 / NRCeS mappings (ABDM, NHCX)
│   ├── printing/           # Print templates (A4/A5), ESC/POS receipts, PDF
│   ├── masters/            # Seed data: ICD-10, lab tests, generic drugs, PIN codes
│   ├── templates/  static/ # Shared Jinja2 layouts and macros, HTMX/Alpine, CSS
│   └── locale/             # Babel/gettext translation files
├── desktop/                # pywebview launcher (starts Uvicorn, opens window)
├── packaging/              # PyInstaller spec, Inno Setup script, update signing
├── docs/                   # ADRs, compliance notes, user guides
└── tests/
    ├── unit/
    └── sync_sim/           # Hypothesis-based multi-device sync simulation
```

---

## 13. Open decisions

1. **Business model:** open source, freemium (Solo free, sync/cloud paid) or fully commercial? This affects licensing choices.
2. **Pilot sites:** which hospitals, and which states (state Clinical Establishments rules and languages)?
3. **UI approach:** server-rendered Jinja2 + HTMX (planned: almost all Python, light on old PCs), or a separate JavaScript front end (React) on the FastAPI JSON routes (richer offline browser behaviour, but a second language and build)? FastAPI keeps the second option open.
4. **ABDM timing:** keep it in Phase 4, or move ABHA/Scan & Share into Phase 1 for the DHIS incentive?
5. **Hosting the relay:** which Indian cloud region and provider for Tier 3 (relevant from Phase 4)?
