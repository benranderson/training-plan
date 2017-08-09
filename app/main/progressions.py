import datetime


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


def run_easy_progress(weeks, start=25, freq=3, max=35):
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
    dur = start
    week = 0
    while week < weeks:
        if not rest_week(week, weeks):
            if (week + 1) % freq == 0 and dur < max:
                dur += 5
            wk_dur = dur
        else:
            wk_dur = dur - 5
        yield Run("Easy", wk_dur)
        week += 1


def interval_progress(weeks, start_week=0, step=1, reps_start=5, reps_freq=1,
                      reps_max=8, fast_start=0.5, fast_freq=2, fast_max=1):
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
        yield Interval(wk_reps, wk_fast, 1)
        week += step


def hillsprint_progress(weeks, start_week=1, step=2, reps_start=6, reps_freq=3,
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
    week = start_week

    reps = reps_start

    while week < weeks:
        if week > 0:
            if not rest_week(week, weeks):
                if ((week + start_week) / step) % reps_freq == 0 and reps < reps_max:
                    reps += 2

        wk_reps = reps
        yield HillSprint(wk_reps, 0.25)
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


class EventDay:

    color = '#001F3F'
    textColor = 'hsla(210, 100%, 75%, 1.0)'

    def __init__(self, event):
        self.title = event


class Tempo:
    '''
    Represents a tempo workout.
    '''

    color = '#0074D9'
    textColor = 'hsla(208, 100%, 85%, 1.0)'

    def __init__(self, warmup, steady, easy, tempo, warmdown):
        self.warmup = warmup
        self.steady = steady
        self.easy = easy
        self.tempo = tempo
        self.warmdown = warmdown
        self.background_css = 'btn-primary'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "RunEasy({0}m), Runsteady({1}m) Runeasy({2}m) Runtempo({3}m) Runeasy({4}m)".format(self.warmup,
                                                                                                  self.steady,
                                                                                                  self.easy,
                                                                                                  self.tempo,
                                                                                                  self.warmdown)

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run for {0} minutes at an easy pace".format(self.duration)


class Run:
    '''
    Represents a run workout.
    '''

    color = '#2ECC40'
    textColor = 'hsla(127, 63%, 15%, 1.0)'

    def __init__(self, pace, duration):
        self.pace = pace
        self.duration = duration
        self.warmup = None
        self.warmdown = None
        self.background_css = 'btn-success'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run{0}({1}m)".format(self.pace, self.duration)

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run for {0} minutes at an easy pace".format(self.duration)


class Interval:
    '''
    Represents an interval training workout.
    '''

    color = '#FF4136'
    textColor = 'hsla(3, 100%, 25%, 1.0)'

    def __init__(self, reps, fast, slow):
        self.description = "Intervals"
        self.reps = reps
        self.fast = fast
        self.slow = slow
        self.warmup = Run("Easy", 10)
        self.warmdown = Run("Easy", 10)
        self.duration = self.calculate_duration()
        self.background_css = 'btn-danger'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        fast = mins_to_seconds_formatter(self.fast)
        slow = mins_to_seconds_formatter(self.slow)
        return "{0}, {1}x Interval({2}, {3}), {4}".format(repr(self.warmup), self.reps, fast, slow, repr(self.warmdown))

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        fast = mins_to_seconds_formatter(self.fast)
        slow = mins_to_seconds_formatter(self.slow)
        return "Run fast for {0} then run at an easy pace for {1}.  Repeat {2} times.".format(fast, slow, self.reps)

    def calculate_duration(self):
        warmup = self.warmup.duration
        work = self.reps * (self.fast + self.slow)
        warmdown = self.warmdown.duration
        return warmup + work + warmdown


class HillSprint:
    '''
    Represents a hill sprint workout.
    '''

    color = '#FFDC00'
    textColor = 'hsla(52, 100%, 20%, 1.0)'

    def __init__(self, reps, sprint):
        self.description = "Hill Sprint"
        self.reps = reps
        self.sprint = sprint
        self.warmup = Run("Easy", 12)
        self.warmdown = Run("Easy", 12)
        self.duration = self.calculate_duration()
        self.background_css = 'btn-warning'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        sprint = mins_to_seconds_formatter(self.sprint)
        return "{0}, {1}x HillSprint({2}), {3}".format(repr(self.warmup), self.reps, sprint, repr(self.warmdown))

    def __str__(self):
        '''
        Return a more human-readable representation
        '''
        sprint = mins_to_seconds_formatter(self.sprint)
        return "Run fast uphill for {0}.  Repeat {1} times.".format(sprint, self.reps)

    def calculate_duration(self):
        warmup = self.warmup.duration
        work = self.reps * self.sprint
        warmdown = self.warmdown.duration
        return warmup + work + warmdown


def mins_to_seconds_formatter(dur_in_mins):
    return "{}s".format(int(dur_in_mins * 60))
