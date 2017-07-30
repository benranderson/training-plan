import datetime
import calendar

from .events import events_dict


class Plan:

    def __init__(self, event, level, current_date=datetime.date.today()):
        self.event = event
        self.distance = "5k"
        self.level = level
        self.current_date = current_date
        self.start_date = self.determine_start_date()
        self.schedule_weeks = self.determine_schedule_weeks()
        self.weeks_to_event = len(self.schedule_weeks)

        self.schedule = {}

        self.create_schedule()

        self.calendars = []

        year = 0
        month = 0
        for entry in self.schedule:
            if entry.year > year or entry.month > month:
                year = entry.year
                month = entry.month
                self.calendars.append(WorkoutCalendar(
                    self.schedule).formatmonth(year, month))

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} Plan for the {2}".format(self.weeks_to_event,
                                                      self.level,
                                                      self.event)

    def determine_start_date(self):
        days_ahead = 0 - self.current_date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return self.current_date + datetime.timedelta(days_ahead)

    def determine_schedule_weeks(self):
        event_date = events_dict[self.event]
        days_ahead = 6 - event_date.weekday()
        end_date = event_date + datetime.timedelta(days_ahead)
        days = [self.start_date + datetime.timedelta(n)
                for n in range(int((end_date - self.start_date).days) + 1)]
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    # def calculate_weeks_to_event(self):

    #     event_date = events[self.event]
    #     days_to_event = event_date - self.start_date

    #     return int(days_to_event.days / 7)

    # def add_progression_to_schedule(self, day, progression):

    #     for i, week in enumerate(progression):
    #         try:
    #             self.schedule[i][day] = week

    #         except IndexError:
    #             self.schedule.append({})
    #             self.schedule[i][day] = week

    # def calculate_mins_training_per_week(self, week):

    #     duration = 0

    #     for day, workout in self.schedule[week].items():
    #         duration += workout.duration

    #     return duration

    def create_schedule(self):

        builders = {"5k": {"Beginner": self.builder_5k_beg}}

        builders[self.distance][self.level]()

    def builder_5k_beg(self):

        days = [0, 2, 5]

        # Day A and C
        prog_A = []
        prog_C = []

        dur_A = 25
        dur_C = 30

        max = 35

        for week, dates in enumerate(self.schedule_weeks):

            # Day A
            date_A = dates[0]

            # Day C
            date_C = dates[5]

            if not rest_week(week, self.weeks_to_event):
                if (week + 1) % 6 == 0 and dur_C < max:
                    dur_C += 5
                elif (week + 1) % 3 == 0 and dur_A < max:
                    dur_A += 5

                self.schedule[date_A] = RunEasy(dur_A)
                self.schedule[date_C] = RunEasy(dur_C)

            else:
                if dur_C < dur_A:
                    self.schedule[date_A] = RunEasy(dur_A)
                    self.schedule[date_C] = RunEasy(dur_C - 5)
                else:
                    self.schedule[date_A] = RunEasy(dur_A - 5)
                    self.schedule[date_C] = RunEasy(dur_C)


class Workout:

    def __init__(self, date=datetime.date.today()):
        self.date = date


def rest_week(week, plan_length):
    ''' Return True if rest week and False if progression week '''
    build_up = plan_length % 4
    if week <= build_up and build_up < 3:
        return False
    elif (week - build_up + 1) % 4 == 0:
        return True
    else:
        return False


class RunEasy(Workout):

    def __init__(self, duration, date=datetime.date.today()):
        super().__init__(date)
        self.description = "Run Easy"
        self.duration = duration
        self.warmup = None
        self.warmdown = None
        self.background_css = 'btn-success'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run for {0} minutes at an easy pace".format(self.duration)


class Interval(Workout):

    def __init__(self, reps, fast, slow):
        super().__init__(datetime.date.today())
        self.description = "Intervals"
        self.reps = reps
        self.fast = fast
        self.slow = slow
        self.warmup = RunEasy(10)
        self.warmdown = RunEasy(10)
        self.duration = self.calculate_duration()
        self.background_css = 'btn-danger'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run fast for {0} minutes then run at an easy pace for {1} minutes.  Repeat {2} times.".format(self.fast, self.slow, self.reps)

    def calculate_duration(self):
        warmup = self.warmup.duration
        work = self.reps * (self.fast + self.slow)
        warmdown = self.warmdown.duration
        return warmup + work + warmdown


