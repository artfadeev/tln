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
        raise utils.ReferenceException(f"There is no mark named {mark!r}")
    return row["id"]


def any(connection, reference):
    if reference.startswith("@"):
        return id(connection, reference[1:])
    elif reference.startswith("."):
        return mark(connection, reference[1:])
    return label(connection, reference)
