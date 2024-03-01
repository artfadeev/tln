import sqlite3
import functools

import pytest
from click.testing import CliRunner
import click

from tln import cli, ReferenceType


def provide_db(function):
    @functools.wraps(function)
    def inner(data_path, *args, **kwargs):
        init_script = (data_path / "test_data.sql").read_text()
        runner = CliRunner()

        with runner.isolated_filesystem():
            conn = sqlite3.connect("test.db")
            conn.executescript(init_script)
            conn.commit()

            function(data_path, *args, **kwargs, runner=runner)

    return inner


@provide_db
def test_path(data_path, runner=None):
    assert (
        runner.invoke(cli, ["--db_path", "test.db", "path"]).output.strip() == "test.db"
    )


@provide_db
def test_show(data_path, runner=None):
    test_cases = [
        ("@tag_manhattan", "tag_manhattan"),
        (".msk", "moscow_fact"),
        ("/prefix:todo", "space_travel"),
        ("//famous park", "cool_park"),
        ("/", "unrelated_fact"),
        ("country", "tag_country"),
    ]

    for reference, id in test_cases:
        assert (
            runner.invoke(
                cli, ["--db_path", "test.db", "show", reference]
            ).output.splitlines()[0]
            == id
        )

    assert (
        runner.invoke(
            cli, ["--db_path", "test.db", "show", "todo:", "go", "into space"]
        ).output.splitlines()[0]
        == "space_travel"
    )

    # invalid reference
    assert (
        runner.invoke(cli, ["--db_path", "test.db", "show", "ASDFASDF"]).exit_code != 0
    )

    # no reference
    assert runner.invoke(cli, ["--db_path", "test.db", "show"]).exit_code != 0


@provide_db
def test_add(data_path, runner=None):
    runner.invoke(cli, ["--db_path", "test.db", "add", "NEW ONE"])
    assert "NEW ONE" in runner.invoke(cli, ["--db_path", "test.db", "list"]).output

    assert runner.invoke(cli, ["--db_path", "test.db", "add"]).exit_code == 1


@provide_db
def test_basic_list(data_path, runner=None):
    result = runner.invoke(
        cli, ["--db_path", "test.db", "--max_width", "100000", "list"]
    )
    lines = result.output.splitlines()
    assert len(lines) == 17
    assert "Panda" in lines[-1]
    assert "2021.01.02" in lines[-1]
    assert "china" in lines[-1]


@provide_db
def test_init(data_path, runner=None):
    assert runner.invoke(cli, ["init", "test.db"]).exit_code != 0
    assert runner.invoke(cli, ["init", "new_test.db"]).exit_code == 0

    def invoke(*args):
        return runner.invoke(cli, ["--db_path", "new_test.db", *args])

    assert len(invoke("list").output.splitlines()) == 1

    assert invoke("show", "/").exit_code == 1

    # insert new element
    assert invoke("add", "Hello world!").exit_code == 0
    assert invoke("add", "--id", "second", "Another hello!").exit_code == 0

    assert "second" in invoke("show", "/").output


@provide_db
def test_tag_system(data_path, runner=None):
    assert runner.invoke(cli, ["init", "new_test.db"]).exit_code == 0

    def invoke(*args):
        return runner.invoke(cli, ["--db_path", "new_test.db", *args])

    for invocation in [
        invoke("add", "year1828"),
        invoke("tag", "year1828", "tag"),
        invoke("mark", "year1828", ".1828"),
        invoke("add", "19th_century"),
        invoke("tag", "/", "tag"),
        invoke("mark", "/", "XIX"),
        invoke("relation", "year1828", "subtag_of", "19th_century"),
        invoke("add", "--id", "leo_tolstoy", "Leo Tolstoy was born in 1828"),
        invoke("tag", "@leo_tolstoy", "year1828"),
    ]:
        assert invocation.exit_code == 0

    tagged_year1828 = invoke("list", "-t", "year1828")
    tagged_19th_century = invoke("list", "-t", ".XIX")
    assert tagged_year1828.exit_code == tagged_19th_century.exit_code == 0
    assert tagged_year1828.output == tagged_19th_century.output
    assert "Leo Tolstoy" in tagged_year1828.output

    # tag with zero tags shouldn't produce an error
    assert invoke("tag", "XIX").exit_code == 0


@provide_db
def test_list_max_width(data_path, runner=None):
    long_label = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
        "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim "
        "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
        "aliquip ex ea commodo consequat. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
        "culpa qui officia deserunt mollit anim id est laborum."
    )
    assert (
        runner.invoke(cli, ["--db_path", "test.db", "add", long_label]).exit_code == 0
    )

    result_lines = runner.invoke(
        cli, ["--db_path", "test.db", "--max_width", "50", "list"]
    ).output.splitlines()
    assert all(len(line) <= 50 for line in result_lines)


@provide_db
def test_add_editor(data_path, monkeypatch, runner=None):
    monkeypatch.setattr(
        click, "edit", lambda label: label + " label text added in editor"
    )

    assert (
        runner.invoke(
            cli, ["--db_path", "test.db", "add", "--editor", "label text from cli"]
        ).exit_code
        == 0
    )
    assert (
        "label text from cli label text added in editor"
        in runner.invoke(cli, ["--db_path", "test.db", "show", "/"]).output
    )


@provide_db
def test_no_db(data_path, monkeypatch, runner=None):
    monkeypatch.delenv("TLN_DB", raising=False)

    assert runner.invoke(cli, ["list"]).exit_code != 0


@provide_db
def test_ReferenceType(data_path, monkeypatch, runner=None):
    monkeypatch.setenv("TLN_DB", "test.db")
    r = ReferenceType()
    result = r.shell_complete(None, None, ".ms")
    assert len(result) == 1
    assert result[0].value == ".msk"
    assert result[0].help.startswith("Moscow")

    assert not r.shell_complete(None, None, "asdfsfas")
    assert not r.shell_complete(None, None, "")

    monkeypatch.delenv("TLN_DB")
    r = ReferenceType()
    assert not r.shell_complete(None, None, ".ms")