class HillSprint(Workout):

    def __init__(self, reps, sprint):
        super().__init__(datetime.date.today())
        self.description = "Hill Sprint"
        self.reps = reps
        self.sprint = sprint
        self.warmup = RunEasy(12)
        self.warmdown = RunEasy(12)
        self.duration = self.calculate_duration()
        self.background_css = 'btn-warning'

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''
        return "Run fast uphill for {0} minutes.  Repeat {1} times.".format(self.sprint, self.reps)

    def calculate_duration(self):
        warmup = self.warmup.duration
        work = self.reps * self.sprint
        warmdown = self.warmdown.duration
        return warmup + work + warmdown


class WorkoutCalendar(calendar.HTMLCalendar):

    def __init__(self, schedule):
        super(WorkoutCalendar, self).__init__()
        self.schedule = schedule

    def formatday(self, day, weekday):

        # days belonging to last or next month are rendered empty
        if day == 0:
            return self.day_cell('noday', '&nbsp;')

        date_obj = datetime.date(self.year, self.month, day)
        cssclass = self.cssclasses[weekday]
        if datetime.date.today() == date_obj:
            cssclass += ' today'

        # There are no logs for this day, doesn't need special attention
        if date_obj not in self.schedule:
            return self.day_cell(cssclass, day)

        entry = self.schedule.get(date_obj)
        background_css = entry.background_css
        formatted_date = str(day)
        body = []
        body.append('<p> {0} </p>'.format(formatted_date))
        body.append(
            '<a class="btn btn-block {0} calendar-link">'.format(background_css))

        body.append(repr(entry))
        body.append('</a>')

        return self.day_cell(cssclass, '{0}'.format(''.join(body)))

    def formatmonth(self, year, month):
        '''
        Format the table header. This is basically the same code from python's
        calendar module but with additional bootstrap classes
        '''
        self.year, self.month = year, month
        out = []
        out.append('<table class="month table table-bordered">\n')
        out.append(self.formatmonthname(year, month))
        out.append('\n')
        out.append(self.formatweekheader())
        out.append('\n')
        for week in self.monthdays2calendar(year, month):
            out.append(self.formatweek(week))
            out.append('\n')
        out.append('</table>\n')
        return ''.join(out)

    def day_cell(self, cssclass, body):
        '''
        Renders a day cell
        '''
        return '<td class="{0}" style="vertical-align: middle;">{1}</td>'.format(cssclass, body)

        # =============
        # Beginner Plan
        # =============

        # plan = Plan("5k", "Beginner", 24, 3)

        # Day A
        # # -----

        # start_dur = 25
        # progress = 5
        # freq = 3
        # max = 2
        # rest = -5

        # work_week = 0
        # multiplier = 0

        # progression = []

        # for week in range(plan.length):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:
        #         if week > 0 and (work_week + 1) % freq == 0 and multiplier < max:
        #             multiplier += 1

        #         work_week += 1
        #         duration = start_dur + multiplier * progress

        #     else:
        #         duration = start_dur + multiplier * progress + rest

        #     workset = WorkSet(1)
        #     workset.add_exercise(Exercise("Easy", duration))
        #     workout.add_work_set(workset)
        #     progression.append(workout)
        #     plan.add_progression("A", progression)

        # # Day B
        # # -----

        # # Interval progression

        # start_dur = 0.5
        # prog_dur = 0.25
        # mult_dur = 0

        # start_reps = 5
        # prog_reps = 1
        # mult_reps = 0

        # work_week = 0

        # progression_1 = []

        # for week in range(0, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         if work_week % 2 == 0:
        #             # Duration progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
        #                 mult_dur += 1

        #         else:
        #             # Reps progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
        #                 mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Fast", duration))
        #     workset.add_exercise(Exercise("Easy", 1))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmdown)

        #     progression_1.append(workout)

        # # Hills progression

        # start_dur = 0.25
        # prog_dur = 0
        # mult_dur = 0

        # start_reps = 6
        # prog_reps = 2
        # mult_reps = 0

        # work_week = 0

        # progression_2 = []

        # for week in range(1, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         # Reps progression
        #         if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
        #             mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Hills", duration))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmdown)
        #     progression_2.append(workout)

        # progression = [val for pair in zip(
        #     progression_1, progression_2) for val in pair]

        # plan.add_progression("B", progression)

        # # Day C

        # start_dur = 30
        # progress = 5
        # freq = 3
        # max = 1
        # rest = -5

        # work_week = 0
        # multiplier = 0

        # progression = []

        # for week in range(plan.length):

        #     rest = rest_week(week, plan.length)

        #     workout = Workout(rest)

        #     if not rest:
        #         if week > 0 and (work_week + 1) % freq == 0 and multiplier < max:
        #             multiplier += 1

        #         work_week += 1
        #         duration = start_dur + multiplier * progress

        #     else:
        #         duration = start_dur + multiplier * progress + rest

        #     workset = WorkSet(1)
        #     workset.add_exercise(Exercise("Easy", duration))
        #     workout.add_work_set(workset)
        #     progression.append(workout)
        #     plan.add_progression("C", progression)

        # # =============
        # # Intermediate Plan
        # # =============

        # plan = Plan("5k", "Intermediate", 24, 3)

        # # Day A
        # # -----

        # # Tempo progression

        # start_dur = 0.5
        # prog_dur = 0.25
        # mult_dur = 0

        # start_reps = 5
        # prog_reps = 1
        # mult_reps = 0

        # work_week = 0

        # progression_1 = []

        # for week in range(0, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         if work_week % 2 == 0:
        #             # Duration progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
        #                 mult_dur += 1

        #         else:
        #             # Reps progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
        #                 mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Fast", duration))
        #     workset.add_exercise(Exercise("Easy", 1))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmdown)

        #     progression_1.append(workout)

        # # Hills progression

        # start_dur = 0.25
        # prog_dur = 0
        # mult_dur = 0

        # start_reps = 6
        # prog_reps = 2
        # mult_reps = 0

        # work_week = 0

        # progression_2 = []

        # for week in range(1, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         # Reps progression
        #         if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
        #             mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Hills", duration))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmdown)
        #     progression_2.append(workout)

        # progression = [val for pair in zip(
        #     progression_1, progression_2) for val in pair]

        # plan.add_progression("B", progression)

        # # Day B
        # # -----

        # # Interval progression

        # start_dur = 0.5
        # prog_dur = 0.25
        # mult_dur = 0

        # start_reps = 5
        # prog_reps = 1
        # mult_reps = 0

        # work_week = 0

        # progression_1 = []

        # for week in range(0, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         if work_week % 2 == 0:
        #             # Duration progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_dur < 3:
        #                 mult_dur += 1

        #         else:
        #             # Reps progression
        #             if week > 0 and (work_week + 1) % 1 == 0 and mult_reps < 2:
        #                 mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Fast", duration))
        #     workset.add_exercise(Exercise("Easy", 1))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 10))
        #     workout.add_work_set(warmdown)

        #     progression_1.append(workout)

        # # Hills progression

        # start_dur = 0.25
        # prog_dur = 0
        # mult_dur = 0

        # start_reps = 6
        # prog_reps = 2
        # mult_reps = 0

        # work_week = 0

        # progression_2 = []

        # for week in range(1, plan.length, 2):

        #     rest = rest_week(week, plan.length)
        #     workout = Workout(rest)

        #     if not rest:

        #         # Reps progression
        #         if week > 0 and (work_week + 1) % 3 == 0 and mult_reps < 4:
        #             mult_reps += 1

        #         work_week += 1

        #     reps = start_reps + mult_reps * prog_reps
        #     duration = start_dur + mult_dur * prog_dur

        #     # Warmup set
        #     warmup = WorkSet(1)
        #     warmup.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmup)

        #     # Work Set
        #     workset = WorkSet(reps)
        #     workset.add_exercise(Exercise("Hills", duration))
        #     workout.add_work_set(workset)

        #     # Warmdown set
        #     warmdown = WorkSet(1)
        #     warmdown.add_exercise(Exercise("Easy", 12))
        #     workout.add_work_set(warmdown)
        #     progression_2.append(workout)

        # progression = [val for pair in zip(
        #     progression_1, progression_2) for val in pair]

        # plan.add_progression("B", progression)

        # # Day C

        # start_dur = 30
        # progress = 5
        # work_week = 0
        # multiplier = 0

        # progression = []

        # for week in range(plan.length):

        #     rest = rest_week(week, plan.length)

        #     workout = Workout(rest)

        #     if not rest:
        #         if week > 0 and (work_week + 1) % 3 == 0 and multiplier < 2:
        #             multiplier += 1

        #         work_week += 1
        #         duration = start_dur + multiplier * progress

        #     else:
        #         duration = start_dur + multiplier * progress - 5

        #     workset = WorkSet(1)
        #     workset.add_exercise(Exercise("Easy", duration))
        #     workout.add_work_set(workset)
        #     progression.append(workout)
        #     plan.add_progression("C", progression)

        # for day in plan.progressions:
        #     print(day)
        #     for week in plan.progressions[day]:
        #         print(week)
