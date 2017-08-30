
from datetime import date, timedelta
import types

from collections import namedtuple

RuneasySettings = namedtuple(
    'RuneasySettings', 'init_dur prog_freq rest race max_dur')
IntervalSettings = namedtuple(
    'IntervalSettings', 'init_dur prog_freq rest race max_dur')

PLANS = {
    "5k": {
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


def determine_next_weekday(now, weekday):
    '''
    datetime, int -> datetime
    '''
    days_ahead = weekday - now.weekday() + 7
    return now + timedelta(days_ahead)

def week_type(week, length):
    if wk == (length - 1):
        return 'race'
    elif rest_week(week, length):
        return 'rest'
    else:
        return 'prog'

def rest_week(week, plan_length):
    '''
    int -> boolean

    Determine if current week is a rest week.

    Plans work on a 4 week block, with every 4th week being an easier week.
    Runner has at least 2 weeks, and a maximum of 5 weeks before they get an
    easier week.  So if they were on a 6 week plan they would only have an
    easier week on race week.

    Returns True if rest week and False if progression week.
    '''
    build_up = plan_length % 4
    if week <= build_up and build_up < 3:
        return False
    elif (week - build_up + 1) % 4 == 0:
        return True
    else:
        return False

def rest_pc_or_abs(week_cut, dur):
    '''
    Return rest week duration based on whether rest duration reduction is applied as an absolute
    or % value
    '''
    if isinstance(week_cut, str):
        return (float(week_cut.strip('%')) / 100) * dur
    else:
        return dur - week_cut

class Exercise:

    def __init__(self, description, duration):
        self.description = description
        self.duration = duration
    
    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return '{0}({1})'.format(self.description, self.duration)

    @staticmethod
    def mins_to_seconds_formatter(dur_in_mins):
        '''
        Return duration nicely formatted minutes based on value in seconds
        '''
        return "{}s".format(int(dur_in_mins * 60))

class WorkoutSet:

    def __init__(self, reps):
        self.reps = reps
        self.exercises = []
        self._duration = 0

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        ex = ', '.join(str(exercise) for exercise in self.exercises)
        return '{0}x ({1})'.format(self.reps, ex)

    @property
    def duration(self):
        return self.reps * self._duration

    def add_exercise(self, exercise):
        self.exercises.append(exercise)
        self._duration += exercise.duration

class Workout:
    '''
    Represents a workout session
    '''

    formatting_dict = {
        'Event Day': {'color': '#001F3F',
                      'textColor': 'hsla(210, 100%, 75%, 1.0)'},
        'RunEasy': {'color': '#2ECC40',
                    'textColor': 'hsla(127, 63%, 15%, 1.0)'},
        'Intervals': {'color': '#FF4136',
                      'textColor': 'hsla(3, 100%, 25%, 1.0)'},
        'Hillsprint': {'color': '#FFDC00',
                       'textColor': 'hsla(52, 100%, 20%, 1.0)'},
        'Tempo': {'color': '#0074D9',
                  'textColor': 'hsla(208, 100%, 85%, 1.0)'}
    }

    def __init__(self, date, title):
        self.date = date
        self.title = title
        self.duration = 0
        self.workoutsets = []

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return '{0} - {1}'.format(self.date.strftime('%d %b %Y'),
                                  self.title)

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        # TODO: add if for EventDay
        ws = '\n'.join('{0}x {1}'.format(workoutset.reps,
                                         workoutset.exercises) for workoutset in self.workoutsets)
        return '{0}\n{1}'.format(self.title, ws)

    @property
    def color(self):
        return self.formatting_dict[self.title]['color']

    @property
    def textColor(self):
        return self.formatting_dict[self.title]['textColor']

    def add_workoutset(self, workoutset):
        self.workoutsets.append(workoutset)
        self.duration += workoutset.duration

class Progression:
    
    def __init__(self, start_date, length, progressions):
        self.start_date = start_date
        self.length = length
        self.sessions = []
        
        progress_dict = {
            "runeasy": self.runeasy,
            "interval": self.interval
        }
        
        start = 0
        step = len(progressions)
        
        for progression in progressions:
            self.sessions += [wk for wk in progress_dict[progression[0]](start, step, progression[1])]     
            start += 1  
        
        
    def runeasy(self, start, step, settings):
        '''
        '''

        wk = start

        dur = settings.init_dur

        while wk < self.length:
            if week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif week_type(wk, self.length) == 'rest':
                wk_dur = rest_pc_or_abs(settings.rest, dur)
            else:
                wk_dur = rest_pc_or_abs(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'RunEasy')
            ws = WorkoutSet(1)
            e = Exercise('Easy', wk_dur)
            ws.add_exercise(e)
            w.add_workoutset(ws)           

            yield w

            wk += step
    
    def interval(self, start, step, settings):
        '''
        '''

        wk = start

        dur = settings.init_dur

        while wk < self.length:
            if week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif week_type(wk, self.length) == 'rest':
                wk_dur = rest_pc_or_abs(settings.rest, dur)
            else:
                wk_dur = rest_pc_or_abs(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'Interval')
            ws = WorkoutSet(1)
            e = Exercise('Easy', wk_dur)
            ws.add_exercise(e)
            w.add_workoutset(ws)           

            yield w

            wk += step

class Plan:
    '''
    Represents running training plan for prescribed event and level.
    '''
    
    def __init__(self, distance, level, start_date, event_date, event_title):
        
        self.distance = distance
        self.level = level
        self.start_date = start_date
        self._event_date = event_date
        self.event_title = event_title
        

        # Populate schedule with event
        self.schedule = [Workout(self._event_date, 'Event Day')]

    @property
    def length(self):
        '''
        Length of the training plan in weeks
        '''
        return self.weeks_between_dates(self.start_date, self._event_date)

    def create(self, days):
        '''
        Creates schedule based on ability level and training days
        '''
        
        details = PLANS[self.distance][self.level]
        
        for day, detail in zip(days, details):
            session_start = determine_next_weekday(self.start_date, day)
            p = Progression(session_start, self.length, detail)
            self.schedule += p.sessions

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} Plan for the {2}".format(self.length,
                                                      self.level,
                                                      self.event_title)

    @property
    def event_date(self):
        '''
        Event date property, formatted as a string
        '''
        return self._event_date.strftime('%d %b %Y')

    @staticmethod
    def weeks_between_dates(start_date, end_date):
        '''
        Return the number of weeks between two dates
        '''
        return int((determine_next_weekday(end_date, 0) -
                    determine_next_weekday(start_date, 0)).days / 7)

start_date = date(2017, 8, 25)
event_date = start_date + timedelta(weeks=4)
p = Plan('5k', 'Beginner', start_date, event_date, 'RACE DAY')

days = [0, 2]
p.create(days)

for wo in p.schedule:
    print('{wo.date}:\n{wo}\n'.format(wo=wo))

import json

class WorkoutEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            to_serialize = {
                'title': o.title,
                'start': o.date,
                'color': o.color,
                'textColor': o.textColor,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)

class Workout:
    def __init__(self):
        self.title = "Run"
        self.date = "today"
        self.color = "red"
        self.textColor = "blue"

w = Workout()

json.dumps(w, cls=WorkoutEncoder)






