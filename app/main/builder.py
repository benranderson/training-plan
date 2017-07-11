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


def plan_builder(distance, ability, plan_length, days_per_week):

    plan = Plan(distance, ability, plan_length)

    plan

    return plan


def create_5k_beginner_plan(plan_length, days_per_week):

    days = {}

    days["A"] = list(run_easy_progress(plan_length, "5k", "Beginner"))

    if days_per_week > 1:
        days["B"] = list(inteval_hills_progress(plan_length, "5k", "Beginner"))

    if days_per_week > 2:
        days["C"] = list(run_easy_progress(plan_length, "5k", "Beginner"))

    return days


def run_easy_progress(plan_length, distance="5k", ability="Beginner"):

    week = 0
    work_week = 0

    reps = 1
    durations = {"Beginner": 25}
    duration = durations[ability]

    while week < plan_length:

        if not rest_week(week, plan_length):

            if week > 0 and work_week % 3 == 0 and duration < 35:
                duration += 5

            exercise = Exercise("Easy", duration)

            work_week += 1

        else:
            rest_duration = duration - 5
            exercise = Exercise("Easy", rest_duration)

        workout = []

        workout_set = WorkoutSet(reps)
        workout_set.add_exercise(exercise)

        workout.append(workout_set)

        yield workout

        week += 1


def inteval_hills_progress(plan_length, distance="5k", ability="Beginner"):

    week = 0
    int_work_week = 0
    hill_work_week = 0

    int_reps = 5
    fast_duration = 0.5
    easy_duration = 1

    hill_reps = 6

    while week < plan_length:

        # interval week
        if week % 2 == 0:

            if not rest_week(week, plan_length):

                if int_work_week > 0:
                    if int_work_week % 2 == 0:
                        if fast_duration < 1:
                            fast_duration += 0.25

                    elif int_reps < 8:
                        int_reps += 1

                int_work_week += 1

            warmup_dur = 10
            warmdown_dur = 10

            work_reps = int_reps
            work_1 = Exercise("Fast", fast_duration)
            work_2 = Exercise("Easy", 1)

            work_sets = [work_1, work_2]

        # hillsprint week
        else:

            if not rest_week(week, plan_length):

                if hill_work_week > 0 and hill_work_week % 3 == 0 and hill_reps < 10:
                    hill_reps += 2

                hill_work_week += 1

            work_reps = hill_reps

            warmup_dur = 12
            warmdown_dur = 12
            work = Exercise("Hill", 0.25)

            work_sets = [work]

        workout = []

        warmup = WorkoutSet(1)
        warmup.add_exercise(Exercise("Easy", warmup_dur))
        workout.append(warmup)

        work = WorkoutSet(work_reps)

        for work_set in work_sets:
            work.add_exercise(work_set)

        workout.append(work)

        warmdown = WorkoutSet(1)
        warmdown.add_exercise(Exercise("Easy", warmdown_dur))
        workout.append(warmdown)

        yield workout

        week += 1


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

    def __init__(self, distance, ability, plan_length, days_per_week):
        self.distance = distance
        self.ability = ability
        self.plan_length = plan_length
        self.days_per_week = days_per_week

        self.days = create_5k_beginner_plan(plan_length, days_per_week)

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "{0} week {1} {2} plan ({3} days per week)".format(self.plan_length,
                                                                  self.ability,
                                                                  self.distance,
                                                                  self.days_per_week)

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

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        # exercises = [(exercise.description, exercise.total_time)
        #              for exercise in self.exercises]

        return "{0} x {1}".format(self.reps, self.exercises)


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
        return "{0} for {1} min".format(self.description, self.total_time)


if __name__ == "__main__":
    plan = create_5k_beginner_plan(12, 3)

    for day in plan:
        print(day)
        for week in plan[day]:
            print(week)
