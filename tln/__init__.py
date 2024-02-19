import textwrap
import os
import sys

import click

from . import db


class TLNException(Exception):
    pass


@click.group()
@click.pass_context
@click.option("--maxwidth", default=120, type=int, help="Maximum output's width")
def cli(ctx, maxwidth):
    """TLN information management system"""
    ctx.ensure_object(dict)
    ctx.obj["db_path"] = os.environ.get("TLN_DB", None)
    ctx.obj["max_width"] = maxwidth

    if not ctx.obj["db_path"]:
        print(f"$TLN_DB is not set. Aborting.", file=stderr)
        sys.exit(1)


@cli.command("list")
@click.argument("query", required=False, default="")
@click.pass_context
def list_(ctx, query: str):
    """Print entries from the database"""
    cursor = db.connect(ctx.obj["db_path"]).execute(
        db.query("list"), {"query": query.lower()}
    )

    previous_date = None
    date_col_width = 11  # "1970.01.01 "
    time_col_width = 6  # "12:34 "
    for row in cursor:
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
