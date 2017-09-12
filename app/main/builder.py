from datetime import date, timedelta, datetime
import types
import os

from .plans import PLANS
from . import utils

basedir = os.path.abspath(os.path.dirname(__file__))


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

    def __init__(self, date, category):
        self.date = date
        self.category = category
        self.duration = 0
        self.workoutsets = []

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return '{0} - {1}'.format(self.date.strftime('%d %b %Y'),
                                  self.category)

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        # TODO: add if for EventDay

        return '<br />'.join('{0}x {1}'.format(workoutset.reps,
                                               workoutset.exercises) for workoutset in self.workoutsets)

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
            "hill": self.hill,
            "tempo": self.hill,
            "crosstrain": self.hill
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
            if utils.week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif utils.week_type(wk, self.length) == 'rest':
                wk_dur = utils.rest_duration(settings.rest, dur)
            else:
                wk_dur = utils.rest_duration(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'easy')
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
            if utils.week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif utils.week_type(wk, self.length) == 'rest':
                wk_dur = utils.rest_duration(settings.rest, dur)
            else:
                wk_dur = utils.rest_duration(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'interval')

            durs = [10, wk_dur, 10]

            for d in durs:
                ws = WorkoutSet(1)
                e = Exercise('Easy', d)
                ws.add_exercise(e)
                w.add_workoutset(ws)

            yield w

            wk += step

    def hill(self, start, step, settings):
        '''
        '''

        wk = start

        dur = settings.init_dur

        while wk < self.length:
            if utils.week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif utils.week_type(wk, self.length) == 'rest':
                wk_dur = utils.rest_duration(settings.rest, dur)
            else:
                wk_dur = utils.rest_duration(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'hillsprint')
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
            session_start = utils.next_weekday(self.start_date, day)
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
        return int((utils.next_weekday(end_date, 0) -
                    utils.next_weekday(start_date, 0)).days / 7)


def get_plan(event, level):
    '''
    Plan factory method
    '''
    # Retrieve event information
    resource_path = os.path.join(basedir, 'events.json')
    events = utils.open_json(resource_path)
    distance = events[event]["distance"]
    event_date = datetime.strptime(
        events[event]["date"], '%Y-%m-%d').date()

    start_date = date.today()

    return Plan(distance, level, start_date, event_date, event)
