from collections import namedtuple

RuneasySettings = namedtuple(
    'RuneasySettings', 'init_dur prog_freq rest race max_dur')
IntervalSettings = namedtuple(
    'IntervalSettings', 'init_dur prog_freq rest race max_dur')
HillSettings = namedtuple(
    'HillSettings', 'init_dur prog_freq rest race max_dur')
TempoSettings = namedtuple(
    'TempoSettings', 'init_dur prog_freq rest race max_dur')
CrosstrainSettings = namedtuple(
    'CrosstrainSettings', 'init_dur prog_freq rest race max_dur')

PLANS = {
    "5k": {
        "Beginner": [
            [("runeasy", RuneasySettings(25, 3, 5, 5, 35))],
            [("interval", IntervalSettings(10, 1, 5, 5, 35)),
             ("hill", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 3, 5, 5, 35))]
        ],
        "Intermediate": [
            [("tempo", TempoSettings(10, 1, 5, 5, 35)),
             ("interval", IntervalSettings(10, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 9, 5, 10, 35))],
            [("hill", HillSettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(40, 3, 0, '50%', 55))]
        ],
        "Advanced": [
            [("tempo", TempoSettings(5, 1, 5, 5, 35)),
             ("interval", IntervalSettings(25, 1, 5, 5, 35))],
            [("crosstrain", CrosstrainSettings(30, 9, 5, 5, 35))],
            [("interval", IntervalSettings(10, 1, 5, 5, 35))],
            [("interval", IntervalSettings(10, 1, 5, 5, 35)),
             ("hill", HillSettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(65, 3, 10, '50%', 90))]
        ]
    },
    "10k": {
        "Beginner": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("interval", RuneasySettings(10, 1, 5, 5, 35)),
             ("hill", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Intermediate": [
            [("tempo", RuneasySettings(5, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("interval", RuneasySettings(10, 1, 5, 5, 35)),
             ("hill", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ],
        "Advanced": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("tempo", RuneasySettings(5, 1, 5, 5, 35))],
            [("crosstrain", CrosstrainSettings(30, 9, 5, 5, 35))],
            [("interval", IntervalSettings(10, 1, 5, 5, 35))],
            [("interval", RuneasySettings(10, 1, 5, 5, 35)),
             ("hill", RuneasySettings(25, 1, 5, 5, 35))],
            [("runeasy", RuneasySettings(30, 1, 5, 5, 35))]
        ]
    },
    "half": {
        "Beginner": [
            [("runeasy", RuneasySettings(5, 1, 5, 5, 35))],
            [("tempo", RuneasySettings(5, 1, 5, 5, 35))],
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
    "full": {
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
