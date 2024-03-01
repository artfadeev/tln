import pytest

from tln import ref, ReferenceType
from tln.utils import ReferenceException
from tln.ref import CompletionSuggestion


def test_complete_label(geo_db):
    def suggestions(text, allow_whitespace=False):
        return set(
            c.suggestion
            for c in ref.complete_label(geo_db, text, allow_whitespace=allow_whitespace)
        )

    assert suggestions("M") == {"moscow", "manhattan"}
    assert suggestions("m", allow_whitespace=True) == {
        "moscow",
        "manhattan",
        "Moscow is the largest city in Russia",
    }


def test_complete_id(geo_db):
    def suggestions(text, allow_whitespace=False):
        return set(
            c.suggestion
            for c in ref.complete_id(geo_db, text, allow_whitespace=allow_whitespace)
        )

    assert suggestions("tag_m") == {"tag_moscow", "tag_manhattan"}

    assert ref.complete_id(geo_db, "tag_newy") == [
        CompletionSuggestion("tag_newyork", "new_york")
    ]


def test_complete_mark(geo_db):
    assert ref.complete_mark(geo_db, "u") == [CompletionSuggestion("us", "usa")]


def test_complete_substring(geo_db):
    assert ref.complete_substring(geo_db, "bears may be", allow_whitespace=True) == [
        CompletionSuggestion("bears may be dangerous", "Panda bears may be dangerous")
    ]
    assert ref.complete_substring(geo_db, "bears", allow_whitespace=False) == []
    assert ref.complete_substring(geo_db, "anha", allow_whitespace=False) == [
        CompletionSuggestion("anhattan", "manhattan")
    ]


def test_complete_any(geo_db):
    def suggestions(text, allow_whitespace=False):
        return set(
            c.suggestion
            for c in ref.complete_any(geo_db, text, allow_whitespace=allow_whitespace)
        )

    assert suggestions("@tag_lo") == {"@tag_london"}
    assert suggestions(".ms") == {".msk"}
    assert suggestions("/prefix:tra") == {"/prefix:travel"}
    assert suggestions("//largest city", True) == {"//largest city in Russia"}
    assert suggestions("/") == set()
    assert suggestions("i visited", True) == {"I visited Spain", "i visited Spain"}
