
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


    def add_set_progression(self, day, progression):

        for i, week in enumerate(progress(self.plan_length, progression)):
            self.days[day][i].append(week)