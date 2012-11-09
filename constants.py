"""Contains data mostly retrieved from DBC files."""
from sweet.structures.dict import AttrDict


CLASS_NAMES = (
    "Warrior", 
    "Paladin", 
    "Hunter", 
    "Rogue", 
    "Priest", 
    "Death Knight",
    "Shaman", 
    "Mage", 
    "Warlock", 
    "Druid"
)
_a = AttrDict


def _repr(inst):
    return "<{0}('{1}')>".format(inst.__class__.__name__,
        getattr(inst, "display_name", "Unknown"))


class Class(AttrDict):
    def __repr__(self):
        return _repr(self)


class Race(AttrDict):
    def __repr__(self):
        return _repr(self)


class ChrClasses(object):

    WARRIOR = Class(display_name="Warrior", binary=1,      id=1)
    PALADIN = Class(display_name="Paladin", binary=2 << 0, id=2)
    HUNTER  = Class(display_name="Hunter",  binary=2 << 1, id=3)
    ROGUE   = Class(display_name="Rogue",   binary=2 << 2, id=4)
    PRIEST  = Class(display_name="Priest",  binary=2 << 3, id=5)
    DEATH_KNIGHT = DK = Class(display_name="Death Knight", binary=2 << 4, id=6)
    SHAMAN  = Class(display_name="Shaman",  binary=2 << 5, id=7)
    MAGE    = Class(display_name="Mage",    binary=2 << 6, id=8)
    WARLOCK = Class(display_name="Warlock", binary=2 << 7, id=9)
    DRUID   = Class(display_name="Druid",   binary=2 << 9, id=11)

    ALL = (WARRIOR, PALADIN, HUNTER, ROGUE, PRIEST, DEATH_KNIGHT, SHAMAN, MAGE,
        WARLOCK, DRUID)

    @classmethod
    def find_class(cls, value, method="id"):
        for class_ in cls.ALL:
            if class_[method] == value:
                return class_


class ChrRaces(object):

    HUMAN     = Race(display_name="Human",     binary=1, id=1)
    ORC       = Race(display_name="Orc",       binary=2 << 0, id=2)
    DWARF     = Race(display_name="Dwarf",     binary=2 << 1, id=3)
    NIGHT_ELF = Race(display_name="Night Elf", binary=2 << 2, id=4)
    UNDEAD    = Race(display_name="Undead",    binary=2 << 3, id=5)
    TAUREN    = Race(display_name="Tauren",    binary=2 << 4, id=6)
    GNOME     = Race(display_name="Gnome",     binary=2 << 5, id=7)
    TROLL     = Race(display_name="Troll",     binary=2 << 6, id=8)
    GOBLIN    = Race(display_name="Goblin",    binary=2 << 7, id=9)
    BLOOD_ELF = Race(display_name="Blood Elf", binary=2 << 8, id=10)
    DRAENEI   = Race(display_name="Draenei",   binary=2 << 9, id=11)
    FEL_ORC   = Race(display_name="Fel Orc",   binary=2 << 10, id=12)
    NAGA      = Race(display_name="Naga",      binary=2 << 11, id=13)
    BROKEN    = Race(display_name="Broken",    binary=2 << 12, id=14)
    SKELETON  = Race(display_name="Skeleton",  binary=2 << 13, id=15)
    VRYKUL    = Race(display_name="Vrykul",    binary=2 << 14, id=16)
    TUSKARR   = Race(display_name="Tuskarr",   binary=2 << 15, id=17)
    FOREST_TROLL = Race(display_name="Forest Troll", binary=2 << 16, id=18)
    TAUNKA    = Race(display_name="Taunka",    binary=2 << 17, id=19)
    NORTHREND_SKELETON = Race(display_name="Northrend Skeleton", 
                                             binary=2 << 18, id=20)
    ICE_TROLL = Race(display_name="Ice Troll", binary=2 << 19, id=21)

    ALL = (HUMAN, ORC, DWARF, NIGHT_ELF, UNDEAD, TAUREN, GNOME, TROLL, GOBLIN,
        BLOOD_ELF, DRAENEI, FEL_ORC, NAGA, BROKEN, SKELETON, VRYKUL, TUSKARR,
        FOREST_TROLL, TAUNKA, NORTHREND_SKELETON, ICE_TROLL)
    PLAYABLE = (HUMAN, ORC, DWARF, NIGHT_ELF, UNDEAD, TAUREN, GNOME, TROLL, 
        BLOOD_ELF, DRAENEI)
    ALLIANCE = (HUMAN, DWARF, GNOME, NIGHT_ELF, DRAENEI)
    HORDE = (ORC, UNDEAD, TAUREN, TROLL, BLOOD_ELF)

    @classmethod
    def find_race(cls, value, method="id"):
        for class_ in cls.ALL:
            if class_[method] == value:
                return class_


