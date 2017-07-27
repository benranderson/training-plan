class Plan:

    def __init__(self, distance, ability, length, days_per_week):
        self.distance = distance
        self.ability = ability
        self.length = length
        self.days_per_week = days_per_week

        self.progressions = {}

    def add_progression(self, day, progression):
        self.progressions[day] = progression

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} {2} plan ({3} days per week)".format(self.length,
                                                                  self.ability,
                                                                  self.distance,
                                                                  self.days_per_week)


class Workout:

    def __init__(self, rest=False):
        self.rest = rest
        self.work_sets = []

    def add_work_set(self, work_set):
        self.work_sets.append(work_set)

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "Rest={0} {1}".format(self.rest, self.work_sets)


class WorkSet:

    def __init__(self, reps):
        self.reps = reps
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def calculate_duration(self):

        duration = 0

        for exercise in self.exercises:
            duration += exercise.total_time

        return self.reps * duration

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} x {1}".format(self.reps, self.exercises)


class Exercise:

    def __init__(self, description, total_time):
        self.description = description
        self.total_time = total_time

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "{0} for {1} min".format(self.description, self.total_time)


def rest_week(week, plan_length):
    ''' Return True if rest week and False if progression week '''
    build_up = plan_length % 4
    if week <= build_up and build_up < 3:
        return False
    elif (week - build_up + 1) % 4 == 0:
        return True
    else:
        return False

# =============
# Beginner Plan
# =============


plan = Plan("5k", "Beginner", 24, 3)

# Day A
# -----

start_dur = 25
progress = 5
freq = 3
max = 2
rest = -5

work_week = 0
multiplier = 0

progression = []

for week in range(plan.length):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:
        if week > 0 and (work_week + 1) % freq == 0 and multiplier < max:
            multiplier += 1

        work_week += 1
        duration = start_dur + multiplier * progress

    else:
        duration = start_dur + multiplier * progress + rest

    workset = WorkSet(1)
    workset.add_exercise(Exercise("Easy", duration))
    workout.add_work_set(workset)
    progression.append(workout)
    plan.add_progression("A", progression)

# Day B
# -----

# Interval progression

start_dur = 0.5
prog_dur = 0.25
mult_dur = 0

start_reps = 5
prog_reps = 1
mult_reps = 0

work_week = 0

progression_1 = []

for week in range(0, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        if work_week % 2 == 0:
            # Duration progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
                mult_dur += 1

        else:
            # Reps progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
                mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Fast", duration))
    workset.add_exercise(Exercise("Easy", 1))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmdown)

    progression_1.append(workout)

# Hills progression

start_dur = 0.25
prog_dur = 0
mult_dur = 0

start_reps = 6
prog_reps = 2
mult_reps = 0

work_week = 0

progression_2 = []

for week in range(1, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        # Reps progression
        if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
            mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Hills", duration))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmdown)
    progression_2.append(workout)

progression = [val for pair in zip(
    progression_1, progression_2) for val in pair]

plan.add_progression("B", progression)

# Day C

start_dur = 30
progress = 5
freq = 3
max = 1
rest = -5

work_week = 0
multiplier = 0

progression = []

for week in range(plan.length):

    rest = rest_week(week, plan.length)

    workout = Workout(rest)

    if not rest:
        if week > 0 and (work_week + 1) % freq == 0 and multiplier < max:
            multiplier += 1

        work_week += 1
        duration = start_dur + multiplier * progress

    else:
        duration = start_dur + multiplier * progress + rest

    workset = WorkSet(1)
    workset.add_exercise(Exercise("Easy", duration))
    workout.add_work_set(workset)
    progression.append(workout)
    plan.add_progression("C", progression)


# =============
# Intermediate Plan
# =============


plan = Plan("5k", "Intermediate", 24, 3)

# Day A
# -----

# Tempo progression

start_dur = 0.5
prog_dur = 0.25
mult_dur = 0

start_reps = 5
prog_reps = 1
mult_reps = 0

work_week = 0

progression_1 = []

for week in range(0, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        if work_week % 2 == 0:
            # Duration progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
                mult_dur += 1

        else:
            # Reps progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
                mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Fast", duration))
    workset.add_exercise(Exercise("Easy", 1))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmdown)

    progression_1.append(workout)

# Hills progression

start_dur = 0.25
prog_dur = 0
mult_dur = 0

start_reps = 6
prog_reps = 2
mult_reps = 0

work_week = 0

progression_2 = []

for week in range(1, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        # Reps progression
        if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
            mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Hills", duration))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmdown)
    progression_2.append(workout)

progression = [val for pair in zip(
    progression_1, progression_2) for val in pair]

plan.add_progression("B", progression)

# Day B
# -----

# Interval progression

start_dur = 0.5
prog_dur = 0.25
mult_dur = 0

start_reps = 5
prog_reps = 1
mult_reps = 0

work_week = 0

progression_1 = []

for week in range(0, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        if work_week % 2 == 0:
            # Duration progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
                mult_dur += 1

        else:
            # Reps progression
            if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
                mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Fast", duration))
    workset.add_exercise(Exercise("Easy", 1))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 10))
    workout.add_work_set(warmdown)

    progression_1.append(workout)

# Hills progression

start_dur = 0.25
prog_dur = 0
mult_dur = 0

start_reps = 6
prog_reps = 2
mult_reps = 0

work_week = 0

progression_2 = []

for week in range(1, plan.length, 2):

    rest = rest_week(week, plan.length)
    workout = Workout(rest)

    if not rest:

        # Reps progression
        if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
            mult_reps += 1

        work_week += 1

    reps = start_reps + mult_reps * prog_reps
    duration = start_dur + mult_dur * prog_dur

    # Warmup set
    warmup = WorkSet(1)
    warmup.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmup)

    # Work Set
    workset = WorkSet(reps)
    workset.add_exercise(Exercise("Hills", duration))
    workout.add_work_set(workset)

    # Warmdown set
    warmdown = WorkSet(1)
    warmdown.add_exercise(Exercise("Easy", 12))
    workout.add_work_set(warmdown)
    progression_2.append(workout)

progression = [val for pair in zip(
    progression_1, progression_2) for val in pair]

plan.add_progression("B", progression)

# Day C

start_dur = 30
progress = 5
work_week = 0
multiplier = 0

progression = []

for week in range(plan.length):

    rest = rest_week(week, plan.length)

    workout = Workout(rest)

    if not rest:
        if week > 0 and (work_week + 1) % 3 == 0 and multiplier < 2:
            multiplier += 1

        work_week += 1
        duration = start_dur + multiplier * progress

    else:
        duration = start_dur + multiplier * progress - 5

    workset = WorkSet(1)
    workset.add_exercise(Exercise("Easy", duration))
    workout.add_work_set(workset)
    progression.append(workout)
    plan.add_progression("C", progression)

for day in plan.progressions:
    print(day)
    for week in plan.progressions[day]:
        print(week)
