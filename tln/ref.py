from . import db
from . import utils


def label(connection, label):
    """Label reference: select concept by its label text"""

    # TODO: case conversion works only for ASCII
    cursor = connection.execute(db.query("label_reference"), {"label": label.lower()})

    row = cursor.fetchone()

    if not row:
        raise utils.ReferenceException(f"No concept has label {label!r}!")

    if cursor.fetchone():
        raise utils.ReferenceException(f"Several concepts match label {label!r}!")

    return row["id"]


def id(connection, id):
    cursor = connection.execute(db.query("id_reference"), {"id": id})

    row = cursor.fetchone()

    if not row:
        raise utils.ReferenceException(f"There is no concept with id {id!r}!")

    return row["id"]


def mark(connection, mark):
    cursor = connection.execute(db.query("mark_reference"), {"mark": mark})

    row = cursor.fetchone()
    if not row:
        raise utils.ReferenceException(f"There is no mark named {mark!r}!")
    return row["id"]


def prefix(connection, prefix):
    cursor = connection.execute(db.query("prefix_reference"), {"prefix": prefix})

    row = cursor.fetchone()
    if not row:
        raise utils.ReferenceException(f"There is no concept with prefix {prefix!r}!")
    if cursor.fetchone():
        raise utils.ReferenceException(f"Several concepts match prefix {prefix!r}!")
    return row["id"]

def substring(connection, substring):
    cursor = connection.execute(db.query("substring_reference"), {"substring": substring})

    row = cursor.fetchone()
    if not row:
        raise utils.ReferenceException(f"No concept contains text {substring!r}!")
    if cursor.fetchone():
        raise utils.ReferenceException(f"Several concepts contain text {substring!r}!")
    return row["id"]

def latest(connection):
    cursor = connection.execute(db.query("latest_reference"))

    row = cursor.fetchone()
    if not row:
        raise utils.ReferenceException(
            f"There are no timestamped concepts in the database!"
        )
    return row["id"]


def any(connection, reference):
    if reference.startswith("@"):
        return id(connection, reference[1:])
    elif reference.startswith("."):
        return mark(connection, reference[1:])
    elif reference.startswith("/prefix:"):
        return prefix(connection, reference[8:])
    elif reference.startswith("//"):
        return substring(connection, reference[2:])
    elif reference == "/":
        return latest(connection)
    return label(connection, reference)
