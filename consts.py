from datetime import date, datetime

#these are numbers that are rounded from the general trends found in paimon.moe
PROB_FIVE_STAR_AT_WISH_NUM_CHARACTERS = {74: .06, 75: .12, 76: .18, 77: .24, 78: .3, 79: .35, 80: .4, 81: .45, 82: .5, 83: .55, 84: .6, 85: .65, 86: .65, 87: .5, 88: .5, 89: .25, 90: 1}
#https://paimon.moe/wish/tally?id=400029
PROB_FIVE_STAR_AT_WISH_NUM_WEAPONS = {63: 0.08, 64: 0.15, 65: 0.22, 66: 0.28, 67: 0.36, 68: 0.42, 69: 0.5, 70: 0.56, 71: 0.6, 72: 0.67, 73: 0.71, 74: 0.47,75: 0.33, 76: 0.22, 77: 0.14, 78: 0.16, 79: 0.01, 80: 1}
STANDARD_FIVE_STAR_CHARACTERS = ["Jean", "Diluc", "Qiqi", "Mona", "Keqing"]
STANDARD_FIVE_STAR_WEAPONS = ["Amos\' Bow","Lost Prayer to the Sacred Winds","Primordial Jade Winged-Spear","Wolf\'s Gravestone","Aquila Favonia","Skyward Harp","Skyward Spine","Skyward Atlas","Skyward Pride","Skyward Blade"]
FOUR_STAR_CHARACTERS = ["Barbara", "Beidou", "Bennett", "Chongyun", "Diona", "Fischl", "Gorou", "Kujou Sara", "Ningguang", "Noelle", "Razor", "Rosaria", "Sayu", "Sucrose", "Thoma","Xiangling", "Xingqiu", "Xinyan", "Yanfei", "Yun Jin"]
FOUR_STAR_WEAPONS = ["Dragon's Bane","Eye of Perception","Favonius Codex","Favonius Greatsword","Favonius Lance","Favonius Sword","Favonius Warbow","Lion's Roar","Rainslasher","Rust","Sacrificial Bow","Sacrificial Fragments","Sacrificial Greatsword","Sacrificial Sword","The Bell","The Flute","The Stringless","The Widsith"    ]
STANDARD_FOUR_STARS = ["Amber", "Kaeya", "Lisa"]
#currently supported ones
BANNER_TYPES = {"character": ["character", "Character", "c", "C"], "weapon": ["Weapon", "weapon", "W", "w"]}

TIMER_FOLDER = 'timer_files/'
PRIMO_RECORD_FOLDER = 'primo_record_files/'
PERCENTAGE_BREAKDOWN_FOLDER = 'percentage_breakdown_files/'

YES_RESPONSES = ["Yes", "yes", "y", "Y", "true", "True"]
NO_RESPONSES = ["No", "no", "n", "N", "false", "False"]

INDENT =  "    "
 # default 80 is arbitrarily selected by me
UNIVERSAL_FORMAT_LENGTH = 80