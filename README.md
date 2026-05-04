# Flask PostgreSQL CRUD API

Simple REST API using Flask and PostgreSQL.

For setup and testing commands, read [START_INSTRUCTIONS.md](START_INSTRUCTIONS.md).

## Project Structure

```text
app/
  controllers/      HTTP request and response logic
  helpers/          Shared response and SQL helpers
  middleware/       Global error handlers
  repositories/     PostgreSQL SQL queries
  routes/           API route definitions
  schemas/          Request validation
  services/         Business logic
tests/              Automated API tests
run.py              App entry point
```

## Endpoints

```text
GET    /health
POST   /api/v1/users
GET    /api/v1/users
GET    /api/v1/users/<user_id>
PUT    /api/v1/users/<user_id>
DELETE /api/v1/users/<user_id>
```

