import functools
from collections import namedtuple

from click.shell_completion import CompletionItem

from . import db
from . import utils

CompletionSuggestion = namedtuple("CompletionSuggestion", "suggestion, help")


def _error_handler(reference_name, zero_found_text=None, many_found_text=None):
    def wrapper(function):
        @functools.wraps(function)
        def inner(connection, query=None):
            cursor = function(connection, query)
            row = cursor.fetchone()

            if not row:
                raise utils.ReferenceException(
                    zero_found_text.format(query=query)
                    if zero_found_text
                    else f"{reference_name} reference with query {query!r} matches nothing."
                )

            if cursor.fetchone():
                raise utils.ReferenceException(
                    many_found_text.format(query=query)
                    if many_found_text
                    else f"Several concepts match {reference_name} reference with query {query!r}"
                )
            return row["id"]

        return inner

    return wrapper


@_error_handler("label")
def label(connection, label):
    """Label reference: select concept by its label text"""

    # TODO: case conversion works only for ASCII
    return connection.execute(db.query("reference/label"), {"label": label.lower()})


def complete_label(connection, prefix, allow_whitespace=False):
    return [
        CompletionSuggestion(row["label"], help=None)
        for row in connection.execute(
            db.query("complete/label"),
            {"prefix": prefix.lower(), "allow_whitespace": allow_whitespace},
        )
    ]


@_error_handler("id")
def id(connection, id):
    return connection.execute(db.query("reference/id"), {"id": id})


def complete_id(connection, prefix, allow_whitespace=False):
    return [
        CompletionSuggestion(row["id"], help=row["label"])
        for row in connection.execute(
            db.query("complete/id"),
            {"prefix": prefix, "allow_whitespace": allow_whitespace},
        )
    ]


@_error_handler("mark")
def mark(connection, mark):
    return connection.execute(db.query("reference/mark"), {"mark": mark})


def complete_mark(connection, prefix, allow_whitespace=False):
    return [
        CompletionSuggestion(row["name"], help=row["label"])
        for row in connection.execute(
            db.query("complete/mark"),
            {"prefix": prefix, "allow_whitespace": allow_whitespace},
        )
    ]


@_error_handler("prefix")
def prefix(connection, prefix):
    return connection.execute(db.query("reference/prefix"), {"prefix": prefix})


@_error_handler("substring")
def substring(connection, substring):
    return connection.execute(db.query("reference/substring"), {"substring": substring})


def complete_substring(connection, prefix, allow_whitespace=False):
    return [
        CompletionSuggestion(row["label_suffix"], help=row["label"])
        for row in connection.execute(
            db.query("complete/substring"),
            {"prefix": prefix.lower(), "allow_whitespace": allow_whitespace},
        )
    ]


@_error_handler("latest")
def latest(connection, query=""):
    if query:
        raise utils.ReferenceException("Latest reference doesn't take queries")
    return connection.execute(db.query("reference/latest"))


def complete_none(*args, **kwargs):
    return []


_reference_table = (
    # reference_syntax, handler, completion
    ("@", id, complete_id),
    (".", mark, complete_mark),
    ("/prefix:", prefix, complete_label),
    ("//", substring, complete_substring),
    ("/", latest, complete_none),
    ("", label, complete_label),
)


def any(connection, reference):
    for reference_syntax, handler, _ in _reference_table:
        if reference.startswith(reference_syntax):
            return handler(connection, reference[len(reference_syntax) :])

    raise utils.ReferenceException(
        "Unknown reference {reference!r}!"
    )  # pragma: no cover


def complete_any(connection, prefix, allow_whitespace=False):
    for syntax, _, completer in _reference_table:
        if prefix.startswith(syntax):
            return [
                CompletionSuggestion(syntax + suggestion, help)
                for suggestion, help in completer(
                    connection, prefix[len(syntax) :], allow_whitespace=allow_whitespace
                )
            ]
    return []  # pragma: no cover
