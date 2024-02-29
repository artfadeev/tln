import sqlite3
import pathlib
import functools

_sql_root = pathlib.Path(__file__).parent / "sql"


@functools.cache
def query(name):
    return (_sql_root / f"{name}.sql").read_text()


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
