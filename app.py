
from pathlib import Path

from flask import (
    Flask, render_template, request, jsonify,
    send_file, session, redirect, url_for, abort
)


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hospital.db"
# DB_PATH = Path("/var/lib/hackshield/service6/hospital.db")
FLAG_PATH = Path("/opt/flag/flag6")

# from database import get_db, init_db

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

app = Flask(__name__)
app.secret_key = "local-ctf-development-key-change-before-use"


@app.before_request
def demo_session():
    # This challenge starts with a pre-authenticated receptionist.
    if "user_id" not in session:
        session["user_id"] = "receptionist-01"
        session["role"] = "receptionist"
        session["display_name"] = "Alex Morgan"


@app.get("/")
def index():
    return redirect(url_for("dashboard"))


@app.get("/dashboard")
def dashboard():
    conn = get_db()
    patients = conn.execute(
        "SELECT * FROM patients ORDER BY name"
    ).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients,
        active="dashboard",
    )


@app.get("/patient/<patient_uuid>")
def patient_profile(patient_uuid):
    conn = get_db()

    # INTENTIONAL FLAW:
    # The endpoint checks existence but not patient assignment
    # or whether this receptionist may view this record.
    patient = conn.execute(
        "SELECT * FROM patients WHERE uuid = ?",
        (patient_uuid,),
    ).fetchone()

    if patient is None:
        conn.close()
        abort(404)

    doctor = conn.execute(
        "SELECT * FROM doctors WHERE id = ?",
        (patient["doctor_id"],),
    ).fetchone()

    conn.close()

    return render_template(
        "patient.html",
        patient=patient,
        doctor=doctor,
        active="patients",
    )


@app.get("/doctor/<int:doctor_id>")
def doctor_profile(doctor_id):
    conn = get_db()

    # INTENTIONAL FLAW:
    # No role or doctor-record authorization check.
    doctor = conn.execute(
        "SELECT * FROM doctors WHERE id = ?",
        (doctor_id,),
    ).fetchone()

    if doctor is None:
        conn.close()
        abort(404)

    documents = conn.execute("""
        SELECT
            shares.share_id,
            shares.expiry,
            documents.title,
            documents.filename
        FROM shares
        JOIN documents
          ON documents.id = shares.document_id
        WHERE shares.owner_id = ?
        ORDER BY shares.share_id
    """, (doctor_id,)).fetchall()

    conn.close()

    return render_template(
        "doctor.html",
        doctor=doctor,
        documents=documents,
        active="doctors",
    )


@app.patch("/share/<int:share_id>")
def update_share(share_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    conn = get_db()

    share = conn.execute(
        "SELECT * FROM shares WHERE share_id = ?",
        (share_id,),
    ).fetchone()

    if share is None:
        conn.close()
        abort(404)

    # INTENTIONAL FLAWS:
    # 1. No authorization check for modifying this share.
    # 2. Client-controlled document_id is accepted.
    # 3. No validation that the target document belongs
    #    to the share owner.
    allowed_updates = {"expiry", "document_id"}
    updates = {
        key: value
        for key, value in data.items()
        if key in allowed_updates
    }

    if not updates:
        conn.close()
        return jsonify(error="No supported fields supplied"), 400

    # Parameterized SQL avoids introducing SQL injection.
    # The vulnerability here is authorization, not SQL syntax.
    assignments = ", ".join(
        f"{column} = ?" for column in updates
    )
    values = list(updates.values()) + [share_id]

    try:
        conn.execute(
            f"UPDATE shares SET {assignments} WHERE share_id = ?",
            values,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        return jsonify(error="Update failed"), 400

    conn.close()

    return jsonify(
        message="Share settings updated",
        share_id=share_id,
    )


@app.get("/share/<int:share_id>")
def get_shared_document(share_id):
    conn = get_db()

    # INTENTIONAL FLAW:
    # The share is resolved using its stored document_id,
    # without checking whether this user may access the document.
    row = conn.execute("""
        SELECT documents.file_path, documents.filename,
               documents.title
        FROM shares
        JOIN documents
          ON documents.id = shares.document_id
        WHERE shares.share_id = ?
    """, (share_id,)).fetchone()

    conn.close()

    if row is None:
        abort(404)

    path = (BASE_DIR / row["file_path"]).resolve()

    # Keep file serving within the documents directory.
    # This path check prevents arbitrary filesystem traversal;
    # it does not fix the intended document-authorization flaw.
    docs_root = (BASE_DIR / "documents").resolve()

    if not path.is_relative_to(docs_root) or not path.is_file():
        abort(404)

    if path.suffix.lower() == ".pdf":
        return send_file(
            path,
            mimetype="application/pdf",
            as_attachment=False,
            download_name=row["filename"],
        )

    return send_file(
        path,
        mimetype="text/plain",
        as_attachment=True,
        download_name=row["filename"],
    )

#lalala

@app.get("/backups/october_backup.zip")
def download_backup():
    # INTENTIONAL FLAW:
    # No authentication or authorization requirement for this backup.
    path = BASE_DIR / "backups" / "october_backup.zip"

    if not path.is_file():
        abort(404)

    response = send_file(
        path,
        mimetype="application/zip",
        as_attachment=True,
        download_name="october_backup.zip",
    )

    # Reset the vulnerable share after preparing the download response.
    conn = get_db()
    try:
        conn.executemany("""
        UPDATE shares
        SET document_id = ?
        WHERE share_id = ?
    """, [
        (51, 908),
        (52, 909),
        (53, 910),
    ])
        conn.commit()
    finally:
        conn.close()

    return response


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", active=""), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
