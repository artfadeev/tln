from datetime import datetime
from tln import db


def test_formatters_default1(geo_db):
    db.filter_concepts(geo_db, "", ())
    result = geo_db.execute(db.query("formatters/default")).fetchall()

    assert result[-1]["label"] == "Panda bears may be dangerous"
    assert result[-1]["timestamp"] == datetime(2021, 1, 2, 12, 32, 22)
    assert result[-7]["label"].startswith("Central Park")


def test_formatters_default2(geo_db):
    db.filter_concepts(geo_db, "Moscow", ())
    result = geo_db.execute(db.query("formatters/default")).fetchall()
    assert result[0]["label"] == "moscow"
    assert result[1]["label"].startswith("Moscow")
