class WorkoutCalendar(HTMLCalendar):
    '''
    A calendar renderer, see this blog entry for details:
    * http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
    '''
    def __init__(self, workout_logs, *args, **kwargs):
        super(WorkoutCalendar, self).__init__(*args, **kwargs)
        self.workout_logs = workout_logs

    def formatday(self, day, weekday):

        # days belonging to last or next month are rendered empty
        if day == 0:
            return self.day_cell('noday', '&nbsp;')

        date_obj = datetime.date(self.year, self.month, day)
        cssclass = self.cssclasses[weekday]
        if datetime.date.today() == date_obj:
            cssclass += ' today'

        # There are no logs for this day, doesn't need special attention
        if date_obj not in self.workout_logs:
            return self.day_cell(cssclass, day)

        # Day with a log, set background and link
        entry = self.workout_logs.get(date_obj)

        # Note: due to circular imports we use can't import the workout session
        # model to access the impression values directly, so they are hard coded
        # here.
        if entry['session']:
            # Bad
            if entry['session'].impression == '1':
                background_css = 'btn-danger'
            # Good
            elif entry['session'].impression == '3':
                background_css = 'btn-success'
            # Neutral
            else:
                background_css = 'btn-warning'

        else:
            background_css = 'btn-warning'

        url = reverse('manager:log:log', kwargs={'pk': entry['workout'].id})
        formatted_date = date_obj.strftime('%Y-%m-%d')
        body = []
        body.append('<a href="{0}" '
                    'data-log="log-{1}" '
                    'class="btn btn-block {2} calendar-link">'.format(url,
                                                                      formatted_date,
                                                                      background_css))
        body.append(repr(day))
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