CLASS_RACE_COMBOS = {
    ChrRaces.HUMAN.id: (
        ChrClasses.WARRIOR, ChrClasses.PALADIN, ChrClasses.ROGUE,
        ChrClasses.PRIEST, ChrClasses.MAGE, ChrClasses.WARLOCK, 
        ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.DWARF.id: (
        ChrClasses.WARRIOR, ChrClasses.PALADIN, ChrClasses.HUNTER,
        ChrClasses.ROGUE, ChrClasses.PRIEST, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.NIGHT_ELF.id: (
        ChrClasses.WARRIOR, ChrClasses.HUNTER, ChrClasses.ROGUE, 
        ChrClasses.PRIEST, ChrClasses.DRUID, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.GNOME.id: (
        ChrClasses.WARRIOR, ChrClasses.ROGUE, ChrClasses.MAGE,
        ChrClasses.WARLOCK, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.DRAENEI.id: (
        ChrClasses.WARRIOR, ChrClasses.PALADIN, ChrClasses.HUNTER,
        ChrClasses.PRIEST, ChrClasses.SHAMAN, ChrClasses.MAGE,
        ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.ORC.id: (
        ChrClasses.WARRIOR, ChrClasses.HUNTER, ChrClasses.ROGUE, 
        ChrClasses.SHAMAN, ChrClasses.WARLOCK, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.UNDEAD.id: (
        ChrClasses.WARRIOR, ChrClasses.ROGUE, ChrClasses.PRIEST,
        ChrClasses.MAGE, ChrClasses.WARLOCK, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.TAUREN.id: (
        ChrClasses.WARRIOR, ChrClasses.HUNTER, ChrClasses.SHAMAN,
        ChrClasses.DRUID, ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.TROLL.id: (
        ChrClasses.WARRIOR, ChrClasses.HUNTER, ChrClasses.ROGUE,
        ChrClasses.PRIEST, ChrClasses.SHAMAN, ChrClasses.MAGE,
        ChrClasses.DEATH_KNIGHT
    ),
    ChrRaces.BLOOD_ELF.id: (
        ChrClasses.WARRIOR, ChrClasses.PALADIN, ChrClasses.HUNTER,
        ChrClasses.ROGUE, ChrClasses.PRIEST, ChrClasses.MAGE,
        ChrClasses.WARLOCK, ChrClasses.DEATH_KNIGHT
    ),
}


class NpcFlag(object):

    GOSSIP             = 1
    QUEST_GIVER        = 2 << 0
    TRAINER            = 2 << 3
    CLASS_TRAINER      = 2 << 4
    PROFESSION_TRAINER = 2 << 5
    VENDOR             = 2 << 6
    AMMO_VENDOR        = 2 << 7
    FOOD_VENDOR        = 2 << 8
    POISON_VENDOR      = 2 << 9
    REAGENT_VENDOR     = 2 << 10
    REPAIRER           = 2 << 11
    FLIGHT_MASTER      = 2 << 12
    SPIRIT_HEALER      = 2 << 13
    SPIRIT_GUIDE       = 2 << 14
    INNKEEPER          = 2 << 15
    BANKER             = 2 << 16
    PETITIONER         = 2 << 17
    TABARD_DESIGNER    = 2 << 18
    BATTLEMASTER       = 2 << 19
    AUCTIONEER         = 2 << 20
    STABLE_MASTER      = 2 << 21
    GUILD_BANKER       = 2 << 22
    SPELLCLICK         = 2 << 23
    MAILBOX            = 2 << 25


class InventoryType(object):

    NON_EQUIPABLE = 0
    HEAD            = 1
    NECK            = 2
    SHOULDER        = 3
    SHIRT           = 4
    CHEST           = 5
    WAIST           = 6
    LEGS            = 7
    FEET            = 8
    WRISTS          = 9
    HANDS           = 10
    FINGER          = 11
    TRINKET         = 12
    WEAPON          = 13
    SHIELD          = 14
    RANGED_WEAPON   = RANGED = 15
    BACK            = 16
    TWO_HAND_WEAPON = TWO_HAND = 17
    BAG             = 18
    TABARD          = 19
    ROBE            = 20
    MAIN_HAND_WEAPON = MAIN_HAND = 21
    OFF_HAND_WEAPON = OFF_HAND = 22
    HOLDABLE        = TOME = 23
    AMMO            = 24
    THROWN          = 25
    RANGED_RIGHT    = 26
    QUIVER          = 27
    RELIC           = 28


class Trainer(object):

    TYPE_CLASS       = 0
    TYPE_MOUNTS      = 1
    TYPE_TRADESKILLS = 2
    TYPE_PETS        = 3


META_GEM_NAMES = (
    [i + " Earthsiege Diamond" for i in [
        "Austere", "Beaming", "Bracing", "Eternal", "Insightful",
        "Invigorating", "Persistent", "Powerful", "Relentless", 
        "Trenchant"
    ]] +
    [i + " Skyflare Diamond" for i in [
        "Chaotic", "Destructive", "Ember", "Enigmatic", "Effulgent", "Forlorn", 
        "Impassive", "Revitalizing", "Swift", "Thundering", "Tireless"
    ]]
)
HIGH_LEVEL_GEM_NAMES = (
    META_GEM_NAMES +
    [i + " Cardinal Ruby" for i in [
        "Bold", "Bright", "Delicate", "Flashing", "Fractured", 
        "Precise", "Runed", "Subtle"
    ]] +
    [i + " Ametrine" for i in [
        "Accurate", "Champion's", "Deadly", "Deft", "Durable",
        "Empowered", "Etched", "Fierce", "Glimmering", "Glinting",
        "Inscribed", "Lucent", "Luminous", "Potent", "Pristine", 
        "Resolute", "Resplendent", "Stalwart", "Stark", "Veiled", 
        "Wicked", "Reckless"
    ]] +
    [i + " King's Amber" for i in [
        "Brilliant", "Mystic", "Quick", "Rigid", "Smooth", "Thick"
    ]] + 
    [i + " Eye of Zul" for i in [
        "Dazzling", "Enduring", "Energized", "Forceful", "Intricate",
        "Jagged", "Lambent", "Misty", "Opaque", "Radiant", "Seer's", 
        "Shattered", "Shining", "Steady", "Sundered", "Tense", 
        "Timeless", "Turbid", "Vivid"
    ]] +
    [i + " Majestic Zircon" for i in [
        "Lustrous", "Solid", "Stormy", "Sparkling"
    ]] +
    [i + " Dreadstone" for i in [
        "Balanced", "Defender's", "Glowing", "Guardian's", "Infused",
        "Mysterious", "Puissant", "Purified", "Regal", "Royal",
        "Sovereign", "Tenuous", "Shifting"
    ]] + 
    [i + " Dragon's Eye" for i in [
        # Red
        "Bold", "Bright", "Delicate", "Flashing", "Fractured", 
        "Precise", "Runed", "Subtle", 

        # Yellow
        "Brilliant", "Mystic", "Quick", "Rigid", "Smooth", "Thick", 

        # Blue
        "Lustrous", "Solid", "Sparkling", "Stormy"
    ]] +
    ["Nightmare Tear"]
)