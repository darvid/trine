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


class FactionTemplate(object):
    """Contains only IDs corresponding to a given faction name."""
    ACTOR_EVIL                        = 1684
    ACTOR_EVIL1                       = 1771
    ACTOR_EVIL2                       = 1902
    ACTOR_EVIL3                       = 1904
    ACTOR_EVIL4                       = 1958
    ACTOR_EVIL5                       = 1959
    ACTOR_EVIL6                       = 2088
    ACTOR_EVIL7                       = 2101
    ACTOR_EVIL8                       = 2102
    ACTOR_GOOD                        = 1683
    ACTOR_GOOD1                       = 1770
    ACTOR_GOOD2                       = 1934
    ACTOR_GOOD3                       = 1935
    ACTOR_GOOD4                       = 2115
    ACTOR_GOOD5                       = 2117
    ACTOR_GOOD6                       = 2176
    ACTOR_GOOD7                       = 2178
    ALLIANCE                          = 1802
    ALLIANCE1                         = 2142
    ALLIANCE_GENERIC                  = 84
    ALLIANCE_GENERIC1                 = 210
    ALLIANCE_GENERIC2                 = 534
    ALLIANCE_GENERIC3                 = 694
    ALLIANCE_GENERIC4                 = 1054
    ALLIANCE_GENERIC5                 = 1055
    ALLIANCE_GENERIC6                 = 1315
    ALLIANCE_GENERIC7                 = 1732
    ALLIANCE_GENERIC8                 = 1733
    ALLIANCE_GENERIC9                 = 1819
    AMBIENT                           = 188
    AMBIENT1                          = 190
    AMBIENT2                          = 1803
    AMBIENT3                          = 1804
    AMBIENT4                          = 1990
    AMBIENT5                          = 2028
    AMBIENT6                          = 2038
    AMBIENT7                          = 2106
    AMBIENT8                          = 2127
    AMBIENT9                          = 2136
    ARAKKOA                           = 1738
    ARAKKOA1                          = 1869
    ARCANE_ANNIHILATOR_DNR            = 1798
    ARGENT_CRUSADE                    = 2070
    ARGENT_CRUSADE1                   = 2071
    ARGENT_CRUSADE2                   = 2072
    ARGENT_CRUSADE3                   = 2073
    ARGENT_CRUSADE4                   = 2131
    ARGENT_CRUSADE5                   = 2134
    ARGENT_CRUSADE6                   = 2138
    ARGENT_CRUSADE7                   = 2230
    ARGENT_DAWN                       = 794
    ARGENT_DAWN1                      = 814
    ARGENT_DAWN2                      = 1624
    ARGENT_DAWN3                      = 1625
    ARGENT_DAWN4                      = 1766
    ARGENT_DAWN5                      = 1767
    ARGENT_DAWN6                      = 2086
    ARGENT_DAWN7                      = 2087
    ARMIES_OF_CTHUN                   = 370
    ASHTONGUE_DEATHSWORN              = 1820
    ASHTONGUE_DEATHSWORN1             = 1858
    ASHTONGUE_DEATHSWORN2             = 1866
    AZALOTH                           = 1834
    BASILISK                          = 49
    BASILISK1                         = 410
    BATTLEGROUND_NEUTRAL              = 1194
    BEAST_BAT                         = 411
    BEAST_BEAR                        = 44
    BEAST_BOAR                        = 1094
    BEAST_CARRION_BIRD                = 73
    BEAST_GORILLA                     = 72
    BEAST_RAPTOR                      = 48
    BEAST_RAPTOR1                     = 1909
    BEAST_SPIDER                      = 22
    BEAST_SPIDER1                     = 312
    BEAST_WOLF                        = 32
    BEAST_WOLF1                       = 38
    BEAST_WOLF2                       = 1815
    BLACKFATHOM                       = 128
    BLACKFATHOM1                      = 350
    BLADESPIRE_CLAN                   = 1780
    BLADESPIRE_CLAN1                  = 1782
    BLADESPIRE_CLAN2                  = 1784
    BLADESPIRE_CLAN3                  = 1790
    BLOODMAUL_CLAN                    = 1781
    BLOODMAUL_CLAN1                   = 1783
    BLOODMAUL_CLAN2                   = 1785
    BLOODMAUL_CLAN3                   = 1791
    BLOODSAIL_BUCCANEERS              = 119
    BLUE                              = 1621
    BLUE1                             = 1948
    BOOTY_BAY                         = 120
    BOOTY_BAY1                        = 121
    BOOTY_BAY2                        = 390
    BROKEN                            = 1679
    BROOD_OF_NOZDORMU                 = 776
    BROOD_OF_NOZDORMU1                = 1601
    BURNING_BLADE                     = 554
    CAVERNS_OF_TIME_DURNHOLDE         = 1748
    CAVERNS_OF_TIME_DURNHOLDE1        = 2074
    CAVERNS_OF_TIME_SOUTHSHORE_GUARDS = 1749
    CAVERNS_OF_TIME_THRALL            = 1747
    CENARION_CIRCLE                   = 635
    CENARION_CIRCLE1                  = 994
    CENARION_CIRCLE2                  = 996
    CENARION_CIRCLE3                  = 1254
    CENARION_CIRCLE4                  = 1608
    CENARION_EXPEDITION               = 1659
    CENARION_EXPEDITION1              = 1660
    CENARION_EXPEDITION2              = 1661
    CENARION_EXPEDITION3              = 1710
    CENARION_EXPEDITION4              = 1728
    CENARION_EXPEDITION5              = 1987
    CENTAUR_GALAK                     = 131
    CENTAUR_KOLKAR                    = 130
    CENTAUR_KOLKAR1                   = 655
    CHESS_ALLIANCE                    = 1688
    CHESS_ALLIANCE1                   = 1690
    CHESS_FRIENDLY_TO_ALL_CHESS       = 1852
    CHESS_HORDE                       = 1689
    CHESS_HORDE1                      = 1691
    COT_ARTHAS                        = 2076
    COT_ARTHAS1                       = 2077
    COT_ARTHAS2                       = 2079
    COT_SCOURGE                       = 2075
    COT_STRATHOLME_CITIZEN            = 2078
    CRAIGS_SQUIRRELS                  = 1936
    CRAIGS_SQUIRRELS1                 = 1937
    CRAIGS_SQUIRRELS10                = 1947
    CRAIGS_SQUIRRELS2                 = 1938
    CRAIGS_SQUIRRELS3                 = 1939
    CRAIGS_SQUIRRELS4                 = 1940
    CRAIGS_SQUIRRELS5                 = 1941
    CRAIGS_SQUIRRELS6                 = 1942
    CRAIGS_SQUIRRELS7                 = 1943
    CRAIGS_SQUIRRELS8                 = 1944
    CRAIGS_SQUIRRELS9                 = 1945
    CRAZED_OWLKIN                     = 1687
    CREATURE                          = 7
    CREATURE1                         = 15
    CREATURE10                        = 1917
    CREATURE2                         = 58
    CREATURE3                         = 189
    CREATURE4                         = 1274
    CREATURE5                         = 1275
    CREATURE6                         = 1606
    CREATURE7                         = 1607
    CREATURE8                         = 1886
    CREATURE9                         = 1887
    CTF_FLAG_ALLIANCE                 = 1913
    CTF_FLAG_ALLIANCE1                = 1995
    CTF_FLAG_ALLIANCE2                = 1997
    CTF_FLAG_ALLIANCE3                = 2236
    CTF_FLAG_HORDE                    = 2058
    CTF_FLAG_HORDE1                   = 2235
    CTF_FLAG_NEUTRAL                  = 2059
    DALARAN                           = 76
    DARKHOWL                          = 78
    DARKMOON_FAIRE                    = 1555
    DARKMOON_FAIRE1                   = 1896
    DARKSPEAR_TROLLS                  = 126
    DARKSPEAR_TROLLS1                 = 876
    DARKSPEAR_TROLLS2                 = 877
    DARK_IRON_DWARVES                 = 54
    DARK_IRON_DWARVES1                = 674
    DARK_IRON_DWARVES2                = 734
    DARK_IRON_DWARVES3                = 754
    DARK_PORTAL_ATTACKER_LEGION       = 1752
    DARK_PORTAL_ATTACKER_LEGION1      = 1753
    DARK_PORTAL_ATTACKER_LEGION2      = 1754
    DARK_PORTAL_DEFENDER_ALLIANCE     = 1755
    DARK_PORTAL_DEFENDER_ALLIANCE1    = 1756
    DARK_PORTAL_DEFENDER_ALLIANCE2    = 1757
    DARK_PORTAL_DEFENDER_HORDE        = 1758
    DARK_PORTAL_DEFENDER_HORDE1       = 1759
    DARK_PORTAL_DEFENDER_HORDE2       = 1760
    DARNASSUS                         = 79
    DARNASSUS1                        = 80
    DARNASSUS2                        = 124
    DARNASSUS3                        = 1076
    DARNASSUS4                        = 1097
    DARNASSUS5                        = 1594
    DARNASSUS6                        = 1600
    DARNASSUS7                        = 1951
    DEFIAS_BROTHERHOOD                = 17
    DEFIAS_BROTHERHOOD1               = 27
    DEFIAS_BROTHERHOOD2               = 34
    DEMON                             = 90
    DEMON1                            = 954
    DEMON2                            = 1768
    DEMON3                            = 1769
    DEMON4                            = 1786
    DEMON5                            = 1825
    DEMON6                            = 1963
    DRAGONFLIGHT_BLACK                = 103
    DRAGONFLIGHT_BLACK1               = 1394
    DRAGONFLIGHT_BLACK_BAIT           = 1114
    DRAGONFLIGHT_BRONZE               = 1605
    DRAGONFLIGHT_GREEN                = 50
    DRAGONFLIGHT_RED                  = 60
    DRAGONMAW_ENEMY                   = 1864
    EARTHEN                           = 2118
    EARTHEN_RING                      = 1725
    EARTHEN_RING1                     = 1726
    EARTHEN_RING2                     = 1727
    EARTH_ELEMENTAL                   = 1681
    ELEMENTAL                         = 91
    ELEMENTAL1                        = 834
    ELEMENTAL2                        = 1081
    ELEMENTAL3                        = 1680
    ELEMENTAL4                        = 1932
    ELEMENTAL_AIR                     = 2098
    ELEMENTAL_WATER                   = 2099
    ENEMY                             = 168
    ENEMY1                            = 1620
    ESCORTEE                          = 10
    ESCORTEE1                         = 33
    ESCORTEE10                        = 1986
    ESCORTEE11                        = 2046
    ESCORTEE2                         = 113
    ESCORTEE3                         = 231
    ESCORTEE4                         = 232
    ESCORTEE5                         = 250
    ESCORTEE6                         = 290
    ESCORTEE7                         = 495
    ESCORTEE8                         = 774
    ESCORTEE9                         = 775
    ETHEREUM                          = 1678
    ETHEREUM1                         = 1796
    ETHEREUM2                         = 1800
    ETHEREUM3                         = 1823
    ETHEREUM_SPARBUDDY                = 1799
    EVERLOOK                          = 854
    EVERLOOK1                         = 855
    EXODAR                            = 1638
    EXODAR1                           = 1639
    EXODAR10                          = 1700
    EXODAR2                           = 1640
    EXODAR3                           = 1646
    EXODAR4                           = 1647
    EXODAR5                           = 1654
    EXODAR6                           = 1655
    EXODAR7                           = 1694
    EXODAR8                           = 1698
    EXODAR9                           = 1699
    EXPLORERS_LEAGUE                  = 1926
    EXPLORERS_LEAGUE1                 = 1927
    FARSTRIDERS                       = 1627
    FARSTRIDERS1                      = 1636
    FARSTRIDERS2                      = 1637
    FEL_ORC                           = 1662
    FEL_ORC1                          = 1697
    FEL_ORC2                          = 1704
    FEL_ORC3                          = 1705
    FEL_ORC4                          = 1792
    FEL_ORC_GHOST                     = 1663
    FIGHTING_ROBOTS                   = 1682
    FIGHTING_VANITY_PET               = 1961
    FLAYER_HUNTER                     = 1840
    FORLORN_SPIRIT                    = 77
    FRENZY                            = 1878
    FRENZYHEART_TRIBE                 = 2060
    FRENZYHEART_TRIBE1                = 2061
    FRENZYHEART_TRIBE2                = 2062
    FREYA                             = 2081
    FRIENDLY                          = 35
    FRIENDLY1                         = 1080
    FRIENDLY10                        = 2135
    FRIENDLY11                        = 2137
    FRIENDLY12                        = 2140
    FRIENDLY13                        = 2141
    FRIENDLY2                         = 1774
    FRIENDLY3                         = 1806
    FRIENDLY4                         = 1812
    FRIENDLY5                         = 1816
    FRIENDLY6                         = 1857
    FRIENDLY7                         = 1933
    FRIENDLY8                         = 2036
    FRIENDLY9                         = 2110
    FRIENDLY_FORCE_REACTION           = 1971
    FROSTWOLF_CLAN                    = 1214
    FROSTWOLF_CLAN1                   = 1215
    FROSTWOLF_CLAN2                   = 1335
    FROSTWOLF_CLAN3                   = 1554
    FROSTWOLF_CLAN4                   = 1597
    FROST_VRYKUL                      = 2109
    FROST_VRYKUL1                     = 2113
    FROST_VRYKUL2                     = 2125
    FROST_VRYKUL3                     = 2126
    FROST_VRYKUL4                     = 2133
    FUNGAL_GIANT                      = 1706
    FURBOLG                           = 82
    FURBOLG_FROSTPAW                  = 2003
    FURBOLG_REDFANG                   = 2001
    FURBOLG_UNCORRUPTED               = 934
    GADGETZAN                         = 474
    GADGETZAN1                        = 475
    GELKIS_CLAN_CENTAUR               = 132
    GIANT                             = 778
    GIZLOCK                           = 1294
    GIZLOCKS_CHARM                    = 86
    GIZLOCKS_DUMMY                    = 52
    GNOLL_MOSSHIDE                    = 61
    GNOLL_MUDSNOUT                    = 95
    GNOLL_REDRIDGE                    = 19
    GNOLL_RIVERPAW                    = 20
    GNOLL_ROTHIDE                     = 70
    GNOLL_SHADOWHIDE                  = 39
    GNOMEREGAN_BUG                    = 494
    GNOMEREGAN_EXILES                 = 23
    GNOMEREGAN_EXILES1                = 64
    GNOMEREGAN_EXILES2                = 875
    GNOME_LEPER                       = 63
    GOBLIN_DARK_IRON_BAR_PATRON       = 735
    GOBLIN_DARK_IRON_BAR_PATRON1      = 736
    GRELL                             = 81
    GRIZZLY_HILLS_TRAPPER             = 2032
    HARPY                             = 514
    HATES_EVERYTHING                  = 2189
    HATES_EVERYTHING1                 = 2190
    HATES_EVERYTHING2                 = 2191
    HILLSBRAD_MILITIA                 = 88
    HILLSBRAD_SOUTHSHORE_MAYOR        = 96
    HOLIDAY_MONSTER                   = 1998
    HOLIDAY_WATER_BARREL              = 1952
    HONOR_HOLD                        = 1666
    HONOR_HOLD1                       = 1667
    HONOR_HOLD2                       = 1671
    HONOR_HOLD3                       = 1737
    HORDE                             = 1801
    HORDE_EXPEDITION                  = 1901
    HORDE_EXPEDITION1                 = 1918
    HORDE_GENERIC                     = 83
    HORDE_GENERIC1                    = 106
    HORDE_GENERIC10                   = 1835
    HORDE_GENERIC11                   = 2031
    HORDE_GENERIC2                    = 714
    HORDE_GENERIC3                    = 1034
    HORDE_GENERIC4                    = 1314
    HORDE_GENERIC5                    = 1494
    HORDE_GENERIC6                    = 1495
    HORDE_GENERIC7                    = 1496
    HORDE_GENERIC8                    = 1734
    HORDE_GENERIC9                    = 1735
    HUMAN_NIGHT_WATCH                 = 53
    HUMAN_NIGHT_WATCH1                = 56
    HYDRAXIAN_WATERLORDS              = 695
    HYJAL_DEFENDERS                   = 1716
    HYJAL_DEFENDERS1                  = 1717
    HYJAL_DEFENDERS2                  = 1718
    HYJAL_DEFENDERS3                  = 1719
    HYJAL_INVADERS                    = 1720
    HYLDSMEET                         = 2128
    INCITER_TRIGGER                   = 1761
    INCITER_TRIGGER1                  = 1762
    INCITER_TRIGGER2                  = 1763
    INCITER_TRIGGER3                  = 1764
    INCITER_TRIGGER4                  = 1765
    IRONFORGE                         = 55
    IRONFORGE1                        = 57
    IRONFORGE2                        = 122
    IRONFORGE3                        = 1611
    IRONFORGE4                        = 1618
    IRONFORGE5                        = 2155
    IRON_DWARVES                      = 1954
    IRON_DWARVES1                     = 1955
    IRON_GIANTS                       = 2108
    JAEDENAR                          = 1434
    KEEPERS_OF_TIME                   = 1779
    KHADGARS_SERVANT                  = 1773
    KIRINVAR_BELMARA                  = 1808
    KIRINVAR_COHLIEN                  = 1809
    KIRINVAR_DATHRIC                  = 1810
    KIRINVAR_LUMINRATH                = 1811
    KIRIN_TOR                         = 2006
    KIRIN_TOR1                        = 2007
    KIRIN_TOR2                        = 2008
    KIRIN_TOR3                        = 2009
    KNIGHTS_OF_THE_EBON_BLADE         = 2050
    KNIGHTS_OF_THE_EBON_BLADE1        = 2051
    KNIGHTS_OF_THE_EBON_BLADE2        = 2144
    KNIGHTS_OF_THE_EBON_BLADE3        = 2214
    KNIGHTS_OF_THE_EBON_BLADE4        = 2226
    KOBOLD                            = 25
    KOBOLD1                           = 26
    KURENAI                           = 1721
    KURENAI1                          = 1722
    KURENAI2                          = 1723
    KURENAI3                          = 1724
    KURZENS_MERCENARIES               = 46
    LEGION_COMMUNICATOR               = 1842
    LEOPARD                           = 66
    LEOTHERAS_DEMON_I                 = 1829
    LEOTHERAS_DEMON_II                = 1830
    LEOTHERAS_DEMON_III               = 1831
    LEOTHERAS_DEMON_IV                = 1832
    LEOTHERAS_DEMON_V                 = 1833
    LOST_ONES                         = 51
    LOWER_CITY                        = 1818
    LOWER_CITY1                       = 1851
    MAGRAM_CLAN_CENTAUR               = 133
    MAIEV                             = 1859
    MAIEV1                            = 1867
    MAIEV2                            = 1916
    MAKRURA                           = 129
    MANA_CREATURE                     = 1772
    MARAUDINE                         = 134
    MIGHT_OF_KALIMDOR                 = 777
    MIGHT_OF_KALIMDOR1                = 1613
    MONSTER                           = 14
    MONSTER1                          = 16
    MONSTER10                         = 1985
    MONSTER11                         = 1992
    MONSTER12                         = 2022
    MONSTER13                         = 2033
    MONSTER14                         = 2039
    MONSTER15                         = 2111
    MONSTER16                         = 2124
    MONSTER2                          = 93
    MONSTER3                          = 148
    MONSTER4                          = 634
    MONSTER5                          = 1614
    MONSTER6                          = 1751
    MONSTER7                          = 1787
    MONSTER8                          = 1925
    MONSTER9                          = 1970
    MONSTER_PREDATOR                  = 1711
    MONSTER_PREDATOR1                 = 1953
    MONSTER_PREDATOR2                 = 2029
    MONSTER_PREDATOR3                 = 2030
    MONSTER_PREDATOR4                 = 2156
    MONSTER_PREY                      = 1712
    MONSTER_PREY1                     = 1713
    MONSTER_PREY2                     = 1999
    MONSTER_PREY3                     = 2000
    MONSTER_REFEREE                   = 2119
    MONSTER_REFEREE1                  = 2120
    MONSTER_SPAR                      = 1692
    MONSTER_SPAR1                     = 1847
    MONSTER_SPAR2                     = 1965
    MONSTER_SPAR3                     = 1983
    MONSTER_SPAR4                     = 1993
    MONSTER_SPAR5                     = 2055
    MONSTER_SPAR6                     = 2104
    MONSTER_SPAR_BUDDY                = 1693
    MONSTER_SPAR_BUDDY1               = 1736
    MONSTER_SPAR_BUDDY2               = 1814
    MONSTER_SPAR_BUDDY3               = 1848
    MONSTER_SPAR_BUDDY4               = 1868
    MONSTER_SPAR_BUDDY5               = 1984
    MONSTER_SPAR_BUDDY6               = 1994
    MONSTER_SPAR_BUDDY7               = 2056
    MONSTER_SPAR_BUDDY8               = 2105
    MONSTER_SPAR_BUDDY9               = 2150
    MONSTER_ZONE_FORCE_REACTION       = 1924
    MONSTER_ZONE_FORCE_REACTION1      = 2057
    MOUNT_TAXI_ALLIANCE               = 2090
    MOUNT_TAXI_HORDE                  = 2091
    MOUNT_TAXI_NEUTRAL                = 2092
    MURLOC                            = 18
    MURLOC1                           = 1966
    MURLOC2                           = 1969
    MURLOC_WINTERFIN                  = 1968
    NAGA                              = 74
    NETHERGARDE_CARAVAN               = 208
    NETHERGARDE_CARAVAN1              = 209
    NETHERWING                        = 1824
    NETHERWING1                       = 1850
    NONE                              = 1665
    NORTHSEA_PIRATES                  = 1888
    OBJECT_FORCE_REACTION             = 1972
    OGRE                              = 45
    OGRE_CAPTAIN_KROMCRUSH            = 1374
    OGRILA                            = 1872
    OGRILA1                           = 1874
    ORC_BLACKROCK                     = 40
    ORC_DRAGONMAW                     = 62
    ORC_DRAGONMAW1                    = 1863
    ORC_DRAGONMAW2                    = 1865
    ORC_DRAGONMAW3                    = 1877
    ORC_DRAGONMAW4                    = 1880
    ORGRIMMAR                         = 29
    ORGRIMMAR1                        = 65
    ORGRIMMAR2                        = 85
    ORGRIMMAR3                        = 125
    ORGRIMMAR4                        = 1074
    ORGRIMMAR5                        = 1174
    ORGRIMMAR6                        = 1595
    ORGRIMMAR7                        = 1612
    ORGRIMMAR8                        = 1619
    PLAYER_BLOOD_ELF                  = 1610
    PLAYER_DRAENEI                    = 1629
    PLAYER_DWARF                      = 3
    PLAYER_GNOME                      = 115
    PLAYER_NIGHT_ELF                  = 4
    PLAYER_ORC                        = 2
    PLAYER_TAUREN                     = 6
    PLAYER_TROLL                      = 116
    PLAYER_UNDEAD                     = 5
    POACHER                           = 1989
    PREY                              = 31
    PROTECTORATE                      = 1794
    PROTECTORATE1                     = 1795
    PROTECTORATE2                     = 1797
    PROTECTORATE3                     = 1807
    QUILBOAR_BRISTLEBACK              = 111
    QUILBOAR_BRISTLEBACK1             = 112
    QUILBOAR_DEATHSHEAD               = 154
    QUILBOAR_RAZORFEN                 = 152
    QUILBOAR_RAZORFEN1                = 153
    QUILBOAR_RAZORMANE                = 109
    QUILBOAR_RAZORMANE1               = 110
    RAM_RACING_POWERUP_DND            = 1930
    RAM_RACING_TRAP_DND               = 1931
    RATCHET                           = 69
    RATCHET1                          = 637
    RAVENHOLDT                        = 471
    RAVENHOLDT1                       = 473
    RAVENSWOOD_ANCIENTS               = 1846
    RC_ENEMIES                        = 1617
    RC_OBJECTS                        = 1616
    RED                               = 1622
    REUSE                             = 2021
    ROCK_FLAYER                       = 1839
    ROCK_FLAYER1                      = 1873
    SCARLET_CRUSADE                   = 67
    SCARLET_CRUSADE1                  = 89
    SCARLET_CRUSADE2                  = 2089
    SCARLET_CRUSADE3                  = 2095
    SCARLET_CRUSADE4                  = 2096
    SCARLET_CRUSADE5                  = 2103
    SCORPID                           = 413
    SCOURGE_INVADERS                  = 1630
    SCOURGE_INVADERS1                 = 1634
    SCOURGE_INVADERS2                 = 2023
    SCOURGE_INVADERS3                 = 2048
    SCOURGE_INVADERS4                 = 2049
    SCOURGE_INVADERS5                 = 2139
    SCOURGE_INVADERS6                 = 2145
    SEARING_SPIDER                    = 575
    SERVANT_OF_ILLIDAN                = 1813
    SERVANT_OF_ILLIDAN1               = 1826
    SERVANT_OF_ILLIDAN2               = 1843
    SERVANT_OF_ILLIDAN3               = 1849
    SERVANT_OF_ILLIDAN4               = 1853
    SERVANT_OF_ILLIDAN5               = 1882
    SHADOWMOON_SHADE                  = 1841
    SHADOWSILK_POACHER                = 574
    SHADOW_COUNCIL_COVERT             = 1750
    SHATARI_SKYGUARD                  = 1856
    SHATARI_SKYGUARD1                 = 1870
    SHATTERED_SUN_OFFENSIVE           = 1956
    SHATTERED_SUN_OFFENSIVE1          = 1957
    SHATTERED_SUN_OFFENSIVE2          = 1960
    SHATTERED_SUN_OFFENSIVE3          = 1967
    SHATTERSPEAR_TROLLS               = 1014
    SHATTERSPEAR_TROLLS1              = 1015
    SHENDRALAR                        = 1354
    SHENDRALAR1                       = 1355
    SILITHID                          = 310
    SILITHID1                         = 311
    SILITHID_ATTACKERS                = 1395
    SILVERMOON_CITY                   = 1602
    SILVERMOON_CITY1                  = 1603
    SILVERMOON_CITY2                  = 1604
    SILVERMOON_CITY3                  = 1656
    SILVERMOON_CITY4                  = 1657
    SILVERMOON_CITY5                  = 1658
    SILVERMOON_CITY6                  = 1695
    SILVERMOON_CITY7                  = 1745
    SILVERMOON_CITY8                  = 2210
    SILVERMOON_REMNANT                = 371
    SILVERMOON_REMNANT1               = 1576
    SILVERWING_SENTINELS              = 1514
    SILVERWING_SENTINELS1             = 1642
    SKETTIS_ARAKKOA                   = 1862
    SKETTIS_ARAKKOA1                  = 1871
    SKETTIS_ARAKKOA2                  = 1881
    SKETTIS_SHADOWY_ARAKKOA           = 1860
    SKYGUARD_ENEMY                    = 1879
    SONS_OF_LOTHAR_GHOSTS             = 1664
    SOUTHSEA_FREEBOOTERS              = 230
    SPIRIT                            = 92
    SPIRITS_OF_SHADOWMOON             = 1821
    SPIRITS_OF_SHADOWMOON1            = 1822
    SPIRIT_GUIDE_ALLIANCE             = 1414
    SPIRIT_GUIDE_HORDE                = 1415
    SPOREGGAR                         = 1707
    SPOREGGAR1                        = 1708
    SPOREGGAR2                        = 1709
    SPOREGGAR3                        = 1837
    SPOTTED_GRYPHON                   = 1906
    STEAMWHEEDLE_CARTEL               = 1615
    STEAMWHEEDLE_CARTEL1              = 1635
    STILLPINE_FURBOLG                 = 1685
    STILLPINE_FURBOLG1                = 1686
    STORMPIKE_GUARD                   = 1216
    STORMPIKE_GUARD1                  = 1217
    STORMPIKE_GUARD2                  = 1334
    STORMPIKE_GUARD3                  = 1534
    STORMPIKE_GUARD4                  = 1596
    STORMWIND                         = 11
    STORMWIND1                        = 12
    STORMWIND2                        = 123
    STORMWIND3                        = 1078
    STORMWIND4                        = 1575
    SULFURON_FIRELORDS                = 1234
    SULFURON_FIRELORDS1               = 1235
    SULFURON_FIRELORDS2               = 1236
    SUNHAWKS                          = 1701
    SUNHAWKS1                         = 1702
    SUNHAWKS2                         = 1714
    SUNHAWKS3                         = 1789
    SUNHAWKS4                         = 1793
    SYNDICATE                         = 87
    SYNDICATE1                        = 97
    SYNDICATE2                        = 108
    SYNDICATE3                        = 472
    TAMED_PLAGUEHOUND                 = 1905
    TASKMASTER_FIZZULE                = 430
    TEST                              = 1915
    TEST_FACTION                      = 1672
    TEST_FACTION1                     = 1674
    TEST_FACTION2                     = 1675
    TEST_FACTION3                     = 1907
    TEST_FACTION4                     = 1908
    THERAMORE                         = 149
    THERAMORE1                        = 150
    THERAMORE2                        = 151
    THERAMORE3                        = 894
    THERAMORE4                        = 1075
    THERAMORE5                        = 1077
    THERAMORE6                        = 1096
    THERAMORE_DESERTER                = 1883
    THE_ALDOR                         = 1743
    THE_ALDOR1                        = 1776
    THE_ALDOR2                        = 1777
    THE_ALDOR3                        = 1805
    THE_ALDOR4                        = 1844
    THE_ALDOR5                        = 1854
    THE_ALDOR6                        = 1875
    THE_ASHEN_VERDICT                 = 2216
    THE_ASHEN_VERDICT1                = 2217
    THE_ASHEN_VERDICT2                = 2218
    THE_ASHEN_VERDICT3                = 2219
    THE_CONSORTIUM                    = 1730
    THE_CONSORTIUM1                   = 1731
    THE_CONSORTIUM2                   = 1788
    THE_CONSORTIUM3                   = 1836
    THE_DEFILERS                      = 412
    THE_DEFILERS1                     = 1598
    THE_HAND_OF_VENGEANCE             = 1897
    THE_HAND_OF_VENGEANCE1            = 1900
    THE_HAND_OF_VENGEANCE2            = 1928
    THE_HAND_OF_VENGEANCE3            = 1929
    THE_HAND_OF_VENGEANCE4            = 2024
    THE_KALUAK                        = 1949
    THE_KALUAK1                       = 1950
    THE_KALUAK2                       = 2047
    THE_KALUAK3                       = 2148
    THE_LEAGUE_OF_ARATHOR             = 1577
    THE_LEAGUE_OF_ARATHOR1            = 1599
    THE_MAGHAR                        = 1650
    THE_MAGHAR1                       = 1651
    THE_MAGHAR2                       = 1652
    THE_MAGHAR3                       = 1653
    THE_ORACLES                       = 2063
    THE_ORACLES1                      = 2064
    THE_ORACLES2                      = 2065
    THE_ORACLES3                      = 2066
    THE_SCALE_OF_THE_SANDS            = 1778
    THE_SCRYERS                       = 1744
    THE_SCRYERS1                      = 1746
    THE_SCRYERS2                      = 1838
    THE_SCRYERS3                      = 1845
    THE_SCRYERS4                      = 1855
    THE_SCRYERS5                      = 1876
    THE_SHATAR                        = 1741
    THE_SHATAR1                       = 1775
    THE_SILVER_COVENANT               = 2025
    THE_SILVER_COVENANT1              = 2026
    THE_SILVER_COVENANT2              = 2027
    THE_SILVER_COVENANT3              = 2130
    THE_SONS_OF_HODIR                 = 2107
    THE_SONS_OF_HODIR1                = 2112
    THE_SONS_OF_LOTHAR                = 1644
    THE_SONS_OF_LOTHAR1               = 1645
    THE_SONS_OF_LOTHAR2               = 1648
    THE_SONS_OF_LOTHAR3               = 1649
    THE_SUNREAVERS                    = 2121
    THE_SUNREAVERS1                   = 2122
    THE_SUNREAVERS2                   = 2123
    THE_SUNREAVERS3                   = 2129
    THE_TAUNKA                        = 1921
    THE_TAUNKA1                       = 1922
    THE_TAUNKA2                       = 1923
    THE_TAUNKA3                       = 2019
    THE_VIOLET_EYE                    = 1696
    THE_WYRMREST_ACCORD               = 2010
    THE_WYRMREST_ACCORD1              = 2011
    THE_WYRMREST_ACCORD2              = 2012
    THE_WYRMREST_ACCORD3              = 2013
    THE_WYRMREST_ACCORD4              = 2041
    THE_WYRMREST_ACCORD5              = 2067
    THORIUM_BROTHERHOOD               = 1474
    THORIUM_BROTHERHOOD1              = 1475
    THRALLMAR                         = 1668
    THRALLMAR1                        = 1669
    THRALLMAR2                        = 1670
    THRALLMAR3                        = 1729
    THUNDER_BLUFF                     = 104
    THUNDER_BLUFF1                    = 105
    THUNDER_BLUFF2                    = 995
    TIMBERMAW_HOLD                    = 414
    TIMBERMAW_HOLD1                   = 636
    TITAN                             = 415
    TITAN1                            = 416
    TITAN2                            = 470
    TOWOW_FLAG                        = 1673
    TOWOW_FLAG_TRIGGER_ALLIANCE_DND   = 1677
    TOWOW_FLAG_TRIGGER_HORDE_DND      = 1676
    TRAINING_DUMMY                    = 914
    TRAINING_DUMMY1                   = 1095
    TRAINING_DUMMY2                   = 1703
    TRANQUILLIEN                      = 1623
    TRANQUILLIEN1                     = 1628
    TREANT                            = 1828
    TREASURE                          = 94
    TREASURE1                         = 100
    TREASURE2                         = 101
    TREASURE3                         = 102
    TREASURE4                         = 114
    TREASURE5                         = 1375
    TROGG                             = 36
    TROGG1                            = 59
    TROGG2                            = 594
    TROLL_AMANI                       = 1890
    TROLL_BLOODSCALP                  = 28
    TROLL_DRAKKARI                    = 2069
    TROLL_FOREST                      = 1643
    TROLL_FROSTMANE                   = 37
    TROLL_FROSTMANE1                  = 107
    TROLL_SKULLSPLITTER               = 30
    TROLL_VILEBRANCH                  = 795
    TROLL_WITHERBARK                  = 654
    TUSKARR                           = 1884
    UNDEAD_SCOURGE                    = 21
    UNDEAD_SCOURGE1                   = 233
    UNDEAD_SCOURGE10                  = 2005
    UNDEAD_SCOURGE11                  = 2018
    UNDEAD_SCOURGE12                  = 2035
    UNDEAD_SCOURGE13                  = 2042
    UNDEAD_SCOURGE14                  = 2043
    UNDEAD_SCOURGE15                  = 2068
    UNDEAD_SCOURGE16                  = 2080
    UNDEAD_SCOURGE17                  = 2082
    UNDEAD_SCOURGE18                  = 2083
    UNDEAD_SCOURGE19                  = 2084
    UNDEAD_SCOURGE2                   = 974
    UNDEAD_SCOURGE20                  = 2085
    UNDEAD_SCOURGE21                  = 2093
    UNDEAD_SCOURGE22                  = 2094
    UNDEAD_SCOURGE23                  = 2097
    UNDEAD_SCOURGE24                  = 2100
    UNDEAD_SCOURGE25                  = 2209
    UNDEAD_SCOURGE26                  = 2212
    UNDEAD_SCOURGE3                   = 1626
    UNDEAD_SCOURGE4                   = 1962
    UNDEAD_SCOURGE5                   = 1964
    UNDEAD_SCOURGE6                   = 1975
    UNDEAD_SCOURGE7                   = 1982
    UNDEAD_SCOURGE8                   = 1988
    UNDEAD_SCOURGE9                   = 1991
    UNDERCITY                         = 68
    UNDERCITY1                        = 71
    UNDERCITY2                        = 98
    UNDERCITY3                        = 118
    UNDERCITY4                        = 1134
    UNDERCITY5                        = 1154
    UNUSED                            = 1889
    VALGARDE_COMBATANT                = 1920
    VALIANCE_EXPEDITION               = 1891
    VALIANCE_EXPEDITION1              = 1892
    VALIANCE_EXPEDITION10             = 2037
    VALIANCE_EXPEDITION11             = 2040
    VALIANCE_EXPEDITION12             = 2044
    VALIANCE_EXPEDITION13             = 2143
    VALIANCE_EXPEDITION2              = 1893
    VALIANCE_EXPEDITION3              = 1898
    VALIANCE_EXPEDITION4              = 1899
    VALIANCE_EXPEDITION5              = 1973
    VALIANCE_EXPEDITION6              = 1974
    VALIANCE_EXPEDITION7              = 1976
    VALIANCE_EXPEDITION8              = 1977
    VALIANCE_EXPEDITION9              = 2004
    VENTURE_COMPANY                   = 47
    VICTIM                            = 42
    VICTIM1                           = 99
    VICTIM2                           = 614
    VICTIM3                           = 1454
    VILLIAN                           = 41
    VILLIAN1                          = 43
    VILLIAN2                          = 127
    VOID_ANOMALY                      = 1715
    VRYKUL                            = 1885
    VRYKUL1                           = 1894
    VRYKUL2                           = 1895
    VRYKUL3                           = 1914
    VRYKUL4                           = 2114
    VRYKUL5                           = 2116
    VRYKUL_ANCIENT_SIPRIT             = 1911
    VRYKUL_ANCIENT_SIPRIT1            = 1912
    VRYKUL_ANCIENT_SPIRIT             = 1910
    VRYKUL_GLADIATOR                  = 1919
    WAILING_CAVERNS                   = 270
    WAILING_CAVERNS1                  = 330
    WAILING_CAVERNS2                  = 450
    WARSONG_OFFENSIVE                 = 1978
    WARSONG_OFFENSIVE1                = 1979
    WARSONG_OFFENSIVE2                = 1980
    WARSONG_OFFENSIVE3                = 1981
    WARSONG_OFFENSIVE4                = 2020
    WARSONG_OFFENSIVE5                = 2034
    WARSONG_OFFENSIVE6                = 2045
    WARSONG_OFFENSIVE7                = 2132
    WARSONG_OUTRIDERS                 = 1515
    WARSONG_OUTRIDERS1                = 1641
    WINTERSABER_TRAINERS              = 874
    WORGEN                            = 24
    WRATHGATE_ALLIANCE                = 2053
    WRATHGATE_HORDE                   = 2054
    WRATHGATE_SCOURGE                 = 2052
    WYRMCULT                          = 1827
    ZANDALAR_TRIBE                    = 1574
    ZANGARMARSH_BANNER_ALLIANCE       = 1739
    ZANGARMARSH_BANNER_HORDE          = 1740
    ZANGARMARSH_BANNER_NEUTRAL        = 1742


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

    NON_EQUIPABLE   = 0
    HEAD            = 1
    NECK            = 2
    SHOULDERS       = 3
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


class TrainerType(object):

    CLASS       = 0
    MOUNTS      = 1
    TRADESKILLS = 2
    PETS        = 3


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