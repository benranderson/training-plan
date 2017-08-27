import datetime
import calendar
import json
import types

from .events import events_dict
import utils


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
        'Intervals': {'color': '#FF4136',
                      'textColor': 'hsla(3, 100%, 25%, 1.0)'},
        'Hillsprint': {'color': '#FFDC00',
                       'textColor': 'hsla(52, 100%, 20%, 1.0)'},
        'Tempo': {'color': '#0074D9',
                  'textColor': 'hsla(208, 100%, 85%, 1.0)'}
    }

    def __init__(self, date, description):
        self.date = date
        self.description = description
        self.duration = 0
        self.workoutsets = []

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return '{0} - {1}'.format(self.date.strftime('%d %b %Y'),
                                  self.description)

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        # TODO: add if for EventDay
        ws = '\n'.join('{0}x {1}'.format(workoutset.reps,
                                         workoutset.exercises) for workoutset in self.workoutsets)
        return '{0}\n{1}'.format(self.description, ws)

    @property
    def color(self):
        return self.formatting_dict[self.description]['color']

    @property
    def textColor(self):
        return self.formatting_dict[self.description]['textColor']

    def add_workoutset(self, workoutset):
        self.workoutsets.append(workoutset)
        self.duration += workoutset.duration


class Progression:
    def __init__(self, start_date, length, start_week=0, step=1, func=None):
        self.start_date = start_date
        self.length = length
        self.start_week = start_week
        self.step = step
        self.sessions = []

        if func is not None:
            self.create = types.MethodType(func, self)

    def create(self):
        raise NotImplementedError


def create_runeasy(self, distance, level, workout):
    '''
    Return an easy running progression as a list of workouts
    '''

    init_dur = RUNEASY_SETTINGS[distance][level][workout]['init_dur']
    prog_freq = RUNEASY_SETTINGS[distance][level][workout]['prog_freq']
    rest_week_cut = RUNEASY_SETTINGS[distance][level][workout]['rest_week_cut']
    race_week_cut = RUNEASY_SETTINGS[distance][level][workout]['race_week_cut']
    max_dur = RUNEASY_SETTINGS[distance][level][workout]['max_dur']

    dur = init_dur

    def week_cut_version(week_cut, dur):
        '''
        Return rest week duration based on wether cut is applied as an absolute
        or % value
        '''
        if "%" in week_cut:
            return (float(week_cut.strip('%')) / 100) * dur
        else:
            return dur - week_cut

    for wk, date, wk_type in plan_week_range(self.start_date, self.length):
        if wk_type == 'prog':
            if (wk + 1) % prog_freq == 0 and dur < max_dur:
                dur += 5
            wk_dur = dur
        elif wk_type == 'rest':
            wk_dur = week_cut_version(rest_week_cut, dur)
        else:
            wk_dur = week_cut_version(race_week_cut, dur)

        w = Workout(date, 'RunEasy')
        ws = WorkoutSet(1)
        e = Exercise('Easy', wk_dur)
        ws.add_exercise(e)
        w.add_workoutset(ws)
        self.sessions.append(w)


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

    def __init__(self, start_date, event_date, event, settings):
        self.start_date = start_date
        self._event_date = event_date
        self.event = event
        self.settings = settings
        self.level = None

        # Populate schedule with event
        self.schedule = [Workout(self._event_date, 'Event Day')]

    @property
    def length(self):
        '''
        Length of the training plan in weeks
        '''
        return self.weeks_between_dates(self.start_date, self._event_date)

    def create_schedule(self, level, days):
        '''
        Creates schedule based on ability level and training days
        '''

        self.level = level

        def builder_dict(level, days):
            level_dict = {
                'Beginner': self.beginner_plan,
                'Intermediate': self.intermediate_plan,
                'Advanced': self.advanced_plan
            }.get(level, None)
            return level_dict(days)

        self.schedule += builder_dict(level, days)

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} Plan for the {2}".format(self.length,
                                                      self.level,
                                                      self.event)

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

    def beginner_plan(self, days):
        raise NotImplementedError

    def intermediate_plan(self, days):
        raise NotImplementedError

    def advanced_plan(self, days):
        raise NotImplementedError


class Plan5k(Plan):

    def beginner_plan(self, days):
        '''
        int, int -> None

        Populate plan schedule with 5k Beginner progressions based on number of
        training days a week.
        '''

        # TODO: Namedtuple for progression inputs, use i

        details = [
            {'func': None, 'inputs': (25, 3, 35)},
            {'func': create_intervals, 'inputs': (25, 1, 25)},
            {'func': None, 'inputs': (25, 3, 35)}
        ]

        schedule = []

        for day, details in zip(days, details):
            session_start = determine_next_weekday(self.start_date, day)
            p = Progression(session_start, self.length, details['func'])
            p.create(details['inputs'][0], details['inputs'][1],
                     details['inputs'][2])
            schedule += p.sessions

        return schedule

    def intermediate_plan(self, days):
        '''
        int, int -> matrix

        Return matrix (list of lists) representing 5k Intermediate progressions.
        Based on specified number of weeks and for specified number of training
        days a week.
        '''

        # progressions = []

        # if days > 0:
        #     tempos = list(tempo_progress(weeks, start_week=0, step=2, freq=3))
        #     ints = list(interval_progress(weeks, start_week=1, step=2))
        #     progress = [val for pair in zip(tempos, ints) for val in pair]
        #     progressions.append(progress)
        # if days > 1:
        #     progressions.append(list(run_easy_progress(weeks)))
        # if days > 2:
        #     progressions.append(
        #         list(hillsprint_progress(weeks, start_week=0, step=1)))

        # return progressions

        pass

    def advanced_plan(self, days):
        pass


class Plan10k(Plan):
    def beginner_plan(self, days):
        raise NotImplementedError

    def intermediate_plan(self, days):
        raise NotImplementedError

    def advanced_plan(self, days):
        raise NotImplementedError


class PlanHalf(Plan):
    def beginner_plan(self, days):
        raise NotImplementedError

    def intermediate_plan(self, days):
        raise NotImplementedError

    def advanced_plan(self, days):
        raise NotImplementedError


class PlanFull(Plan):
    def beginner_plan(self, days):
        raise NotImplementedError

    def intermediate_plan(self, days):
        raise NotImplementedError

    def advanced_plan(self, days):
        raise NotImplementedError


def get_plan(event):
    '''
    Plan factory method
    '''
    # Retrieve event information
    events = open_json('inputs/events')
    distance = events[event]["distance"]
    event_date = datetime.datetime.strptime(
        events[event]["date"], '%Y-%m-%d').date()

    plans = {
        "5k": Plan5k,
        "10k": Plan10k,
        "half": PlanHalf,
        "full": PlanFull,
    }

    settings = open_json('inputs/plans')

    plan_settings = settings[distance][]

    return plans[distance](datetime.date.today(), event_date, event, settings)
