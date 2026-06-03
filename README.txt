First-Time Setup Summary

git clone https://github.com/AdamFinkler/communications-LTD-CTF.git
cd communications-LTD-CTF
cd backend
python -m venv venv

PowerShell:

.\venv\Scripts\Activate.ps1

Git Bash:

source venv/Scripts/activate

Install dependencies:

pip install -r requirements.txt

Run the server:

python -m uvicorn main:app --reload   /  python main.py

Open the app in the browser:

http://127.0.0.1:8000/

From the home page use "Log In" or "Join us now". Forgot-password demo codes
are printed in the backend terminal.

------------------------------------------

Delete a customer row (when Delete button fails)

File location:
  backend\delete_customer.py
  backend\delete_customer.bat   (double-click on Windows)

PowerShell (from backend folder):

  python delete_customer.py              show all customers + IDs
  python delete_customer.py 175          delete customer ID 175
  python delete_customer.py --reset      restore 6 default customers

Or double-click delete_customer.bat then run in the window:
  python delete_customer.py
  python delete_customer.py 175

------------------------------------------

SQL Injection demo guide (Hebrew):

  Open in browser (recommended): docs/SQLi_Demo_Guide.html
  PDF: docs/SQLi_Demo_Guide_Communication_LTD.pdf

  Regenerate PDF: backend venv python ../docs/generate_sqli_guide_pdf.py
  Manual PDF: open the HTML file → Ctrl+P → Save as PDF

------------------------------------------

Important Notes

Do not commit:

venv/
__pycache__/
.db files
.vscode/

These are already ignored by .gitignore.
