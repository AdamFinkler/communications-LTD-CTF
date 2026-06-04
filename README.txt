First-Time Setup Summary

git clone https://github.com/alonkr13/communications-LTD-CTF-SECURE.git
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

------------------------------------------

Important Notes

Do not commit:

venv/
__pycache__/
.db files
.vscode/

These are already ignored by .gitignore.


-----------------------------------------

!!!!! VERY IMPORTANT !!!!!

 1. replace the .vscode/settings.json with this:

{
  "liveServer.settings.ignoreFiles": [
    ".vscode/**",
    "**/*.db",
    "**/*.db-journal",
    "**/*.db-wal",
    "**/*.db-shm",
    "backend/**"
  ]
}

 2. Then stop and restart Live Server (click "Port: 5500" in the status bar to stop, then right-click the page → Open with Live Server), and hard-refresh the browser (Ctrl+Shift+R).

