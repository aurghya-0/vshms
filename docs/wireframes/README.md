# Screen wireframes

Low-fidelity wireframes for the main VSHMS screens: desktop at 1366×768, greys plus one blue for primary actions. They settle **layout and flow** only. Colours, type and final spacing come later.

**Live canvas (pan, zoom, click through):** https://claude.ai/artifact/DdGTU8RQNwQ7bo5YtZeQb9. It is private, so ask the project owner to share it with you.

## Screens

| File | Screen | Covers |
|---|---|---|
| `Login.dc.html` | Login and PIN switch | User tiles, 4-digit PIN for shared PCs, password fallback, mode and backup status |
| `Main.dc.html` | Reception home | Search by mobile/name/UHID (shows everyone sharing a mobile), new registration, OPD queue, day summary, backup reminder |
| `Registration.dc.html` | Patient registration | DOB or approximate age, S/o/D/o/W/o, PIN code → district/state, category, ABHA (online only), no Aadhaar, consent, duplicate warning |
| `Consultation.dc.html` | Doctor consultation | Queue, patient banner with allergy and triage vitals, ICD-10 diagnosis, prescription with dose shorthand and bilingual instructions, A5 print preview |
| `Billing.dc.html` | OPD billing | Payer and tariff, service lines, UPI QR made offline, per-device invoice number, GST exemption note, thermal receipt, void and re-issue |
| `Pharmacy.dc.html` | Pharmacy dispensing | Prescriptions waiting, barcode scan, earliest-expiry batch picking, Schedule H1 register note, stock alerts |
| `BedBoard.dc.html` | IPD bed board | Beds by ward (status shown by border style, not colour alone), selected bed's bill and deposit, quick actions, an offline sync conflict |

`canvas.json` holds the canvas layout (frame positions and titles).

## Conventions shown in every screen

- One top bar: role, current user, device mode and sync status, language switch, lock.
- A keyboard shortcut strip at the bottom (F2 new patient, F3 search, F5 bill, Esc back).
- Touch targets at least 44 px; real buttons, inputs and labels.

## Data in the wireframes

Patient and staff names are invented. Values in brackets, such as `[42]` or `₹[950.00]`, are placeholders, not real rates or statistics. Drug brands and the doctor's registration number are placeholders too.

## Using these files

The `.dc.html` files are the canvas's source format. They load a runtime script (`support.js`) from the canvas, so opening them directly in a browser shows unstyled template text. To view them, use the live canvas. To build the real screens, use them as a reference for the Jinja2 + HTMX templates (tasks B1 and B6, C6 and A7's UI in [docs/TASKS.md](../TASKS.md)), not as code to copy.

To bring them into Figma later: use the canvas's **Share › Export** menu if it offers Figma, or export the screens as standalone HTML and import them with a plugin such as html.to.design.
