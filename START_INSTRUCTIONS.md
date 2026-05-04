# Simple Start Guide

Use these commands in Windows PowerShell.

## 1. Go To Project

```powershell
cd "c:\Users\SAINA\OneDrive\Documents\Div\rest api python"
```

## 2. Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activate does not work:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Start MongoDB

If you use Docker:

```powershell
docker compose up -d
```

Your DB URL is in `.env`:

```env
MONGO_URI=mongodb://localhost:27017/flask_mongo_crud
```

## 4. Start API

```powershell
python run.py
```

Keep this terminal open.

API URL:

```text
http://127.0.0.1:5000
```

## 5. Test API

Open a new PowerShell terminal.

### Health

```powershell
curl.exe http://127.0.0.1:5000/health
```

### Create User

```powershell
curl.exe --% -X POST http://127.0.0.1:5000/api/v1/users -H "Content-Type: application/json" --data-raw "{\"name\":\"Div\",\"email\":\"div@example.com\",\"age\":25}"
```

Copy the returned `id`.

### Get All Users

```powershell
curl.exe http://127.0.0.1:5000/api/v1/users
```

### Get One User

Replace `USER_ID_HERE` with your copied id.

```powershell
curl.exe http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
```

### Update User

Replace `USER_ID_HERE`.

```powershell
curl.exe --% -X PUT http://127.0.0.1:5000/api/v1/users/USER_ID_HERE -H "Content-Type: application/json" --data-raw "{\"name\":\"Div Updated\",\"age\":26}"
```

### Delete User

Replace `USER_ID_HERE`.

```powershell
curl.exe -X DELETE http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
```

## 6. Easy Full Test

This runs create, get, update, and delete automatically:

```powershell
.\scripts\test_api.ps1
```

## 7. Run Automated Tests

```powershell
python -m pytest -q
```

Expected:

```text
2 passed
```

## 8. Stop

Stop Flask:

```powershell
Ctrl + C
```

Stop Docker MongoDB:

```powershell
docker compose down
```

## Endpoint List

```text
GET    /health
POST   /api/v1/users
GET    /api/v1/users
GET    /api/v1/users/<user_id>
PUT    /api/v1/users/<user_id>
DELETE /api/v1/users/<user_id>
```
