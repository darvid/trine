# trine: translating english to DML since 2012

*Trine* is a utility for World of Warcraft emulators (e.g. TrinityCore) that
uses YAML as a DML (data manipulation language) to interface with the emulator
database.

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
to do something trivial like creating and populating a vendor.

```yaml
CreatureTemplate:
  - method: update
    where:
        name: Druid Trainer
    subname:
    npcflag: [GOSSIP, TRAINER, VENDOR]
    items: !query
        model: ItemTemplate
        what: entry
        where:
            name: Glyph of %
            AllowableClass: DRUID
```

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
      operation             [clean|execute|dml]

    optional arguments:
      -h, --help            show this help message and exit
      -w [PATH], --working-directory [PATH]
                            specify path to YAML documents

## Working directories

*Working directories* are simply folders with a `config.yml` and any number of
*trine* schema files (`*.yml`). They serve no other purpose other than keeping
your files organized.

By default, trine looks for `.yml` files in `~/.trine/` - but you can specify a
different working directory with the `-w` option.