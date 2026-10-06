import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'packages', 'contracts', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from yemenjpt.main import create_app

@pytest.fixture(scope="session")
def app():
    return create_app()

@pytest.fixture(scope="session")
def client(app):
    with TestClient(app) as c:
        yield c

@pytest.fixture
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
