.PHONY: install dev test lint seed docker-up docker-down reset

install:
	cd apps/api && pip install -e ".[dev]"
	cd packages/contracts && pip install -e .
	cd apps/web && npm install

dev:
	cd apps/api && uvicorn yemenjpt.main:app --reload --host 0.0.0.0 --port 8000 &
	cd apps/web && npm run dev

test:
	cd apps/api && python -m pytest tests/ -v --tb=short

lint:
	cd apps/api && python -m ruff check src/ tests/

seed:
	python apps/api/data/seed.py

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d --build
