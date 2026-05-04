# Simple Start Guide

This project uses Flask + PostgreSQL.

Use these commands in Windows PowerShell.

## 1. Go To Project

```powershell
cd "c:\Users\SAINA\OneDrive\Documents\Div\rest api python"
```

## 2. Install Python Packages

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

## 3. Setup PostgreSQL

Install PostgreSQL on your computer.

Create a database named:

```text
flask_pg_crud
```

If `psql` works in your terminal, run:

```powershell
psql -U postgres -c "CREATE DATABASE flask_pg_crud;"
```

If `psql` does not work, create the database from pgAdmin.

## 4. Check .env

Open `.env`.

Update the password if your PostgreSQL password is different:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask_pg_crud
```

Format:

```text
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

The app creates the `users` table automatically when it starts.

## 5. Start API

```powershell
python run.py
```

Keep this terminal open.

API URL:

```text
http://127.0.0.1:5000
```

## 6. Test API

Open a new PowerShell terminal.

### Health

```powershell
curl.exe http://127.0.0.1:5000/health
```

### Create User

Use a new email each time.

```powershell
curl.exe --% -X POST http://127.0.0.1:5000/api/v1/users -H "Content-Type: application/json" --data-raw "{\"name\":\"Div\",\"email\":\"div@example.com\",\"age\":25}"
```

Copy the returned `id`.

### Get All Users

```powershell
curl.exe http://127.0.0.1:5000/api/v1/users
```

### Get One User

Replace `USER_ID_HERE`.

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

## 7. Easy Full Test

This runs create, get, update, and delete automatically:

```powershell
.\scripts\test_api.ps1
```

## 8. Run Automated Tests

These tests do not need PostgreSQL.

```powershell
python -m pytest -q
```

Expected:

```text
2 passed
```

## 9. Stop API

In the API terminal:

```powershell
Ctrl + C
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

