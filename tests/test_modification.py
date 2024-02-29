import datetime
import pytest

from tln.db import query
from tln import ref


def test_sql_add_concept(geo_db):
    geo_db.execute(
        query("add_concept"),
        {
            "id": "capital_of_finland",
            "timestamp": datetime.datetime(1997, 7, 7, 23, 23),
            "label": "Capital of Finland is Helsinki",
        },
    )
    geo_db.commit()

    result = geo_db.execute(
        "select id, timestamp, label from concepts where id='capital_of_finland'"
    ).fetchall()
    assert len(result) == 1
    assert result[0]["timestamp"] == datetime.datetime(1997, 7, 7, 23, 23)
    assert result[0]["label"] == "Capital of Finland is Helsinki"


def test_sql_insert_relation(geo_db):
    geo_db.execute(
        query("insert_relation"),
        {"subject": "vacation2014", "relation": "tagged", "object": "tag_travel"},
    )
    geo_db.commit()

    assert (
        geo_db.execute(
            "select ('vacation2014', 'tagged', 'tag_travel') in relations"
        ).fetchone()[0]
        == 1
    )


def test_sql_mark_concept(geo_db):
    geo_db.execute(query("mark_concept"), {"concept": "cool_park", "mark": "park"})
    geo_db.commit()

    assert (
        geo_db.execute("select value as id from marks where name='park'").fetchone()[
            "id"
        ]
        == "cool_park"
    )


def test_sql_show_concept(geo_db):
    result = geo_db.execute(query("show_concept"), {"id": "capital_of_uk"}).fetchone()
    assert result["label"] == "London is the capital of Great Britain"
    assert result["id"] == "capital_of_uk"
    assert result["timestamp"].year == 2000


def test_sql_show_relations(geo_db):
    result = geo_db.execute(query("show_relations"), {"id": "tag_newyork"})
    entries = set((row["relation"], row["id"]) for row in result)

    assert entries == {
        ("tagged", "tln/is_tag"),
        ("subtag_of", "tag_usa"),
        ("tagged", "tag_city"),
    }


def test_sql_tag_concept(geo_db):
    geo_db.execute(
        query("tag_concept"), {"concept": "vacation2014", "tag": "tag_travel"}
    )
    geo_db.commit()

    assert geo_db.execute(
        "select ('vacation2014', 'tagged', 'tag_travel') in relations"
    ).fetchone()[0]
