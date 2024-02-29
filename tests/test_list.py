import pytest

from tln.db import list_concepts


def test_list_without_filters(geo_db):
    result = list_concepts(geo_db, "", set()).fetchall()

    assert len(result) == 17  # 7 notes, 9 tags, 1 tag is tln/is_tag
    assert result[-1]["label"] == "Panda bears may be dangerous"
    assert result[-7]["label"].startswith("Central Park")


def test_list_filter_by_substring(geo_db):
    result = list_concepts(geo_db, "Moscow", set()).fetchall()
    assert len(result) == 2
    assert result[0]["label"] == "moscow"
    assert result[1]["label"].startswith("Moscow")


def test_list_filter_by_tag(geo_db):
    result = list_concepts(geo_db, "", {"tln/is_tag"}).fetchall()
    assert len(result) == 10


def test_list_complex(geo_db):
    result = list_concepts(geo_db, "ondo", {"tln/is_tag", "tag_city"}).fetchall()
    assert len(result) == 1
    assert result[0]["label"] == "london"


def test_list_no_results(geo_db):
    assert not list_concepts(geo_db, "", {"tag_china", "tag_usa"}).fetchall()


def test_list_with_subtag(geo_db):
    result = list_concepts(geo_db, "", {"tag_usa"}).fetchall()
    assert len(result) == 1
    assert result[0]["label"].startswith("Central Park")
