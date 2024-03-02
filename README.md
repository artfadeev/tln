# tln
tln is a tool for taking short notes.
It provides easy search and history view, categorization facilities (via tag system), simple storage format (single SQLite database file). See [tutorial](#tutorial) for more information

## Installation
tln is a Python package (Python 3.10+ is suggested), so it can be installed via `pip install`:
```bash
$ git clone https://github.com/artfadeev/tln
$ pip install ./tln
```

Once installed, you need to create a database:
```bash
$ tln init /path/to/tln.db 
Successfully initialized database at /path/to/tln.db!
Provide --db_path to use this database
```

To use this database, set `TLN_DB` environment variable, or pass it via `--db_path` option.
```bash
$ export TLN_DB=/path/to/tln.db # place this into ~/.bashrc or other shell config file
$ tln path # use this command to check where database is located 
/path/to/tln.db
$ tln --db_path /another/path/to/tln.db path # use another path
/another/path/to/tln.db
```

To enable bash tab-completion, add following command to `.bashrc` (see [click docs on shell completion](https://click.palletsprojects.com/en/latest/shell-completion/#enabling-completion) for instructions for other shells):
```bash
$ eval "$(_TLN_COMPLETE=bash_source TLN)"
```
Shell completion works for commands, option names and [concept references](#references). **Note:** shell completion always uses `TLN_DB` environment variable as path to the database; if it is not set, reference completion won't work.

## Tutorial
### Concepts
tln stores information about *concepts*. Each concept has an id (unique string), creation timestamp and a text label.
Use `tln add` to add concepts to the database. The only argument you must pass is label: timestamps and ids are generated automatically.
```bash
$ tln add "This is the first concept in the database"
$ tln add Quotes are not required, but remember to escape shell control characters.
$ tln add --editor "This label will be opened in editor before" # "... saving" is added in $EDITOR 
$ tln add --id manual_id "Ids can be specified manually"
```

To list entries from the database, use `tln list`:
```bash
$ tln list
                 [tag] tag
2024.03.02 16:13 This is the first concept in the database
           16:13 Quotes are not required, but remember to escape shell control characters.
           16:13 This label will be opened in editor before saving
           16:13 Ids can be specified manually
$ tln list "control characters" # search labels
2024.03.02 16:13 Quotes are not required, but remember to escape shell control characters.
```
Here you see all previously added concepts. The first line is for a automatically created `tag` concept, which we will discuss later.

### References
A `reference` is a string written using special syntax, which is used to pick a single concept from the database.
References are accepted everywhere where you need to point to a particular concept from the database.

For example, let's use `tln show` command, which displays all information about a concept.
In this example we use `/` reference — it refers to the concept with largest creation timestamp:
```bash
$ tln show /
manual_id
2024-03-02 16:13:37.966169

Ids can be specified manually
```

There are several kinds of references. Each kind consists of a prefix and an query (query was empty in the previous example).
See `tln show --help` for more info:
```bash
$ tln show --help
...
  Supported references:
  @ID                 find concept by id
  .MARK_NAME          resolve mark
  /prefix:TEXT        search by label prefix
  //TEXT              search by label substring (case-insensitive)
  /                   get latest concept
  QUERY               get concept by exact label match (case-insensitive)
...
```

### Marks
`Marks` are short text labels which point to concepts in the database. They can be created using `tln mark` command and referenced to using `.mark_name` reference:
```
$ tln mark //editor editor_usage # mark the concept containing substring "editor" with "editor_usage" mark
$ tln show .editor_usage # now you can use .editor_usage to refer to that note
5687a5cfb302
2024-03-02 16:13:37.914296

This label will be opened in editor before saving
```
Marks are somewhat similar to ids, but one concept may have many marks. This is useful for shorthands.

### Relations and tags
Two concepts may be connected via a relation. Currently, only `tagged` and `subtag_of` relations are supported.

Any concept can be a tag, although it's better to tag concepts which are used as tags with a special "tln/is_tag" (this is the id of the concept; it has label "tag") concept. Tagging can be done using `tln tag` command
```
$ tln add first_tag
$ tln tag first_tag @tln/is_tag # clarify that first_tag will be used for tagging
$ tln tag @manual_id first_tag # tag concept with id "manual_id" (last added note) with first_tag.
$ tln show @manual_id
manual_id
2024-03-02 16:13:37.966169

Ids can be specified manually

tagged: first_tag
```

You can set a tag to be a subtag of another tag using `tln relation` command. Here is an example:
```bash
$ # create tags
$ tln add vacation2015
$ tln add vacation2016
$ tln add tourism
$ tln relation vacation2015 subtag_of tourism
$ tln relation vacation2016 subtag_of tourism
$ # create concepts
$ tln add "In 2015, I visited Greece" && tln tag / vacation2015
$ tln add "I really liked Athens" && tln tag / vacation2015
$ tln add "In 2016, I visited Germany" && tln tag / vacation2016
$ # find concepts tagged by "tourism"
$ tln list -t tourism
2024.03.02 16:51 [vacation2015] In 2015, I visited Greece
           16:51 [vacation2015] I really liked Athens
           16:51 [vacation2016] In 2016, I visited Germany
$ # As you can see, although these three notes were not directly tagged by "tourism", they still show up.
```
