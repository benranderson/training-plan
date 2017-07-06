'''
Progression variables:

- Exercises
- Starting reps
Reps progression
Reps progression frequency (incl. rest weeks or not?)
Maximum reps
Starting duration
Duration progression
Duration progression frequency (incl. rest weeks or not?)
Maximum duration
Rest weeks (reps and duration)
Race week (reps and duration)

- Alternating exercises each week...

'''


def plan_builder(distance, ability, plan_length):

    plan = Plan(distance, ability, plan_length)

    # Day A

    plan.add_day("A")
    set_progress = SetProgression(1, 0, 1, 0)
    set_progress.add_exercise_progression("Easy", 25, 5, 35, 3)
    plan.add_set_progression("A", set_progress)

    plan.add_day("B")
    set_progress_1 = SetProgression(1, 0, 1, 0)
    set_progress_1.add_exercise_progression("Easy", 10, 0, 10, 0)
    plan.add_set_progression("B", set_progress_1)
    set_progress_2 = SetProgression(5, 1, 8, 1)
    set_progress_2.add_exercise_progression("Easy", 25, 5, 35, 3)
    set_progress_2.add_exercise_progression("Easy", 25, 5, 35, 3)
    plan.add_set_progression("B", set_progress_2)
    set_progress_3 = SetProgression(1, 0, 1, 0)
    set_progress_3.add_exercise_progression("Easy", 10, 0, 10, 0)
    plan.add_set_progression("B", set_progress_3)

    plan.add_day("C")
    set_progress = SetProgression(1, 0, 1, 0)
    set_progress.add_exercise_progression("Easy", 25, 5, 35, 3)
    plan.add_set_progression("C", set_progress)

    return plan


def progress(plan_length, set_progress):
    ''' Yield progression '''

    reps = set_progress.start_reps
    exercise_progressions = set_progress.exercise_progressions

    week = 0
    work_week = 0

    exercise_durs = []

    for exercise_progression in exercise_progressions:
        exercise_durs.append(exercise_progression.start_dur)

    while week < plan_length:

        if not rest_week(week, plan_length):

            if set_progress.freq > 0 and work_week % set_progress.freq == 0 and reps < set_progress.max_reps:
                reps += 1

            for i, exercise_progression in enumerate(exercise_progressions):

                progress_check = exercise_progression.freq > 0 and work_week % exercise_progression.freq == 0
                max_check = exercise_durs[i] < exercise_progression.max_dur

                if progress_check and max_check:
                    exercise_durs[i] += exercise_progression.progress_dur

            work_week += 1

        exercises = []

        for i, exercise_progression in enumerate(exercise_progressions):
            exercises.append(Exercise(exercise_progression.description,
                                      exercise_durs[i]))

        workout_set = WorkoutSet(reps)

        for exercise in exercises:
            workout_set.add_exercise(exercise)

        yield workout_set

        week += 1


def rest_week(week, plan_length):
    ''' Return True if rest week and False if progression week '''
    build_up = plan_length % 4
    if week <= build_up and build_up < 3:
        return False
    elif (week - build_up + 1) % 4 == 0:
        return True
    else:
        return False


class Plan(object):
    '''
    Model for a training plan
    '''

    def __init__(self, distance, ability, plan_length):
        self.distance = distance
        self.ability = ability
        self.plan_length = plan_length

        self.days = {}

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "{0} {1}".format(self.distance, self.ability)

    def add_day(self, day):
        self.days[day] = []
        for week in range(self.plan_length):
            self.days[day].append([])

    def add_set_progression(self, day, progression):

        for i, week in enumerate(progress(self.plan_length, progression)):
            self.days[day][i].append(week)

    def calculate_duration_of_day(self, week, day):
        pass


class SetProgression(object):
    def __init__(self, start_reps, progress_reps, max_reps, freq):
        self.start_reps = start_reps
        self.progress_reps = progress_reps
        self.max_reps = max_reps
        self.freq = freq

        self.exercise_progressions = []

    def add_exercise_progression(self, description, dur, progress_dur, max_dur, freq):
        exercise_progression = ExerciseProgression(
            description, dur, progress_dur, max_dur, freq)
        self.exercise_progressions.append(exercise_progression)


class ExerciseProgression(object):
    def __init__(self, description, start_dur, progress_dur, max_dur, freq):
        self.description = description
        self.start_dur = start_dur
        self.progress_dur = progress_dur
        self.max_dur = max_dur
        self.freq = freq


class WorkoutSet(object):
    def __init__(self, reps):
        self.reps = reps
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def calculate_duration(self):

        duration = 0

        for exercise in self.exercises:
            duration += exercise.total_time

        return duration


class Exercise(object):
    '''
    Settings for an exercise (description, duration, etc.)
    '''

    def __init__(self, description, total_time):
        self.description = description
        self.total_time = total_time

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "{0} ({1})".format(self.description, self.total_time)