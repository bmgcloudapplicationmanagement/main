# Backend

Python Flask API with SQLite for bicycle repair requests. This is a coursework prototype using fictional customer data.

## Requirements
- Python 3.12+
- PowerShell (Windows)

## Setup and run
Open a terminal in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:STAFF_API_KEY = "change-this-demo-key"
$env:DATABASE_PATH = "data/repairs.db"
python run.py
```

Check: http://127.0.0.1:5000/api/health

## Test and demonstrate
Leave the server running. Open a **second** PowerShell terminal in the same folder:

```powershell
.\.venv\Scripts\Activate.ps1
$env:STAFF_API_KEY = "change-this-demo-key"
$env:DATABASE_PATH = "data/repairs.db"
python -m pytest -v
.\scripts\demo_requests.ps1
python scripts/inspect_database.py
```

The staff key must match the key used to start the server. The demo script creates, lists, updates and retrieves a fictional repair request.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Check server health |
| POST | `/api/repairs` | Create a repair request |
| GET | `/api/repairs` | List requests (staff key) |
| GET | `/api/repairs/<id>` | Get request (staff key) |
| PATCH | `/api/repairs/<id>` | Update status (staff key) |

Staff-only requests require header `X-Staff-Key` with the configured key. Allowed statuses: `Pending`, `In Progress`, `Completed`.

The SQLite file is generated automatically at `data/repairs.db`. Do not commit the database, virtual environment or secret keys to GitHub.
