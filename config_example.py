# rename to config.py
from util import init_custom_id
from sweet.io.fs import file_local_path


# `init_custom_id` produces a global, unique integer that
# can be used along with `incr_custom_id` to manage
# identifiers for custom NPCs, objects, spells, etc.
init_custom_id("npctext", 900000)
init_custom_id("creature_template", 50000) # MAX(entry) => 43282
init_custom_id("gameobject_template", 500000)
init_custom_id("quest_template", 30000)

# the following function returns the absolute path to a
# directory named 'scripts' next to this file. change it
# to reflect where your own scripts reside.
SCRIPT_PATH = file_local_path("trine-passive-scripts/", __file__)

# fairly obvious. replace any spaces in the passphrase with a '+'
SQLALCHEMY_DATABASE_URI = "mysql://username:password@localhost/db"
