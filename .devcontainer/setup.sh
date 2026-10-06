#!/usr/bin/env bash
# YemenJPT — Codespaces post-create setup.
# Installs backend + frontend dependencies. Postgres 15 is provided by the
# devcontainer "postgres" feature and is already running on localhost:5432.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> YemenJPT setup starting (root: $ROOT)"

echo "==> Python: $(python3 --version)"
echo "==> Node:   $(node --version)"

# ---------------------------------------------------------------- backend deps
echo "==> Installing backend dependencies"
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install --quiet \
  "fastapi==0.115.0" \
  "uvicorn[standard]==0.30.6" \
  "sqlalchemy[asyncio]==2.0.36" \
  "asyncpg==0.29.0" \
  "alembic==1.13.3" \
  "pydantic==2.9.2" \
  "pydantic-settings==2.5.2" \
  httpx==0.27.2 \
  networkx==3.4.1 \
  "numpy==1.26.4" \
  python-dateutil==2.9.0 \
  structlog==24.4.0 \
  tenacity==9.0.0 \
  orjson==3.10.7 \
  pytest \
  pytest-asyncio

# ------------------------------------------------------------- frontend deps
echo "==> Installing frontend dependencies"
cd "$ROOT/apps/web"
if [ -f package-lock.json ]; then
  npm ci || npm install
else
  npm install
fi

# ------------------------------------------------------------------ env files
cd "$ROOT"
if [ ! -f apps/api/.env ] && [ -f apps/api/.env.example ]; then
  cp apps/api/.env.example apps/api/.env
  echo "==> Created apps/api/.env from .env.example (review DATABASE_URL)"
fi
if [ ! -f apps/web/.env.local ]; then
  printf 'NEXT_PUBLIC_API_URL=http://localhost:8000\n' > apps/web/.env.local
  echo "==> Created apps/web/.env.local"
fi

# ------------------------------------------------------------------- sanity
echo "==> Running backend tests"
cd "$ROOT/apps/api"
PYTHONPATH="$ROOT/apps/api/src:$ROOT/packages/contracts/src" python3 -m pytest tests/ -q --tb=line || \
  echo "!! tests did not pass — see output above"

cat <<'EOF'

==> Setup complete.

Next steps:
  make dev     # API :8000  + UI :3000   (in one terminal)
  make seed    # load SYNTHETIC development fixtures (API must be running)
  make test    # re-run pytest

Ports 8000 and 3000 are forwarded automatically; open the "Ports" panel to
click the forwarded address.
EOF