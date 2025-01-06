import pytest
import redis
from unittest.mock import patch
from app.cache.cache import Cache
from config import CONFIG

@pytest.fixture
def cache():
    return Cache()

def test_set_cache(cache):
    # Test setting cache with a string value
    cache.set("test_key", "test_value")
    stored_value = cache.get("test_key")
    assert stored_value == b"test_value", f"Expected b'test_value', but got {stored_value}"

def test_get_cache_key_not_found(cache):
    # Test getting cache for a non-existing key
    stored_value = cache.get("non_existent_key")
    assert stored_value is None, f"Expected None, but got {stored_value}"