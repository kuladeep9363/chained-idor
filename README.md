ByteForge Technologies --- Employee Portal CTF
A beginner-friendly Web Exploitation challenge demonstrating
client-side trust and Base64 cookie tampering. The application uses
Flask and runs directly on port `5000`; Nginx is not required.
> \*\*Training use only:\*\* This application is intentionally vulnerable.
> Run it only on localhost or an isolated CTF network. Do not expose it
> to the public internet.
1. Challenge overview
When a visitor opens the portal, the app automatically issues an
employee cookie. There is no login form and no username/password to
change.
The cookie contains a Base64-encoded role:
``` text
auth=cm9sZT11c2VyCg==
```
Decoded value:
``` text
role=user
```
Participants can change the role to `admin`, Base64-encode it, and
replace the cookie:
``` text
auth=cm9sZT1hZG1pbgo=
```
The modified cookie should reveal the Administrator Dashboard and the
challenge flag:
``` text
FLAG{client\_side\_trust\_is\_dangerous}
```
Base64 is encoding, not encryption or a signature. The vulnerability is
that the server trusts a role supplied by the browser.
Challenge objectives
Find the HTTP service and identify ByteForge Technologies in the
response headers.
Inspect and decode the `auth` cookie.
Modify the role from `user` to `admin`.
Access the administrator dashboard and profile.
Confirm that malformed cookies never grant administrator access.
2. Application features
ByteForge Technologies branding
Employee home page
Employee dashboard
Employee profile
Company announcements
HR documents page
Administrator dashboard with flag
Administrator-specific profile information
Automatic employee cookie; no login portal
HTTP identification headers for Nmap service reconnaissance
3. Project structure
Create or obtain the project with the following layout:
``` text
employee-portal/
├── app.py
├── requirements.txt
├── Dockerfile
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── announcements.html
│   ├── documents.html
│   └── error.html
└── static/
    └── styles.css
```
The files listed above are the application source files. A README alone
does not contain the app's implementation, so make sure these files are
included when sharing the project with another person.
4. Requirements
Choose either a native Python installation or Docker.
Option A --- Python
Python 3.10 or later (Python 3.12 is a good choice)
`pip`
A terminal
Option B --- Docker
Docker Engine or Docker Desktop
No database, Nginx, or external service is required.
5. Run locally with Python
Linux / Kali Linux / macOS
Open a terminal in the `employee-portal` directory:
``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```
Windows PowerShell
Open PowerShell in the `employee-portal` directory:
``` powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```
If PowerShell blocks virtual-environment activation, open Command Prompt
and use:
``` bat
py -m venv .venv
.venv\\Scripts\\activate.bat
python -m pip install -r requirements.txt
python app.py
```
Open the portal
On the same computer, visit:
``` text
http://127.0.0.1:5000
```
To access it from another machine on the same isolated lab network, use
the host computer's reachable IP address:
``` text
http://<HOST\_IP>:5000
```
The Flask application listens on `0.0.0.0:5000` to permit network
access. Allow port `5000` through the firewall only when required for
the isolated lab.
6. Run with Docker
Build the image from the directory containing the Dockerfile:
``` bash
docker build -t byteforge-employee-portal .
```
Run the container:
``` bash
docker run --rm --name byteforge-portal -p 5000:5000 byteforge-employee-portal
```
Open `http://127.0.0.1:5000`.
Stop the container with `Ctrl+C`. The `--rm` option removes the stopped
container; the image remains available.
7. Verify the cookie vulnerability
Open the portal in a browser.
Open Developer Tools (`F12`) and find the site's cookies under
Application/Storage → Cookies.
Locate the `auth` cookie. The initial value should be:
    `text cm9sZT11c2VyCg==`
Decode it with a local Base64 decoder or a terminal:
    `bash printf 'cm9sZT11c2VyCg==' | base64 -d`
Expected output: `role=user` followed by a newline.
Replace the cookie value with:
    `text cm9sZT1hZG1pbgo=`
