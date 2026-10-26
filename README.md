Meridian Hospital Internal Portal --- Setup Guide
This guide explains how to run the intentionally vulnerable Flask CTF
application on another computer.
> **Lab safety:** This application intentionally contains insecure
> access-control behavior for cybersecurity training. Run it only on a
> machine or network you control. Keep it bound to localhost unless you
> deliberately configure an isolated training environment.
1. Requirements
Python 3.10 or newer recommended
`pip`
Git, if cloning the project from a repository
Check your installation:
``` bash
python --version
python -m pip --version
git --version
```
On some Linux systems, use `python3` instead of `python`.
2. Get the project files
Option A --- Clone the repository
Replace the example URL with the actual repository URL:
``` bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>
```
Option B --- Copy the project folder
Copy the entire project directory to the target computer. Preserve the
relative paths of the Python files, templates, static assets, documents,
and backups.
The project should have a structure similar to:
``` text
hospital/
├── app.py
├── database.py
├── generate_assets.py
├── requirements.txt
├── hospital.db                 # created by database initialization(database.py)
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── patient.html
│   ├── doctor.html
│   └── 404.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── portal.js
├── documents/                   # created by generate_assets.py
│   ├── research_notes.txt
│   ├── patient_summary.txt
│   ├── monthly_review.txt
│   └── audit_report.pdf
└── backups/
    ├── flag.txt
    └── october_backup.zip
```
Some generated files may not exist until you run `generate_assets.py`.
Keep any additional files that are present in your actual project.
3. Create and activate a virtual environment
Run these commands from the project root.
Linux / Kali
``` bash
python3 -m venv .venv
source .venv/bin/activate
```
If creating the environment fails because the venv package is missing,
install your distribution's Python venv package, then retry.
Windows PowerShell
``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, you can use Command Prompt instead:
``` bat
.venv\Scripts\activate.bat
```
4. Install dependencies
With the virtual environment activated:
``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If `requirements.txt` is missing, obtain it from the project source
rather than guessing the dependency versions. Flask is the core web
dependency; PDF generation may require an additional package depending
on the implementation of `generate_assets.py`.
5. Generate the challenge assets and database
From the project root, run:
``` bash
python generate_assets.py
python database.py
```
These scripts should create the challenge documents/archive and
initialize `hospital.db` with the seeded records. Run them from the
project root so the relative asset paths match the expected layout.
The seeded challenge records include:
Doctors with IDs `17`, `18`, and `19`
Patients linked to those doctors
Documents `51`, `52`, `53`, and `91`
Shares `908`, `909`, and `910`
Important: existing database files
The database uses `INSERT OR IGNORE` for seed rows. Re-running
`database.py` will not overwrite rows that already exist.
For a fresh training setup, stop the app and back up or remove the
existing `hospital.db` before initializing it again. Deleting the
database resets all local challenge data, so do this only when you do
not need to preserve it.
If you need to preserve existing data, use a targeted SQL update instead
of deleting the database.
6. Start the application
Keep the virtual environment activated and run:
``` bash
python app.py
```
Open this address in a browser on the same computer:
``` text
http://127.0.0.1:5000/
```
The application is intended to run on `127.0.0.1:5000`. Do not change it
to a public network interface unless you have deliberately isolated the
challenge and understand the risks.
To stop the server, press `Ctrl+C` in the terminal running Flask.
7. Challenge flow
The app is designed as a chained web-security exercise. Depending on the
version of the project, the intended discovery path is:
Explore the dashboard and patient records.
Inspect doctor records and the available document shares.
Read the monthly review document for the migration clue identifying
document reference `91`.
Inspect how the share-expiry update request works.
Observe that the intentionally vulnerable share-update behavior may
allow a document reference to be changed.
Open the affected share to access the internal audit report.
Read the report to discover the backup archive location.
Retrieve the archive in the local lab and inspect its sample flag.
Use only the seeded records and the local lab instance. The intended
exploit behavior is deliberately insecure and should not be copied into
a production application.
8. Share reset behavior
The current training version may reset the three seeded share records
when the backup route is requested. The intended baseline mapping is:
    Share ID   Baseline document ID
---
       `908`                   `51`
       `909`                   `52`
       `910`                   `53`

If this reset logic is enabled in `app.py`, it uses the project's
`get_db()` helper from `database.py`. The database table's key column is
named `share_id`, not `id`.
The reset is global to the local SQLite database. It does not isolate
concurrent participants; use separate challenge instances or per-team
databases for a multi-player deployment.
9. Troubleshooting
`ModuleNotFoundError: No module named 'flask'` (or another dependency)
Activate the virtual environment and run:
``` bash
python -m pip install -r requirements.txt
```
`NameError: name 'get_db' is not defined`
Make sure `app.py` imports the helper from `database.py`. For example:
``` python
from database import get_db
```
If `app.py` already imports other functions from `database.py`, add
`get_db` to that existing import.
`NameError: name 'sqlite3' is not defined`
If the route calls `sqlite3` directly, `app.py` must import it:
``` python
import sqlite3
```
If you use the existing `get_db()` helper instead, you do not need to
call `sqlite3` directly in `app.py`.
A document or ZIP returns `404`
Check that:
`generate_assets.py` completed successfully.
You started commands from the project root.
The expected file exists under `documents/` or `backups/`.
The paths used by the application match the actual filenames.
A renamed document still displays its old name
The seed script uses `INSERT OR IGNORE`, so it does not update an
existing document row. Update the relevant row in SQLite or recreate the
local database if it is safe to reset the data.
Port `5000` is already in use
Stop the other local process using the port or change the Flask port
consistently in your local development configuration.
10. Before sharing the project
Include `requirements.txt`, all templates/static assets, and the
asset-generation script.
Ensure generated assets can be recreated on a clean machine.
Do not commit `.venv/`, Python cache directories, or personal
secrets.
Do not include real patient information, credentials, or production
data.
Explain clearly that the application is intentionally vulnerable.
Keep the service private or isolated during training.
