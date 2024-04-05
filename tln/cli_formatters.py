import click
import textwrap
from collections import defaultdict
from . import db

formatters = {}


def register_formatter(name):
    def decorator(formatter):
        global formatters
        formatters[name] = formatter
        return formatter

    return decorator


@register_formatter("default")
def list_default(ctx, connection):
    previous_date = None
    date_col_width = 11  # "1970.01.01 "
    time_col_width = 6  # "12:34 "
    for row in connection.execute(db.query("formatters/default")):
        current_date = row["timestamp"].strftime("%Y.%m.%d") if row["timestamp"] else ""
        time = row["timestamp"].strftime("%H:%M") if row["timestamp"] else ""
        click.echo(f"{current_date*(current_date!=previous_date):11}{time:6}", nl=False)

        text = (f"[{row['tags']}] " if row["tags"] else "") + row["label"]
        lines = [
            line
            for paragraph in text.splitlines()
            for line in textwrap.wrap(
                paragraph,
                width=ctx.obj["max_width"] - date_col_width - time_col_width,
                break_long_words=False,
            )
        ]
        click.echo(lines[0])
        for line in lines[1:]:
            click.echo(" " * (date_col_width + time_col_width) + line)

        previous_date = current_date


@register_formatter("ids")
def list_ids(ctx, connection):
    for row in connection.execute(db.query("formatters/ids")):
        click.echo(row["id"])


@register_formatter("tags")
def list_hierarchy(ctx, connection):
    top_level = set()  # tags which are not subtags of other tags
    labels = {}  # get label of tag by id
    children = defaultdict(set)  # ids of subtags by tag id
    count = {}  # number of concepts directly tagged by this tag

    for id, label, directly_tagged in connection.execute(
        db.query("formatters/tags_info")
    ):
        top_level.add(id)
        labels[id] = label
        count[id] = directly_tagged

    for subject, object in connection.execute(db.query("formatters/tags_subtag_pairs")):
        top_level -= {subject}
        children[object].add(subject)

    # depth-first search
    were = set()

    def show(id, level=0):
        nonlocal were
        if id in were:
            return click.echo(f'{"    "*level}{labels[id]} ({count[id]}, see above)')

        click.echo(f'{"    "*level}{labels[id]} ({count[id]})')
        were.add(id)
        for child in sorted(children[id], key=count.__getitem__, reverse=True):
            show(child, level + 1)

    for id in sorted(top_level, key=count.__getitem__, reverse=True):
        show(id)
