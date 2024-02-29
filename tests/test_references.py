import pytest

from tln import ref
from tln.utils import ReferenceException


def test_label_reference(geo_db):
    assert ref.label(geo_db, "moscow") == "tag_moscow"
    assert ref.label(geo_db, "panda bears may be dangerous") == "unrelated_fact"
    assert ref.label(geo_db, "tag") == "tln/is_tag"

    for bad_label in ["toronto", "todo: swim"]:
        with pytest.raises(ReferenceException):
            ref.label(geo_db, bad_label)

    # repeating label
    with pytest.raises(ReferenceException):
        ref.label(geo_db, "I visited Spain")


def test_id_reference(geo_db):
    assert ref.id(geo_db, "capital_of_uk") == "capital_of_uk"

    for bad_id in ["tln/nothing", "asdf asdf asdf"]:
        with pytest.raises(ReferenceException):
            ref.label(geo_db, bad_id)


def test_mark_reference(geo_db):
    assert ref.mark(geo_db, "us") == "tag_usa"

    for bad_mark in ["MSK", "EKB"]:
        with pytest.raises(ReferenceException):
            ref.mark(geo_db, bad_mark)


def test_prefix_reference(geo_db):
    assert ref.prefix(geo_db, "Panda") == "unrelated_fact"

    with pytest.raises(ReferenceException):
        ref.prefix(geo_db, "c")  # country, china

    with pytest.raises(ReferenceException):
        ref.prefix(geo_db, "NO_SUCH_PREFIX")


def test_substring_reference(geo_db):
    assert ref.substring(geo_db, "capital") == "capital_of_uk"

    with pytest.raises(ReferenceException):
        ref.substring(geo_db, "visit")

    with pytest.raises(ReferenceException):
        ref.substring(geo_db, "AJDKLFJASLKDF")


def test_latest_reference(geo_db):
    assert ref.latest(geo_db) == "unrelated_fact"


def test_any_reference(geo_db):
    assert ref.any(geo_db, "@tag_manhattan") == "tag_manhattan"
    assert ref.any(geo_db, ".msk") == "moscow_fact"
    assert ref.any(geo_db, "/prefix:todo") == "space_travel"
    assert ref.any(geo_db, "//famous park") == "cool_park"
    assert ref.any(geo_db, "/") == "unrelated_fact"
    assert ref.any(geo_db, "country") == "tag_country"

    for bad_reference in ["@asdf", "/asd", "nothing at all", "/prefix:bears"]:
        with pytest.raises(ReferenceException):
            ref.any(geo_db, bad_reference)
