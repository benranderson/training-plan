from collections import namedtuple

RuneasySettings = namedtuple(
    'RuneasySettings', 'init_dur prog_freq rest race max_dur')
IntervalSettings = namedtuple(
    'IntervalSettings', 'init_dur prog_freq rest race max_dur')

PLANS = {
    "5k": {
        "Beginner": [
            [("runeasy", RuneasySettings(25, 3, 5, 5, 35))],
            [("interval", RuneasySettings(10, 1, 5, 5, 35)),
             ("hillsprint", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 3, 5, 5, 35))]
        ],
        "Intermediate": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Advanced": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ]
    },
    "10k": {
        "Beginner": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Intermediate": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Advanced": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ]
    },
    "Half": {
        "Beginner": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Intermediate": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Advanced": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ]
    },
    "Full": {
        "Beginner": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Intermediate": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Advanced": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(10, 1, 5, 5, 35)),
             ("interval", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ]
    }
}
