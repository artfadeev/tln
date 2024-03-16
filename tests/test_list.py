from tln.db import filter_concepts


def tags_to_relations_query(tags):
    return [("tagged", t, True) for t in tags]


def filter_concepts_wrapper(connection, *args, **kwargs):
    filter_concepts(connection, *args, **kwargs)
    return [row["id"] for row in connection.execute("select id from list_results")]


def test_filter_concepts_without_filters(geo_db):
    result = filter_concepts_wrapper(geo_db, "", ())
    assert len(result) == 17


def test_filter_concepts_by_substring(geo_db):
    result = filter_concepts_wrapper(geo_db, "Moscow", ())

    assert len(result) == 2
    assert set(result) == {"moscow_fact", "tag_moscow"}


def test_filter_concepts_by_tag(geo_db):
    result = filter_concepts_wrapper(
        geo_db, "", tags_to_relations_query({"tln/is_tag"})
    )
    assert len(result) == 10


def test_filter_concepts_complex(geo_db):
    result = filter_concepts_wrapper(
        geo_db, "ondo", tags_to_relations_query({"tln/is_tag", "tag_city"})
    )
    assert result == ["tag_london"]


def test_filter_concepts_no_results(geo_db):
    assert not filter_concepts_wrapper(
        geo_db, "", tags_to_relations_query({"tag_china", "tag_usa"})
    )


def test_filter_concepts_with_subtag(geo_db):
    assert filter_concepts_wrapper(
        geo_db, "", tags_to_relations_query({"tag_usa"})
    ) == ["cool_park"]


def test_filter_concepts_with_tag_negation(geo_db):
    assert set(
        filter_concepts_wrapper(
            geo_db,
            "",
            (
                ("tagged", "tln/is_tag", True),
                ("tagged", "tag_city", False),
                ("tagged", "tag_country", False),
            ),
        )
    ) == {"tag_manhattan", "tag_city", "tag_country", "tag_travel", "tln/is_tag"}
