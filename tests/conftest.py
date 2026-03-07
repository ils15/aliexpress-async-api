import os

import pytest
from dotenv import load_dotenv

from aliexpress_async_api import AliExpressIOPClient

load_dotenv()


@pytest.fixture
def app_key():
    return os.getenv("APP_KEY")


@pytest.fixture
def app_secret():
    return os.getenv("APP_SECRET")


@pytest.fixture
def tracking_id():
    return os.getenv("TRACKING_ID")


@pytest.fixture
async def api_client(app_key, app_secret, tracking_id):
    if not app_key or not app_secret:
        pytest.skip("APP_KEY and APP_SECRET not found in environment")

    async with AliExpressIOPClient(app_key, app_secret, tracking_id) as client:
        yield client
