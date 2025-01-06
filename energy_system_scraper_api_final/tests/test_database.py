import pytest
from unittest.mock import MagicMock
from app.database.operations import DatabaseOperations
from app.database.models import HistoricalDemand
from config import logger

@pytest.fixture
def db_ops():
    return DatabaseOperations()

def test_save_data(db_ops):
    data = [
        {"Date (HE)": "2025-01-01 01:00", "Forecast Pool Price": 10, "Actual Posted Pool Price": 12}
    ]

    db_ops.db = MagicMock()
    db_ops.db.bulk_insert_mappings = MagicMock()
    db_ops.save_data(data)
    db_ops.db.bulk_insert_mappings.assert_called_once()

def test_fetch_all_data(db_ops):
    db_ops.db.query = MagicMock()
    db_ops.db.query.return_value.all.return_value = []
    data = db_ops.fetch_all_data()
    assert data.empty