Navigate to `/dashboard` or refresh the dashboard. The Administrator
Dashboard and flag should appear.
Open `/profile`. The profile should now show the HR Administrator
role, Human Resources department, and administrative access level.
Test with curl
Run these commands on the computer hosting the app, or replace
`127.0.0.1` with the appropriate host address.
Employee cookie:
``` bash
curl -i --cookie 'auth=cm9sZT11c2VyCg==' \\
  http://127.0.0.1:5000/dashboard
```
Expected: Employee Dashboard.
Modified administrator cookie:
``` bash
curl -i --cookie 'auth=cm9sZT1hZG1pbgo=' \\
  http://127.0.0.1:5000/dashboard
```
Expected: Administrator Dashboard and
`FLAG{client\_side\_trust\_is\_dangerous}`.
Malformed cookie:
``` bash
curl -i --cookie 'auth=YWJjMTIz' \\
  http://127.0.0.1:5000/dashboard
```
Expected: HTTP `401` with an authentication error. It must not reveal
the flag.
8. Secondary objective --- Nmap
From a different machine on the same lab network, scan the host running
the application:
``` bash
nmap -sV -p 5000 --script http-title,http-headers <HOST\_IP>
```
The application adds these HTTP response headers:
``` http
Server: ByteForge Technologies Employee Portal
X-Company: ByteForge Technologies
```
The HTTP title should also identify the Employee Portal. Nmap's exact
service/product label varies with its version and probe results; the
`http-headers` script is the most direct way to verify the custom
company header.
If the scan fails:
Confirm the Flask app is running.
Check that port `5000` is reachable from the scanning machine.
Check the host firewall and container port mapping.
Ensure both machines are on a network where they are permitted to
communicate.
9. Expected behavior checklist
---
Request / state                     Expected behavior
---
First visit to `/` without a cookie Portal loads and issues an employee
cookie
Valid `role=user` cookie            Employee pages and Employee
Dashboard
Valid `role=admin` cookie           Administrator Dashboard and flag
`role=admin` cookie on `/profile`   HR Administrator profile and
administrative access details
Malformed or random cookie on a     Authentication error; no elevated
protected route                     access
Nmap HTTP header scan               `ByteForge Technologies` appears in
the response headers
10. Troubleshooting
`ModuleNotFoundError: No module named 'flask'`
Activate the virtual environment and run:
``` bash
python -m pip install -r requirements.txt
```
Port 5000 is already in use
Stop the other process using port `5000`, or change the port in the
`app.run(...)` line and update the browser URL, curl commands, Docker
mapping, and Nmap command accordingly.
The cookie does not change to admin
Confirm the entire cookie value was replaced, without extra spaces
or quotes.
Refresh `/dashboard` after changing the cookie.
Make sure you are editing the cookie for the correct host and port.
Confirm the value is exactly `cm9sZT1hZG1pbgo=`.
The admin profile is not changing
Check that the `/profile` route calls `get\_role()` and passes the
role-dependent template values (`role`, `employee\_id`, `department`, and
`access\_level`). Check that `templates/profile.html` renders those
variables.
A malformed cookie reveals the flag
The role parser must accept only the exact recognized values
`role=user\\\\n` and `role=admin\\\\n`. Unknown, malformed, or undecodable
values must return no role and must never default to `admin`.
11. Important implementation notes
The cookie is deliberately unsigned and client-controlled. This is
the intended challenge vulnerability.
`HttpOnly` prevents ordinary page JavaScript from reading the
cookie; it does not prevent the user from modifying it through
browser developer tools or an intercepting proxy.
The invalid-cookie check is a required challenge behavior. Invalid
values must not receive administrator privileges.
This is a deliberately vulnerable lab, not a production
authentication design. A real application should derive
authorization from trusted server-side state or use a properly
validated, signed session mechanism.
Keep the challenge on an isolated CTF network and do not reuse real
credentials or secrets.
12. Quick start summary
``` bash
# From the project directory
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000` and begin testing the `auth` cookie.
