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
    "show_concept": _sql_root / "show_concept.sql",  # get concept by id
    "tag_concept": _sql_root / "tag_concept.sql",  # tag concept
    "mark_concept": _sql_root / "mark_concept.sql",  # mark concept
}


@functools.cache
def query(name):
    return queries[name].read_text()


def connect(path):
    connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection
