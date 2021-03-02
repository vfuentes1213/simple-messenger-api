import pytest
from api.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def pytest_configure(config):
    config.addinivalue_line("markers", "integration: services are not mocked")