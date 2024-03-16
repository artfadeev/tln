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
        lines = textwrap.wrap(
            text,
            width=ctx.obj["max_width"] - date_col_width - time_col_width,
            break_long_words=False,  # don't break links
        )
        click.echo(lines[0])
        for line in lines[1:]:
            click.echo(" " * (date_col_width + time_col_width) + line)

        previous_date = current_date


@register_formatter("ids")
def list_ids(ctx, connection):
    for row in connection.execute(db.query("formatters/ids")):
        click.echo(row["id"])
