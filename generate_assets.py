
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

BASE_DIR = Path(__file__).resolve().parent
DOCS = BASE_DIR / "documents"
BACKUPS = BASE_DIR / "backups"

DOCS.mkdir(exist_ok=True)
BACKUPS.mkdir(exist_ok=True)


def write_text(filename, content):
    (DOCS / filename).write_text(content, encoding="utf-8")


def generate_audit_pdf():
    output = DOCS / "audit_report.pdf"
    styles = getSampleStyleSheet()

    story = [
        Paragraph("HOSPITAL INTERNAL SYSTEMS", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Internal Audit Report", styles["Heading1"]),
        Paragraph("Classification: CONFIDENTIAL", styles["Heading2"]),
        Spacer(1, 14),
        Paragraph(
            "This report is intended for authorized hospital "
            "administration personnel only.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("Backup Storage Notice", styles["Heading2"]),
        Paragraph(
            "Following the October maintenance window, the internal "
            "database backup was relocated to the following storage "
            "location:",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        Paragraph(
            "<b>/backups/october_backup.zip</b>",
            styles["Code"],
        ),
        Spacer(1, 12),
        Paragraph(
            "Access to this archive should be restricted to authorized "
            "infrastructure personnel.",
            styles["BodyText"],
        ),
    ]

    SimpleDocTemplate(
        str(output),
        pagesize=letter,
        title="Internal Audit Report",
        author="Hospital Internal Systems",
    ).build(story)

    print(f"Created actual PDF: {output}")


def generate_backup():
    flag_path = BACKUPS / "flag.txt"
    flag_path.write_text(
        "CTF{second_order_idor_backup_discovery}\n",
        encoding="utf-8",
    )

    zip_path = BACKUPS / "october_backup.zip"

    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        archive.write(flag_path, arcname="flag.txt")

    print(f"Created actual ZIP: {zip_path}")


if __name__ == "__main__":
    write_text(
        "research_notes.txt",
        "Research Notes\n"
        "Department: Cardiology\n"
        "Status: Internal review\n"
        "This file contains sample training data.\n",
    )

    write_text(
        "patient_summary.txt",
        "Patient Summary\n"
        "This document contains synthetic training information.\n",
    )

    write_text(
        "monthly_review.txt",
        "October Migration Note\n\n"
        "The Internal Audit Report was migrated to document reference 91.\n"
        "Its report contains the location of the October backup archive.\n",
    )

    

    generate_audit_pdf()
    generate_backup()
