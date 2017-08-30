from datetime import date, timedelta, datetime
import calendar
import json
import types
import os

basedir = os.path.abspath(os.path.dirname(__file__))

from .plans import PLANS
from .utils import determine_next_weekday, week_type, rest_week, \
    rest_pc_or_abs


class Exercise:

    def __init__(self, description, duration, intensity='Normal'):
        self.description = description
        self.duration = duration
        self.intensity = intensity

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return '{0}({1})'.format(self.description, self.duration)

    @staticmethod
    def mins_to_seconds_formatter(dur_in_mins):
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
        'Interval': {'color': '#FF4136',
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
            "interval": self.interval,
            "hillsprint": self.hillsprint
        }

        start = 0
        step = len(progressions)

        for progression in progressions:
            self.sessions += [wk for wk in progress_dict[progression[0]]
                              (start, step, progression[1])]
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

    def hillsprint(self, start, step, settings):
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
            w = Workout(date, 'Hillsprint')
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

            durs = [10, wk_dur, 10]

            for d in durs:
                ws = WorkoutSet(1)
                e = Exercise('Easy', d)
                ws.add_exercise(e)
                w.add_workoutset(ws)

            yield w

            wk += step


def create_intervals(self, initial_reps, freq_reps, max_reps, initial_fast,
                     freq_fast, max_fast):
    '''
    Return an easy intervals progression as a list of workouts
    '''

    reps = initial_reps
    fast = initial_fast

    for wk, date, wk_type in plan_week_range(self.start_date, self.length):
        if wk_type == 'prog':
            if (wk / self.step) % 2 == 0:
                if fast < max_fast:
                    fast += 0.25
                else:
                    if reps < max_reps:
                        reps += 1

        wk_reps = reps
        wk_fast = fast

        w = Workout(date, 'Intervals')
        ws = WorkoutSet(1)
        e = Exercise('Easy', 10)
        w.add_workoutset(ws)

        ws = WorkoutSet(wk_reps)
        es = [Exercise('Fast', wk_fast), Exercise('Easy', 1)]
        for e in es:
            ws.add_exercise(e)
        w.add_workoutset(ws)

        ws = WorkoutSet(1)
        e = Exercise('Easy', 10)
        ws.add_exercise(e)
        w.add_workoutset(ws)

        self.sessions.append(w)


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


def open_json(file_name):
    try:
        with open(file_name, 'r') as i:
            return json.load(i)
    except FileNotFoundError:
        raise FileNotFoundError('Check {} exists'.format(file_name))


def get_plan(event, level):
    '''
    Plan factory method
    '''
    # Retrieve event information
    resource_path = os.path.join(basedir, 'events.json')
    events = open_json(resource_path)
    distance = events[event]["distance"]
    event_date = datetime.strptime(
        events[event]["date"], '%Y-%m-%d').date()

    start_date = date.today()

    return Plan(distance, level, start_date, event_date, event)
