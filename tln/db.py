"""Management of underlying SQL database"""
import sqlite3
import pathlib
import functools

_sql_root = pathlib.Path(__file__).parent / "sql"


@functools.cache
def query(name):
    """Retrieve SQL query text from filesystem"""
    return (_sql_root / f"{name}.sql").read_text()


def connect(path):
    connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection


def filter_concepts(
    connection, search_query: str, relations_query: set[tuple[str, str, bool]]
):
    """
    relations_query contains tuples of form (relation, target_object_id, present)
    """
    connection.executescript(query("list/initialize_queries"))

    if relations_query:
        connection.executemany(
            query("list/insert_relations_query"),
            (
                {"relation": relation, "object": object, "present": int(present)}
                for relation, object, present in relations_query
            ),
        )
    if search_query:
        connection.execute(
            query("list/insert_substring_query"), {"search_query": search_query.lower()}
        )

    connection.executescript(query("list/list"))
