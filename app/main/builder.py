import datetime
import calendar
import json

from .events import events_dict


def determine_next_weekday(now, weekday):
    '''
    datetime, int -> datetime
    '''
    days_ahead = weekday - now.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return now + datetime.timedelta(days_ahead)


def mins_to_seconds_formatter(dur_in_mins):
    return "{}s".format(int(dur_in_mins * 60))


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


class WorkoutSet:

    def __init__(self, reps, exercises):
        self.reps = reps
        self.exercises = exercises

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        ex = ', '.join(str(exercise) for exercise in self.exercises)
        return '{0}x ({1})'.format(self.reps, ex)

    def calculate_duration(self):
        '''
        Return total duration of workout set
        '''
        duration = 0

        for exercise in self.exercises:
            duration += exercise.duration

        return self.reps * duration


class Workout:

    def __init__(self, date, description):
        self.date = date
        self.description = description
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
        ws = '\n'.join('{0}x {1}'.format(workoutset.reps,
                                         workoutset.exercises) for workoutset in self.workoutsets)
        return '{0}\n{1}'.format(self.description, ws)

    def calculate_duration(self):
        '''
        Return total duration of workout
        '''
        duration = 0

        for workoutset in self.workoutsets:
            duration += workoutset.calculate_duration()

        return duration


class EventDay(Workout):
    '''
    Represents the Event Day
    '''

    color = '#001F3F'
    textColor = 'hsla(210, 100%, 75%, 1.0)'

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        return '{}!'.format(self.description)


class Run(Workout):
    '''
    Represents a run workout
    '''

    color = '#2ECC40'
    textColor = 'hsla(127, 63%, 15%, 1.0)'

    def __init__(self, date, duration):
        super().__init__(date, 'Run')
        self.workoutsets.append(WorkoutSet(1, [Exercise("Easy", duration)]))


class Interval(Workout):
    '''
    Represents an interval training workout
    '''

    color = '#FF4136'
    textColor = 'hsla(3, 100%, 25%, 1.0)'

    def __init__(self, date, reps, fast, easy):
        super().__init__(date, "Intervals")

        warmup = WorkoutSet(1, [Exercise("Easy", 10)])
        work = WorkoutSet(reps, [Exercise("Fast", easy),
                                 Exercise("Easy", fast)])
        warmdown = WorkoutSet(1, [Exercise("Easy", 10)])

        self.workoutsets = [warmup, work, warmdown]


class HillSprint(Workout):
    '''
    Represents a hill sprint workout
    '''

    color = '#FFDC00'
    textColor = 'hsla(52, 100%, 20%, 1.0)'

    def __init__(self, date, reps, sprint):
        super().__init__(date, "HillSprint")

        warmup = WorkoutSet(1, [Exercise("Easy", 12)])
        work = WorkoutSet(reps, [Exercise("Hillsprint", sprint)])
        warmdown = WorkoutSet(1, [Exercise("Easy", 12)])

        self.workoutsets = [warmup, work, warmdown]


class Tempo(Workout):
    '''
    Represents a tempo workout
    '''

    color = '#0074D9'
    textColor = 'hsla(208, 100%, 85%, 1.0)'

    def __init__(self, date, warmup, steady, easy, tempo, warmdown):
        super().__init__(date, "Tempo")

        warmup = WorkoutSet(1, [Exercise("Easy", warmup)])
        steady = WorkoutSet(1, [Exercise("Easy", steady)])
        easy = WorkoutSet(1, [Exercise("Easy", easy)])
        tempo = WorkoutSet(1, [Exercise("Easy", tempo)])
        warmdown = WorkoutSet(1, [Exercise("Easy", warmdown)])

        self.workoutsets = [warmup, steady, easy, tempo, warmdown]


def runeasy_progress(start_date, weeks, start=25, freq=3, max=35):
    '''
    number, number, number, number -> iterator

    Easy running progression:
    - Every 3rd week the easy running will have a progression
    - The progressions will be: Every 3rd week the easy running total will
    increase by 5 minutes.  The increase will be in one of the easy running
    sessions, and it will alternate between the two
    - On an easier week: The easy running session with less minutes will
    decrease by 5 minutes from the previous week
    - On a target race week: The easy running session with less minutes will
    decrease by 5 minutes from the previous week, the longer easy run will be
    replaced by the race
    - The maximum easy running session will be: Runeasy(35)"
    '''
    workout_date = start_date
    dur = start
    week = 0
    while week < weeks:
        if not rest_week(week, weeks):
            if (week + 1) % freq == 0 and dur < max:
                dur += 5
            wk_dur = dur
        else:
            wk_dur = dur - 5
        yield Run(workout_date, wk_dur)

        workout_date += datetime.timedelta(weeks=1)
        week += 1


def interval_progress(start_date, weeks, start_week=0, step=1, reps_start=5,
                      reps_freq=1, reps_max=8, fast_start=0.5, fast_freq=2,
                      fast_max=1):
    '''
    -> iterator

    Interval progression:
    - Every intervals session (not including easier weeks) will have a
    progression
    - The progressions will be: Increase the number of reps by 1, the following
    week increase the length of the rep by 0.25, continue like this until
    8*RunfastRuneasy(1,1) is reached
    - On an easier week: Go back to previous session
    - On a target race week: Runeasy(10) 5x Interval(0.5, 1) Runeasy(10)
    '''

    workout_date = start_date
    week = start_week
    reps = reps_start
    fast = fast_start

    while week < weeks:
        if week > 0:
            if not rest_week(week, weeks):
                if (week / step) % 2 == 0:
                    if fast < fast_max:
                        fast += 0.25
                else:
                    if reps < reps_max:
                        reps += 1

        wk_reps = reps
        wk_fast = fast

        yield Interval(workout_date, wk_reps, wk_fast, 1)

        workout_date += datetime.timedelta(weeks=step)
        week += step


