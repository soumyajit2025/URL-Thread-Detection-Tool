URL Threat Complete - Noob-friendly Quick Start (Windows - PowerShell)

What this is:
- A simple Flask web app that scans a URL with rule-based checks and stores results in a local SQLite DB.
- UI available at http://127.0.0.1:5000

Steps to run (step-by-step, assume fresh Windows machine):

1) Download and extract the ZIP into a folder, e.g.:
   C:\Users\<yourname>\Desktop\url-threat-complete-noob

2) Open Visual Studio Code (VS Code). From VS Code menu: File -> Open Folder -> select the extracted folder.

3) Open the VS Code integrated terminal:
   - Menu: View -> Terminal
   - You'll see a terminal at the bottom. It usually starts at the project folder path.

4) Create a Python virtual environment (type each line and press Enter):
   python -m venv venv

5) Activate the virtual environment (PowerShell):
   .\venv\Scripts\Activate

   If the prompt changes to start with (venv), you're activated.

6) Install Python dependencies:
   pip install -r requirements.txt

7) Run the app:
   python app.py

8) Open a browser and visit:
   http://127.0.0.1:5000

9) Enter a URL in the form and click Scan. Results will show on the page. History is saved in database.db file.

Troubleshooting tips:
- If you get "can't open file 'app.py'", make sure your terminal's current folder shows the project root and that app.py exists there.
  In PowerShell: run `dir` to list files. If app.py is not listed, check that you opened the right folder.
- If Python isn't found, install Python 3.10+ from python.org and restart VS Code.

Enjoy and be careful — do not scan real malicious payloads on your host machine.
