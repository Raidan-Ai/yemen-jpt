# YemenJPT API

FastAPI backend for the YemenJPT intelligence platform.

## Quick start

```bash
pip install -e .
uvicorn yemenjpt.main:app --reload
```

## Endpoints

- `GET /health` — health check
- `GET /health/readiness` — readiness probe
- `GET /intelligence/status` — intelligence service status