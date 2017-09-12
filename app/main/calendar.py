from calendar import HTMLCalendar
from datetime import date
from itertools import groupby


class WorkoutCalendar(HTMLCalendar):
    '''
    A calendar renderer, see this blog entry for details:
    * http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
    '''

    def __init__(self, workouts, *args, **kwargs):
        super(WorkoutCalendar, self).__init__(*args, **kwargs)
        self.workouts = workouts

    def formatday(self, day, weekday):

        # days belonging to last or next month are rendered empty
        if day == 0:
            return self.day_cell('noday', '&nbsp;')

        date_obj = date(self.year, self.month, day)
        cssclass = self.cssclasses[weekday]
        if date.today() == date_obj:
            cssclass += ' today'

        # There are no logs for this day, doesn't need special attention
        if date_obj not in self.workouts:
            return self.day_cell(cssclass, day)

        # Day with a log
        entry = self.workouts.get(date_obj)

        formatted_date = date_obj.strftime('%d %b %Y')
        body = []
        # exercises_html = "<br />".join(entry.exercises.split("\n"))
        body.append(repr(day))
        body.append('<button type="button" class="btn btn-{0} btn-block"'
                    'data-toggle="modal" data-target="#workoutModal"'
                    'data-title="{1} Workout on {2}" data-description="{3}">'
                    '{1}</button>'.format(entry.category,
                                          entry.category.capitalize(),
                                          formatted_date,
                                          entry.content))
        return self.day_cell(cssclass, '{0}'.format(''.join(body)))

    def formatmonth(self, year, month, withyear=False):
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
        return '<td class="{0}" style="vertical-align: center;">{1}</td>'.format(cssclass, body)
