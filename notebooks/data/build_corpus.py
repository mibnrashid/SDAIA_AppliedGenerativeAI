#!/usr/bin/env python3
"""
build_corpus.py — generates the document set used by Notebook 2.

Run:  python notebooks/data/build_corpus.py

Produces, in this directory:
  * 15 short policy-style .txt documents — a mix of English and Arabic
  * scan_p03.png — a rendered page image with NO text layer, for the
    vision-extraction cell
  * manifest.json — the file list, so the notebook can download by name

Why generated rather than hand-written: the documents must contain
realistic identifiers (SDAIA-F-CRS-201-01-V1 and friends) placed so the
"vector search cannot find an ID" demonstration actually fails, and then
actually succeeds once BM25 is added. Keeping that in one script means
the demo can be tuned without editing fifteen files.

The generated files are committed to the repository so students download
them from raw GitHub URLs rather than from any live service.
"""

import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------
# The corpus. Identifiers are deliberate: they are meaningless to an
# embedding model and trivial for BM25, which is the whole lesson.
# --------------------------------------------------------------------

DOCS = [
    ("01_leave_policy_en.txt", """Employee Leave Policy
Reference: SDAIA-HR-LEA-014-02-V3

1. Scope
This policy applies to all permanent and fixed-term employees. It does not
apply to contractors or seconded staff, who remain subject to the terms of
their own agreements.

2. Annual leave entitlement
Annual leave is granted by grade and accrues monthly from the first day of
service.

Grade 9  - 21 working days
Grade 10 - 24 working days
Grade 11 - 30 working days
Grade 12 - 30 working days plus 5 discretionary days

3. Carry-over
Unused annual leave may be carried into the following year up to a maximum
of ten days, and must be taken before the end of March. Any balance above
ten days is forfeited unless the line manager has granted a written
exception.

4. Sick leave
Employees are entitled to thirty days of paid sick leave per calendar year.
A medical certificate is required for any absence longer than three
consecutive working days.
"""),

    ("02_training_policy_en.txt", """Training and Professional Development Policy
Reference: SDAIA-F-CRS-201-01-V1

1. Purpose
This document sets out how employees request, attend and report on funded
professional development programmes delivered through SDAIA Academy.

2. Entitlement
Employees may attend up to two funded programmes per calendar year, subject
to line manager approval and departmental budget availability.

3. How to request a place
Requests must be submitted on form SDAIA-F-CRS-201-01-V1 no later than two
weeks before the programme start date. Late requests are not processed; the
employee is placed on the waiting list for the next cohort.

4. After the programme
Attendees submit a one-page summary within ten working days of completion.
Programmes longer than three days additionally require a short presentation
to the team.

5. Superseded documents
This version supersedes SDAIA-F-CRS-201-01-V0 and all earlier editions.
"""),

    ("03_data_governance_en.txt", """National Data Governance - Internal Implementation Note
Reference: SDAIA-DG-POL-007-01-V2

1. Classification
All datasets are classified as Public, Internal, Confidential or Restricted
before they are stored. Classification is recorded in the data catalogue and
reviewed annually.

2. Ownership
Every dataset has a named data owner. Where ownership is unclear, the
default owner is the head of the originating department.

3. Sharing
Personal data may not be shared with any external party without written
consent and a completed data sharing agreement.

4. Retention
Datasets are retained only for as long as the stated purpose requires.
Retention schedules are reviewed under reference SDAIA-DG-RET-011-03-V1.
"""),

    ("04_security_policy_en.txt", """Information Security Policy - Summary for Staff
Reference: SDAIA-SEC-POL-002-04-V5

1. Access
Access follows least privilege. Accounts are reviewed quarterly and removed
within one working day of an employee leaving.

2. Devices
Authority data may only be processed on managed devices. Personal cloud
storage is not permitted for any Internal, Confidential or Restricted data.

3. Incidents
Any suspected breach is reported to the data protection officer within
twenty-four hours of discovery. The officer maintains the breach register.

4. Passwords and multi-factor authentication
Multi-factor authentication is mandatory on all systems that hold personal
data. Shared accounts are prohibited without a documented exception.
"""),

    ("05_procurement_en.txt", """Procurement Thresholds - Quick Reference
Reference: SDAIA-FIN-PRC-030-02-V2

Purchases below 5,000 SAR may be approved by the line manager.
Purchases between 5,000 and 50,000 SAR require departmental head approval
and two written quotations.
Purchases above 50,000 SAR require a competitive process managed by the
procurement office.

Cloud services and AI services of any value require an additional security
review under SDAIA-SEC-POL-002-04-V5 before a contract is signed.
"""),

    ("06_remote_work_en.txt", """Remote Working Guidelines
Reference: SDAIA-HR-RMT-022-01-V1

Employees may work remotely up to two days per week with line manager
agreement. Remote days are recorded in the HR system in advance.

Meetings involving Restricted data are held on site unless an exception is
approved. Remote working does not change the leave entitlements set out in
SDAIA-HR-LEA-014-02-V3.
"""),

    ("07_ai_ethics_en.txt", """Responsible AI - Internal Principles
Reference: SDAIA-AI-ETH-001-01-V1

1. Transparency
Users must be told when they are interacting with an AI system, and given a
route to a human.

2. Accountability
Every deployed AI system has a named owner who is accountable for its
behaviour. "The model decided" is not an acceptable explanation.

3. Fairness
Systems are tested for differential performance across languages. A service
that answers well in English and poorly in Arabic is not fit for purpose.

4. Human oversight
Irreversible actions require human approval before execution.
"""),

    ("08_records_en.txt", """Records Management Standard
Reference: SDAIA-DG-REC-018-02-V1

Official records are stored in the approved document management system. A
record is any document that evidences a decision, an obligation or a
transaction.

Email is not a record store. Decisions taken by email must be transferred to
the document management system within five working days.

Disposal follows the retention schedule and requires sign-off from the
records officer.
"""),

    # ---- Arabic documents -----------------------------------------
    ("09_leave_policy_ar.txt", """سياسة الإجازات
المرجع: SDAIA-HR-LEA-014-02-V3

يجب على الموظف تقديم طلب الإجازة قبل أسبوعين على الأقل.

تُمنح الإجازة السنوية حسب المرتبة الوظيفية:
المرتبة ٩ - ٢١ يوم عمل
المرتبة ١٠ - ٢٤ يوم عمل
المرتبة ١١ - ٣٠ يوم عمل

يجوز ترحيل عشرة أيام كحد أقصى إلى السنة التالية.
"""),

    ("10_data_protection_ar.txt", """حماية البيانات الشخصية
المرجع: SDAIA-DG-POL-007-01-V2

لا يجوز مشاركة البيانات الشخصية مع أي جهة خارجية دون موافقة مكتوبة.

يجب الإبلاغ عن أي اشتباه في تسريب البيانات خلال أربع وعشرين ساعة.

تطبق هذه السياسة على جميع الإدارات دون استثناء.
"""),

    ("11_training_ar.txt", """سياسة التدريب والتطوير
المرجع: SDAIA-F-CRS-201-01-V1

يحق للموظف حضور برنامجين ممولين في السنة الواحدة.

تُقدم الطلبات عبر النموذج SDAIA-F-CRS-201-01-V1 قبل أسبوعين من بداية البرنامج.

لن يتم قبول الطلبات المتأخرة.
"""),

    ("12_security_ar.txt", """أمن المعلومات - ملخص للموظفين
المرجع: SDAIA-SEC-POL-002-04-V5

يُمنع استخدام التخزين السحابي الشخصي لبيانات الهيئة.

التحقق متعدد العوامل إلزامي على جميع الأنظمة التي تحتوي على بيانات شخصية.
"""),

    ("13_conduct_en.txt", """Code of Conduct - Extract
Reference: SDAIA-HR-COC-005-01-V2

Employees act with integrity and avoid any situation where a personal
interest could conflict with the interests of the Authority.

Gifts above nominal value are declined and declared. Hospitality is
declared where it could reasonably be seen to influence a decision.

Breaches of this code are handled under the disciplinary procedure and may
be reported anonymously.
"""),

    ("14_it_support_en.txt", """IT Support - Service Levels
Reference: SDAIA-IT-SVC-041-01-V3

Priority 1 (service down for a department): response within 30 minutes.
Priority 2 (individual blocked from working): response within 4 hours.
Priority 3 (degraded but working): response within 2 working days.
Priority 4 (request or question): response within 5 working days.

Requests for new software require a security review under
SDAIA-SEC-POL-002-04-V5.
"""),

    ("15_meeting_rooms_en.txt", """Meeting Room Booking Rules
Reference: SDAIA-ADM-MTG-009-01-V1

Rooms are booked through the calendar system. Bookings not confirmed within
ten minutes of the start time are released automatically.

The board room requires approval from the office of the director. Rooms
holding sessions with Restricted material must have the door closed and
screens angled away from external windows.
"""),
]

