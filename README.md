# trine: translating english to DML since 2012

*Trine* is a utility for World of Warcraft emulators (e.g. TrinityCore) that
uses [YAML](http://yaml.org/) as a DML (data manipulation language) to
interface with an emulator's database(s).

## Why use trine?

Let's say you want to combine glyph vendors with class trainers. A worthy cause,
but a rather tedious one. Without trine, your options are pretty limited:

* You can do everything in-game, using GM commands to manually look up and
  add items to your vendors. If you screw up during this process, or the
  vendor gets deleted, you have to start from scratch.
* You can manually write the SQL required to create the vendor, lookup the
  flags required for a combined vendor/trainer, and lookup the item IDs for
  all glyphs for a particular class, and then create the associated row in
  the `npc_vendor` table for each glyph to be sold.

With *trine*, you can forget about looking up flags and item IDs everytime you want
to do something trivial like creating and populating a vendor. The following YAML
document takes an existing NPC by the name of *"Druid Trainer"*, flags it both as
a class trainer and vendor, and populates the `npc_vendor` table with Druid-only
glyphs related to the vendor:

```yaml
npc:
  - method: UPDATE
    where:
        name: Druid Trainer
    subname:
    npcflag: [GOSSIP, TRAINER, VENDOR]
    items: !query
        model: item
        what: entry
        where:
            name: Glyph of %
            AllowableClass: DRUID
```

*Trine* comes with a small subset of named flags and identifiers obtained from
`.dbc` files (in English only for now, unfortunately). These [constants][const_py]
allow for the use of human friendly identifiers such as `DRUID` rather than `11`.

# Requirements

* [Python](http://python.org), version 2.6 or greater
* [PyYAML](http://pyyaml.org/)
* [SQLAlchemy](http://sqlalchemy.org)
* [schema](https://github.com/halst/schema)
* [sweet](http://github.com/darvid/sweet)
* An up-to-date [TrinityCore](http://www.trinitycore.org/) database.

[AutoCode](http://code.google.com/p/sqlautocode/) is an optional dependency that
is highly recommended if you want to extend this library in any way. It was used
to generate the model classes for TrinityCore's **world** database.

The only wrinkle is that it does not validate field names to prevent the use of
Python reserved keywords as column names, so you will have to manually find and
replace all instances of *class*, for instance, which is used as the column name
for numerous TrinityCore tables.

# Configuration

Save the following in the working directory (specified by `-w`) or `~/.trine/` as
`config.yml`.

```yaml
db:
    type: mysql
    username: trinity
    password: password
    host: localhost
    world_db: world
```

# Usage

    usage: trine [-h] [-w [PATH]] spec [operation]

    positional arguments:
      spec                  name of spec or 'all'
      operation             [execute|dml]

    optional arguments:
      -h, --help            show this help message and exit
      -w [PATH], --working-wdirectory [PATH]
                            specify path to YAML documents

## Working directories

*Working directories* are simply folders with a `config.yml` and any number of
*trine* schema files (`*.yml`). They serve no other purpose other than keeping
your files organized.

By default, trine looks for `.yml` files in `~/.trine/` - but you can specify a
different working directory with the `-w` option.

## Operations

*Trine* supports two main operations:

* **execute** - executes and commits all changes made by given schema files to
  the database.
* **dml** - outputs generated SQL queries to standard output, but does not
  execute any queries.

# Schema Structure

*Trine* expects a mapping of mappings representing model (table) names and their
respective schemas. This forces the user to organize schemas by model name. For
example:

```yaml
--- # item prices
item:
  - method: UPDATE
    where:
        name: Glyph of %
    SellPrice: 0
  - method: UPDATE
    where:
      name: Black Jelly
    SellPrice: 100
```

## Methods

Rather than use verbs such as in SQL (`SELECT`, `INSERT`, `UPDATE`), *Trine* uses
*"methods"* that are indicative of commonly used operations when manipulating
emulator databases.

### UPDATE

This method expects a `where` mapping and issues a SQL `UPDATE` based on the rest
of the schema mapping.

### MERGE

This method expects a `merge-from` key that is either the `entry` of another row
from the same table as the current schema, or a `where` mapping. **MERGE** is
particularly useful for custom NPCs or items, as it simplifies both the process
of creating them as well as updating them.

## Documents

Each YAML file can contain any number of documents, which are delimited by three
dashes (`---`). Currently, documents do not have any special purpose in *Trine*
other than providing a means of organization.

[const_py]: https://github.com/darvid/trine/blob/master/trine/constants.py