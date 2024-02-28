import sqlite3
import pathlib
import functools

_sql_root = pathlib.Path(__file__).parent / "sql"

queries = {
    "list": _sql_root / "list.sql",  # search and list entries from the database
    "label_reference": _sql_root / "label_reference.sql",  # get id by label
    "id_reference": _sql_root / "id_reference.sql",  # check that id exists
    "mark_reference": _sql_root / "mark_reference.sql",  # get id by mark
    "prefix_reference": _sql_root / "prefix_reference.sql",  # get id by prefix
    "latest_reference": _sql_root
    / "latest_reference.sql",  # get id of the latest concept
    "substring_reference": _sql_root / "substring_reference.sql",
    "show_concept": _sql_root / "show_concept.sql",  # get concept by id
    "tag_concept": _sql_root / "tag_concept.sql",  # tag concept
    "mark_concept": _sql_root / "mark_concept.sql",  # mark concept
    "add_concept": _sql_root / "add_concept.sql",  # add concept
    "list_with_tag_filters": _sql_root / "list_with_tag_filters.sql",
    "selected_tags_create": _sql_root / "selected_tags_create.sql",
    "selected_tags_insert": _sql_root / "selected_tags_insert.sql",
}


@functools.cache
def query(name):
    return queries[name].read_text()


def connect(path):
    connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection


def list_concepts(connection, search_query: str, tags: set[str]):
    if not tags:
        return connection.execute(query("list"), {"query": search_query.lower()})

    connection.execute(query("selected_tags_create"))
    connection.executemany(
        query("selected_tags_insert"), ({"id": tag_id} for tag_id in tags)
    )
    return connection.execute(
        query("list_with_tag_filters"), {"query": search_query.lower()}
    )
