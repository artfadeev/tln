import click
import sqlite3
import textwrap


@click.group()
def cli():
    """TLN information management system"""
    pass


@cli.command("list")
@click.argument("query", required=False, default="")
@click.option("-p", "--path", envvar="TLN_DB", help="Path to the database")
@click.option("--maxwidth", default=120, type=int, help="Maximum output's width")
def list_(path: str, query: str, maxwidth: int):
    """Print entries from the database"""
    if not path:
        click.echo("No database! Aborting.")
        exit(1)

    db_connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    db_connection.row_factory = sqlite3.Row

    cursor = db_connection.cursor()
    cursor.execute(
        "select note.timestamp, note.label, group_concat(tag.label, ', ') as tags"
        " from concepts as note"
        "    left join relations on note.id=relations.subject and relations.relation='tagged'"
        "    left join concepts as tag on relations.object=tag.id"
        " where instr(note.label, ?)>0"
        " group by note.id"
        " order by note.timestamp asc",
        (query,),
    )

    previous_date = None
    date_col_width = 11  # "1970.01.01 "
    time_col_width = 6  # "12:34 "
    while row := cursor.fetchone():
        current_date = row["timestamp"].strftime("%Y.%m.%d") if row["timestamp"] else ""
        time = row["timestamp"].strftime("%H:%M") if row["timestamp"] else ""
        click.echo(f"{current_date*(current_date!=previous_date):11}{time:6}", nl=False)

        text = (f"[{row['tags']}] " if row["tags"] else "") + row["label"]
        lines = textwrap.wrap(
            text,
            width=maxwidth - date_col_width - time_col_width,
            break_long_words=False, # don't break links
        )
        click.echo(lines[0])
        for line in lines[1:]:
            click.echo(" " * (date_col_width + time_col_width) + line)

        previous_date = current_date

    db_connection.close()
