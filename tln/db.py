import sqlite3
import pathlib
import functools

_sql_root = pathlib.Path(__file__).parent / "sql"

queries = {
    "list": _sql_root / "list.sql",  # search and list entries from the database
}


@functools.cache
def query(name):
    return queries[name].read_text()


def connect(path):
    connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection
