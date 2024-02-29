import pathlib
import pytest
import tln


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / "data"


@pytest.fixture
def geo_db(data_path):
    """Connection to a toy database about geography"""
    connection = tln.db.connect(":memory:")
    connection.executescript((data_path / "test_data.sql").read_text())
    return connection