def hillsprint_progress(start_date, weeks, start_week=1, step=1, reps_start=6, reps_freq=3,
                        reps_max=8):
    '''
    -> iterator

    Hills progression:
    - Every 3rd hills session (not including easier weeks) will have a
    progression
    - The progressions will be: Increase number of reps by 2
    - On an easier week: Go back to previous session. So week by week the
    number of reps will look like 6,6,8,6,8,10
    - On a target race week: Runeasy(12) 6*Hillsprint(0.25) Runeasy(12)
    '''

    workout_date = start_date
    week = start_week
    reps = reps_start

    while week < weeks:
        if week > 0:
            if not rest_week(week, weeks):
                if ((week + start_week) / step) % reps_freq == 0 and reps < reps_max:
                    reps += 2

        wk_reps = reps
        yield HillSprint(workout_date, wk_reps, 0.25)

        workout_date += datetime.timedelta(weeks=step)
        week += step


def tempo_progress(weeks, start_week=1, step=2, freq=3):
    '''
    int, int, int, int -> iterator

    Tempo progression:
    - Every 3rd tempo session will have a progression
    - The progresssions will be:
    - Runeasy(5) Runsteady(10) Runeasy(10) Runtempo(5) Runeasy(5)
    - Runeasy(5) Runsteady(15) Runeasy(10) Runtempo(5) Runeasy(5)
    - Runeasy(10) Runsteady(15) Runeasy(10) Runtempo(5) Runeasy(5)
    - Runeasy(10) Runsteady(15) Runeasy(5) Runtempo(5) Runeasy(10)
    - Runeasy(10) Runsteady(10) Runeasy(5) Runtempo(10) Runeasy(10)
    - Runeasy(10) Runsteady(10) Runtempo(10) Runeasy(10)
    - On an easier week: the session will be the same as the week before
    '''
    week = start_week
    durations = [[5, 10, 10, 5, 5],
                 [5, 15, 10, 5, 5],
                 [10, 15, 10, 5, 5],
                 [10, 15, 5, 5, 10],
                 [10, 10, 5, 10, 10],
                 [10, 10, 10, 10, 10]]

    i = 0

    while week < weeks:
        if week > 0:
            if not rest_week(week, weeks):
                if ((week + start_week) / step) % freq == 0 and i < 5:
                    i += 1

        yield Tempo(durations[i][0], durations[i][1], durations[i][2],
                    durations[i][3], durations[i][4])
        week += step


class Plan:
    '''
    Represents running training plan for prescribed event and level.
    '''

    def __init__(self, start_date, event_date, event):
        self.start_date = start_date
        self._event_date = event_date
        self.event = event
        self.level = None
        self.length = self.weeks_between_dates(start_date, self._event_date)

        # Populate schedule with event
        self.schedule = [EventDay(self._event_date, event)]

    def create_schedule(self, level, days):

        self.level = level

        def builder_dict(level, days):
            level_dict = {
                'Beginner': self.beginner_plan,
                'Intermediate': self.intermediate_plan,
                'Advanced': self.advanced_plan
            }.get(level, None)
            return level_dict(days)

        builder_dict(level, days)

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
        Event date property, formatted as a string.
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


    def builder_5k_beg(self, weeks, days):
        '''
        int, int -> None

        Populate plan schedule with 5k Beginner progressions.
        Based on specified number of weeks and for specified number of training
        days a week.
        '''

        progressions = [runeasy_progress,
                        hillsprint_progress,
                        runeasy_progress]

        for day, progression in zip(days, progressions):
            progress_start = determine_start_date(self.current_date, day)
            self.schedule += list(progression(progress_start, weeks))

    def builder_5k_int(self, weeks, days):
        '''
        int, int -> matrix

        Return matrix (list of lists) representing 5k Intermediate progressions.
        Based on specified number of weeks and for specified number of training
        days a week.
        '''

        progressions = []

        if days > 0:
            tempos = list(tempo_progress(weeks, start_week=0, step=2, freq=3))
            ints = list(interval_progress(weeks, start_week=1, step=2))
            progress = [val for pair in zip(tempos, ints) for val in pair]
            progressions.append(progress)
        if days > 1:
            progressions.append(list(run_easy_progress(weeks)))
        if days > 2:
            progressions.append(
                list(hillsprint_progress(weeks, start_week=0, step=1)))

        return progressions


class Plan5k(Plan):

    def get_distance(self):
        return "5k"

    def beginner_plan(self, days):
        self.schedule.append(Run(self.start_date, 10))

    def intermediate_plan(self, days):
        self.schedule.append(Run(self.start_date, 10))

    def advanced_plan(self, days):
        self.schedule.append(Run(self.start_date, 10))


def get_plan(event):
    '''
    The factory method
    '''

    # Retrieve event information
    distance, event_date = events_dict[event]

    plans = {
        "5k": Plan5k,
        "10k": Plan5k,
        "half": Plan5k,
        "ful": Plan5k,
    }

    return plans[distance](datetime.date.today(), event_date, event)
