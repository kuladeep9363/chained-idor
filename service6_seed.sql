PRAGMA foreign_keys = ON;

--------------------------------------------------
-- Tables
--------------------------------------------------

CREATE TABLE IF NOT EXISTS patients (
    uuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    doctor_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shares (
    share_id INTEGER PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    expiry TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES documents(id)
);

--------------------------------------------------
-- Doctors
--------------------------------------------------

INSERT OR IGNORE INTO doctors
(id, name, department, designation)
VALUES
(17, 'Dr. Maya Bennett', 'Cardiology', 'Senior Consultant'),
(18, 'Dr. Ethan Brooks', 'Neurology', 'Consultant'),
(19, 'Dr. Olivia Chen', 'Internal Medicine', 'Department Head');

--------------------------------------------------
-- Patients
--------------------------------------------------

INSERT OR IGNORE INTO patients
(uuid, name, age, blood_group, doctor_id)
VALUES
('3fd31f31-9cb7-4a12-8d81-111111111111',
 'John Carter', 54, 'O+', 17),

('6a4e2b10-7d2c-4f81-a239-222222222222',
 'Emily Stone', 37, 'A-', 18),

('8c6f4d22-1a93-4c11-b782-333333333333',
 'Robert Miles', 62, 'B+', 17),

('2b9d7e44-5f18-4a61-9c03-444444444444',
 'Sarah Wilson', 45, 'AB+', 19);

--------------------------------------------------
-- Documents
--------------------------------------------------

INSERT OR IGNORE INTO documents
(id, owner_id, filename, title, file_path)
VALUES
(51, 17,
 'research_notes.txt',
 'Research Notes',
 'documents/research_notes.txt'),

(52, 17,
 'patient_summary.txt',
 'Patient Summary',
 'documents/patient_summary.txt'),

(53, 18,
 'monthly_review.txt',
 'Monthly Review',
 'documents/monthly_review.txt'),

(91, 19,
 'audit_report.pdf',
 'Internal Audit Report',
 'documents/audit_report.pdf');

--------------------------------------------------
-- Shares
--------------------------------------------------

INSERT OR IGNORE INTO shares
(share_id, owner_id, document_id, expiry)
VALUES
(908, 17, 51, '2026-12-31'),
(909, 17, 52, '2026-12-31'),
(910, 18, 53, '2026-12-31');
