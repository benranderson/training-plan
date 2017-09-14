from flask import request, render_template, url_for, redirect, Response
from datetime import date, timedelta
import json

from sqlalchemy import extract

from . import main
from .. import db
from .forms import PlanForm, LEVELS, DAYS
from .builder import get_plan
from ..models import Workout
from .calendar import WorkoutCalendar


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm(date.today())
    if form.validate_on_submit():
        event = form.event.data
        level = dict(LEVELS).get(form.level.data)
        days = [day for day in form.days.data]

        plan = get_plan(event, level)
        plan.create(days)

        Workout.query.delete()

        for workout in plan.schedule:
            wo = Workout(workout.date, workout.category, workout.duration,
                         str(workout))
            db.session.add(wo)
            db.session.commit()

        return redirect(url_for('main.calendar'))
        # return render_template('calendar.html')
    return render_template('index.html', form=form)


@main.route('/about/')
def about():
    """About page."""
    return render_template('about.html')


@main.route('/data')
def data():
    calendar = []
    workouts = Workout.query.all()
    for row in workouts:
        calendar.append({'title': '{0} min {1}'.format(int(row.duration),
                                                       row.category),
                         'start': str(row.date),
                         'color': row.color,
                         'textColor': row.textColor,
                         'description': row.content})
    return Response(json.dumps(calendar))


@main.route('/calendar', defaults={'year': date.today().year,
                                   'month': date.today().month})
@main.route('/calendar/<int:year>/<int:month>')
def calendar(year, month):
    '''
    Show a calendar with the training plan schedule
    '''

    page = request.args.get('page', 1, type=int)

    workouts_year = Workout.query.filter(extract('year', Workout.date) == year)
    workouts_month = workouts_year.filter(
        extract('month', Workout.date) == month)

    workouts = {}
    for workout in workouts_month:
        workouts[workout.date] = workout

    context = {}
    context['calendar'] = WorkoutCalendar(
        workouts).formatmonth(year, month)
    context['workouts'] = workouts_month
    context['current_year'] = year
    context['current_month'] = month

    return render_template('calendar.html', context=context)
