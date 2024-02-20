import textwrap
import os
import sys
import datetime

import click

from . import db
from . import ref
from . import utils


@click.group()
@click.pass_context
@click.option("--maxwidth", default=120, type=int, help="Maximum display width")
def cli(ctx, maxwidth):
    """TLN information management system"""
    ctx.ensure_object(dict)
    ctx.obj["db_path"] = os.environ.get("TLN_DB", None)
    ctx.obj["max_width"] = maxwidth

    if not ctx.obj["db_path"]:
        click.echo(f"$TLN_DB is not set. Aborting.", err=True)
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


@cli.command("show")
@click.argument("reference", nargs=-1)
@click.pass_context
def show(ctx, reference):
    """Find concept by reference"""
    if not reference:
        click.echo("No reference given.", err=True)
        exit(1)
    reference = " ".join(reference)

    connection = db.connect(ctx.obj["db_path"])
    id_ = ref.any(connection, reference)

    # TODO: proper transaction control
    _, timestamp, label = connection.execute(
        db.query("show_concept"), {"id": id_}
    ).fetchone()

    click.echo(f"Id: {id_}")
    if timestamp:
        click.echo(f"Timestamp: {timestamp}")

    click.echo(textwrap.fill(label, width=ctx.obj["max_width"], break_long_words=False))


@cli.command("tag")
@click.argument("concept")
@click.argument("tags", nargs=-1)
@click.pass_context
def tag(ctx, concept, tags):
    """Tag a concept"""

    if not tags:
        exit(0)

    connection = db.connect(ctx.obj["db_path"])
    concept_id = ref.any(connection, concept)
    tag_ids = [ref.any(connection, t) for t in tags]

    connection.executemany(
        db.query("tag_concept"),
        [{"concept": concept_id, "tag": tag_id} for tag_id in tag_ids],
    )
    connection.commit()


@cli.command("mark")
@click.argument("concept")
@click.argument("mark")
@click.pass_context
def mark(ctx, concept, mark):
    """Mark a concept"""
    connection = db.connect(ctx.obj["db_path"])
    concept_id = ref.any(connection, concept)
    if mark.startswith("."):
        mark = mark[1:]

    connection.execute(db.query("mark_concept"), {"concept": concept_id, "mark": mark})
    connection.commit()


@cli.command("add")
@click.argument("label", nargs=-1)
@click.option("--id", type=str, default=None, help="id of the concept")
@click.option(
    "--editor", is_flag=True, default=False, help="Launch editor to edit the label"
)
@click.pass_context
def add(ctx, label, editor, id):
    """Add a concept"""
    label = " ".join(label)
    if editor:
        label = click.edit(label).strip()
    if not label:
        click.echo("Empty label is not allowed.", err=True)
        exit(1)

    id = id or utils.generate_id()
    timestamp = datetime.datetime.now()

    connection = db.connect(ctx.obj["db_path"])
    # TODO: hope id is unique!
    connection.execute(
        db.query("add_concept"), {"id": id, "timestamp": timestamp, "label": label}
    )
    connection.commit()
