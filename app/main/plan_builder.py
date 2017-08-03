import datetime
import calendar

from .events import events_dict
from .progressions import run_easy_progress, interval_progress, \
    hillsprint_progress, tempo_progress


class Plan:
    '''
    Represents running training plan for prescribed event and level.
    '''

    def __init__(self, event, level, current_date=datetime.date.today()):
        self.event = event
        self.distance, self.event_date = events_dict[self.event]
        self.level = level
        self.current_date = current_date

        self.start_date = self.determine_start_date()
        self.schedule_weeks = self.determine_schedule_weeks()
        self.weeks_to_event = len(self.schedule_weeks)

        self.schedule = {}
        self.calendars = []

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} Plan for the {2}".format(self.weeks_to_event,
                                                      self.level,
                                                      self.event)

    def determine_start_date(self):
        '''
        None -> datetime

        Return the start date of the training plan, which is assumed to be
        the next Monday following plan creation.
        '''

        days_ahead = 0 - self.current_date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return self.current_date + datetime.timedelta(days_ahead)

    def determine_schedule_weeks(self):
        '''
        None -> matrix

        Return a matrix (list of lists) representing training plan period.
        Each row represents a week; week entries are datetime.date values.
        '''

        days_ahead = 6 - self.event_date.weekday()
        end_date = self.event_date + datetime.timedelta(days_ahead)
        days = [self.start_date + datetime.timedelta(n)
                for n in range(int((end_date - self.start_date).days) + 1)]
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    def add_progression_to_schedule(self, day, progression):
        '''
        int, list -> None

        Populates plan schedule with given progression on specified day.
        '''
        for step, week in zip(progression, self.schedule_weeks):
            self.schedule[week[day]] = step

    def create_schedule(self, days):
        '''
        list -> None

        Creates plan schedule based on prescribed list of training days.
        '''

        def builder_dict(distance, level, weeks, days):
            distance_dict = {
                "5k": {"Beginner": self.builder_5k_beg,
                       "Intermediate": self.builder_5k_int,
                       "Advanced": self.builder_5k_beg},
                "10k": {"Beginner": self.builder_5k_beg,
                        "Intermediate": self.builder_5k_beg,
                        "Advanced": self.builder_5k_beg},
                "half": {"Beginner": self.builder_5k_beg,
                         "Intermediate": self.builder_5k_beg,
                         "Advanced": self.builder_5k_beg},
                "full": {"Beginner": self.builder_5k_beg,
                         "Intermediate": self.builder_5k_beg,
                         "Advanced": self.builder_5k_beg}
            }.get(distance, None)

            return distance_dict[level](weeks, days)

        progressions = builder_dict(
            self.distance, self.level, len(self.schedule_weeks), len(days))

        for day, progression in zip(days, progressions):
            self.add_progression_to_schedule(day, progression)

        # Populate schedule with race day
        self.schedule[self.event_date] = "RACE DAY!"

    def builder_5k_beg(self, weeks, days):
        '''
        int, int -> matrix

        Return matrix (list of lists) representing 5k Beginner progressions.
        Based on specified number of weeks and for specified number of training
        days a week.
        '''

        progressions = []

        if days > 0:
            progressions.append(list(run_easy_progress(weeks)))
        if days > 1:
            ints = list(interval_progress(weeks, start_week=0, step=2))
            hills = list(hillsprint_progress(weeks, start_week=1, step=2))
            progress = [val for pair in zip(ints, hills) for val in pair]
            progressions.append(progress)
        if days > 2:
            progressions.append(list(run_easy_progress(weeks)))

        return progressions

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

    def create_cals(self):
        '''
        Create list of calendars to render schedule.
        '''

        year = datetime.date.today().year
        month = 0
        for entry in self.schedule:
            if entry.month > month:
                year = entry.year
                month = entry.month
                self.calendars.append(WorkoutCalendar(
                    self.schedule).formatmonth(year, month))


class WorkoutCalendar(calendar.HTMLCalendar):
    '''
    A calendar renderer.
    '''

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

        # Format race day
        if entry == "RACE DAY!":
            formatted_date = str(day)
            body = []
            body.append('<p> {0} </p>'.format(formatted_date))
            body.append(
                '<a class="btn btn-block {0} calendar-link">'.format('btn-info'))
            body.append(entry)
            return self.day_cell(cssclass, '{0}'.format(''.join(body)))

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
        return '<td class="{0}" style="vertical-align: top">{1}</td>'.format(cssclass, body)
