import pathlib
import pytest
import tln

data_path = pathlib.Path(__file__).parent / "data"


@pytest.fixture
def geo_db():
    """Connection to a toy database about geography"""
    connection = tln.db.connect(":memory:")
    connection.executescript((data_path / "test_data.sql").read_text())
    return connection
