import uuid
import functools
import click


class TLNException(Exception):
    """Base exception class"""

    pass


class ReferenceException(TLNException):
    """Raised when reference lookup fails for some reason"""

    pass


def generate_id():
    return str(uuid.uuid4())[-12:]


def requires_db(function):
    """Decorates CLI handlers, which require database access"""

    @click.pass_context
    @functools.wraps(function)
    def wrapped(ctx, *args, **kwargs):
        if not ctx.obj["db_path"]:
            click.echo(f"$TLN_DB is not set. Aborting.", err=True)
            sys.exit(1)

        return function(ctx, *args, **kwargs)

    return wrapped
