"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "id": 1,
        "name": "Test",
        "value": 42
    }


@pytest.fixture
def mock_dataframe():
    """Provide a mock DataFrame for tests."""
    import pandas as pd
    return pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"],
        "col3": [1.1, 2.2, 3.3]
    })
