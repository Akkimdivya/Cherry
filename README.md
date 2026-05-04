# Flask MongoDB CRUD API

This is a modular Flask REST API with MongoDB CRUD operations for `users`.

For complete install, run, and endpoint testing commands, see [START_INSTRUCTIONS.md](START_INSTRUCTIONS.md).

## Project Structure

```text
app/
  controllers/      HTTP request and response logic
  helpers/          Shared response and Mongo helpers
  middleware/       Global error handlers
  repositories/     MongoDB queries
  routes/           API route definitions
  schemas/          Request validation
  services/         Business logic
tests/              Automated API tests
run.py              App entry point
```

## Requirements

- Python 3.10+
- MongoDB running locally, or Docker for MongoDB

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configure

The app reads settings from `.env`.

Default local MongoDB URI:

```env
MONGO_URI=mongodb://localhost:27017/flask_mongo_crud
MONGO_DB_NAME=flask_mongo_crud
```

## Start MongoDB

Option 1: if MongoDB is installed locally, start the MongoDB service.

Option 2: use Docker:

```powershell
docker compose up -d
```

## Run API

```powershell
.\.venv\Scripts\python run.py
```

Open:

```text
http://127.0.0.1:5000/health
```

Expected response:

```json
{
  "data": {
    "service": "flask-mongo-crud"
  },
  "message": "API is running",
  "success": true
}
```

## Test With PowerShell

Use `Invoke-RestMethod` in PowerShell. It avoids JSON quoting issues that can happen with `curl.exe` on Windows.

### 1. Health Check

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/health
```

### 2. Create User

```powershell
$body = @{
  name = "Div"
  email = "div@example.com"
  age = 25
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5000/api/v1/users `
  -ContentType "application/json" `
  -Body $body
```

Copy the returned `data.id` value.

### 3. Get All Users

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/v1/users
```

### 4. Get One User

Replace `USER_ID_HERE` with the ID from create response.

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
```

### 5. Update User

```powershell
$body = @{
  name = "Div Updated"
  age = 26
} | ConvertTo-Json

Invoke-RestMethod -Method Put `
  -Uri http://127.0.0.1:5000/api/v1/users/USER_ID_HERE `
  -ContentType "application/json" `
  -Body $body
```

### 6. Delete User

```powershell
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
```

### 7. Confirm Delete

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
```

Expected status: `404`.

## Automated Tests

These tests use `mongomock`, so they do not need a real MongoDB server.

```powershell
.\.venv\Scripts\python -m pytest -q
```

Expected:

```text
2 passed
```

## Manual Test Script

After the Flask API is running, you can test the full CRUD flow with:

```powershell
.\scripts\test_api.ps1
```

## API Endpoints

```text
GET    /health
POST   /api/v1/users
GET    /api/v1/users
GET    /api/v1/users/<user_id>
PUT    /api/v1/users/<user_id>
DELETE /api/v1/users/<user_id>
```
