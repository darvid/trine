trine
=====

This library provides a very rudimentary, but highly convenient interface 
between Python scripts and the database(s) of TrinityCore, or other World of
Warcraft emulators. 

The main purpose for a project like this is to simplify the often daunting task
of building the long and unreadable, if not complex queries used to create 
custom NPCs, create objects, populate vendors, and so on.

Requirements
------------

* [Python](http://python.org), version 2.6 or greater
* [SQLAlchemy](http://sqlalchemy.org), a popular ORM for Python
* [sweet](http://github.com/darvid/sweet)

[AutoCode](http://code.google.com/p/sqlautocode/) is an optional dependency that
is highly recommended if you want to extend this library in any way. It was used
to generate the model classes for TrinityCore's **world** database. 

The only wrinkle is that it does not validate field names to prevent the usage 
of Python reserved keywords, so you will have to manually find and replace all 
instances of *class*, for instance, which is used as the column name for 
numerous TrinityCore tables.

Usage
-----

After editing the example configuration file **config.py** to your liking,
add some scripts of your own and then run the *generate* script like so:

    $ ./generate.py <script name> [merge|clean]

Be aware that trine currently does not restrict naming for commands (e.g. merge),
so as long as you provide valid callables you can create scripts containing any
number of actions.

Examples
--------

For examples of what you can do with trine, see [trine-passive-scripts][tps].

[tps]: http://github.com/darvid/trine-passive-scripts/