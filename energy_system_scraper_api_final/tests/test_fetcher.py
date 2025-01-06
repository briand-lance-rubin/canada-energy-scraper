import pytest
from unittest.mock import patch, MagicMock
from app.scraper.fetcher import Fetcher
from config import CONFIG

@pytest.fixture
def fetcher():
    return Fetcher("http://example.com")

@patch("app.scraper.fetcher.aiohttp.ClientSession.get")
async def test_fetch_data(mock_get, fetcher):
    mock_response = MagicMock()
    mock_response.text.return_value = "<html><table></table></html>"
    mock_get.return_value = mock_response
    html_content = await fetcher.fetch()
    assert html_content == "<html><table></table></html>"
