# 🚀 RunLab API Endpoints

Base URL: `http://localhost:8000`

## Health & Info

### `GET /`
Health check endpoint

**Response:**
```json
{
  "status": "running",
  "service": "RunLab API",
  "version": "0.1.0"
}
```

---

## Parsing Endpoints

### `POST /api/parse`
Parse runme.md content from JSON

**Request Body:**
```json
{
  "content": "# My App\n...",
  "spec_name": "my-app"  // optional
}
```

**Response:**
```json
{
  "spec": {
    "name": "my-app",
    "description": "...",
    "inputs": [...],
    "command": "...",
    "compute": {...}
  },
  "ui_config": {
    "title": "My App",
    "fields": [...]
  }
}
```

### `POST /api/parse/file`
Upload and parse a runme.md file

**Form Data:**
- `file`: The .runme.md or .md file

**Response:** Same as `/api/parse`

---

## Spec Management

### `GET /api/specs`
List all parsed specifications

**Response:**
```json
{
  "my-app": {
    "spec": {...},
    "ui_config": {...}
  },
  "another-app": {...}
}
```

### `GET /api/specs/{spec_name}`
Get a specific parsed spec

**Response:**
```json
{
  "spec": {...},
  "ui_config": {...}
}
```

### `DELETE /api/specs/{spec_name}`
Delete a parsed specification

**Response:**
```json
{
  "status": "deleted",
  "spec_name": "my-app"
}
```

---

## Job Execution

### `POST /api/run`
Execute a job with user inputs

**Request Body:**
```json
{
  "spec_name": "my-app",
  "inputs": {
    "message": "Hello!",
    "count": 5
  }
}
```

**Response:**
```json
{
  "job_id": "abc-123-def",
  "status": "completed",
  "created_at": "2025-01-15T10:30:00",
  "completed_at": "2025-01-15T10:30:05",
  "logs": "STDOUT output here...",
  "output_urls": ["https://s3.../output.txt"],
  "error": null
}
```

### `GET /api/jobs/{job_id}`
Check job status

**Response:** Same as `/api/run` response

---

## Development Only

### `GET /api/debug/specs`
Debug endpoint to see raw parsed specs (only in development mode)

---

## Example Workflow

```bash
# 1. Parse a runme.md file
curl -X POST http://localhost:8000/api/parse/file \
  -F "file=@examples/simple-hello.runme.md"

# 2. List available specs
curl http://localhost:8000/api/specs

# 3. Run a job
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "spec_name": "hello-world",
    "inputs": {
      "name": "RunLab",
      "count": 3,
      "enthusiastic": true
    }
  }'

# 4. Check job status
curl http://localhost:8000/api/jobs/{job_id}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad request (validation error, missing required field)
- `404` - Not found (spec or job doesn't exist)
- `500` - Internal server error (parsing failed, execution error)

---

## Interactive Documentation

Visit **http://localhost:8000/docs** for:
- Interactive API explorer
- Request/response examples
- Try it out feature
- Schema documentation

Or visit **http://localhost:8000/redoc** for alternative documentation view.