# The page rendered as an image. Note it is NOT in DOCS: the whole point
# is that this content exists only as pixels, so the vision model is the
# only way into the pipeline.
SCAN_PAGE_LINES = [
    "SDAIA - Internal Circular",
    "Reference: SDAIA-CIR-2024-118-01-V1",
    "",
    "Subject: Updated overtime approval process",
    "",
    "1. All overtime must be approved in advance by the line",
    "   manager and recorded in the HR system on the same day.",
    "",
    "2. Overtime above 20 hours in a single month additionally",
    "   requires departmental head approval.",
    "",
    "3. Overtime is compensated at 1.5x the hourly rate, or as",
    "   time off in lieu at the employee's choice.",
    "",
    "4. This circular supersedes SDAIA-CIR-2023-091-02-V2 and",
    "   takes effect from the first of the month.",
    "",
    "Approved by: Director of Human Resources",
    "Page 3 of 4",
]


def write_documents():
    written = []
    for name, text in DOCS:
        path = os.path.join(HERE, name)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        written.append(name)
        print("wrote", name)
    return written


def write_scan():
    """Render a page image with no text layer.

    Uses Pillow, which is present in Colab and in most Python installs.
    If Pillow is missing we skip rather than fail — the rest of the
    corpus is still usable, and the notebook says so.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed - skipping scan_p03.png")
        return None

    W, H = 1240, 1754                     # A4 at 150 dpi
    img = Image.new("RGB", (W, H), (247, 245, 240))   # slightly off-white
    draw = ImageDraw.Draw(img)

    font = None
    for candidate in ("DejaVuSans.ttf", "arial.ttf", "Arial.ttf"):
        try:
            font = ImageFont.truetype(candidate, 30)
            break
        except (OSError, IOError):
            continue
    if font is None:
        font = ImageFont.load_default()

    y = 150
    for line in SCAN_PAGE_LINES:
        draw.text((110, y), line, fill=(28, 28, 32), font=font)
        y += 52

    # A faint border and a slight grey wash, so it reads as a scan
    # rather than as a clean render.
    draw.rectangle([40, 40, W - 40, H - 40], outline=(200, 196, 188), width=2)
    for x in range(0, W, 7):                     # very light scan banding
        draw.line([(x, 0), (x, H)], fill=(244, 242, 237), width=1)

    path = os.path.join(HERE, "scan_p03.png")
    img.save(path, "PNG")
    print("wrote scan_p03.png")
    return "scan_p03.png"


def main():
    names = write_documents()
    scan = write_scan()

    manifest = {
        "description": "Document set for Notebook 2 (day2_retrieval.ipynb).",
        "text_files": names,
        "scan_image": scan,
        "identifiers_present": [
            "SDAIA-F-CRS-201-01-V1",
            "SDAIA-HR-LEA-014-02-V3",
            "SDAIA-SEC-POL-002-04-V5",
            "SDAIA-DG-POL-007-01-V2",
            "SDAIA-CIR-2024-118-01-V1",
        ],
        "note": (
            "SDAIA-CIR-2024-118-01-V1 appears ONLY inside scan_p03.png. "
            "Until the vision extraction cell runs, no text search of any "
            "kind can find it - which is the point of that cell."
        ),
    }
    with io.open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(manifest, indent=2, ensure_ascii=False))
    print("wrote manifest.json")
    print("\n%d text documents + %s" % (len(names), scan or "no image"))


if __name__ == "__main__":
    main()
