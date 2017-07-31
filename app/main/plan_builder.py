import datetime
import calendar

from .events import events_dict
from .progressions import run_easy_progress, interval_progress


class Plan:

    def __init__(self, event, level, current_date=datetime.date.today()):
        self.event = event
        self.distance, self.event_date = events_dict[self.event]
        self.distance = "5k"  # temporary
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
        days_ahead = 0 - self.current_date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return self.current_date + datetime.timedelta(days_ahead)

    def determine_schedule_weeks(self):
        days_ahead = 6 - self.event_date.weekday()
        end_date = self.event_date + datetime.timedelta(days_ahead)
        days = [self.start_date + datetime.timedelta(n)
                for n in range(int((end_date - self.start_date).days) + 1)]
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    def add_progression_to_schedule(self, day, progression):
        for step, week in zip(progression, self.schedule_weeks):
            self.schedule[week[day]] = step

    def create_schedule(self, days):

        builders = {"5k": {"Beginner": self.builder_5k_beg}}

        progressions = builders[self.distance][self.level](
            len(self.schedule_weeks), len(days))

        for day, progression in zip(days, progressions):
            self.add_progression_to_schedule(day, progression)

    def builder_5k_beg(self, weeks, days):

        progressions = []

        if days > 0:
            progressions.append(list(run_easy_progress(weeks)))
        elif days > 1:
            progressions.append(list(interval_progress(weeks)))
        else:
            progressions.append(list(run_easy_progress(weeks)))

        return progressions

    def create_cals(self):
        year = 0
        month = 0
        for entry in self.schedule:
            if entry.year > year or entry.month > month:
                year = entry.year
                month = entry.month
                self.calendars.append(WorkoutCalendar(
                    self.schedule).formatmonth(year, month))


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
