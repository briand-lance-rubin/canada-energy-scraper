import pytest
from app.scraper.parser import Parser

@pytest.fixture
def parser():
    return Parser()

def test_parse_table_no_table(parser):
    html_content = "<html><div>No table here</div></html>"
    headers, rows = parser.parse_table(html_content)
    assert headers == []
    assert rows == []

