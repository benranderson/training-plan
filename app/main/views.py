from flask import request, render_template, url_for, Response
from datetime import date, timedelta
import json

from . import main
from .. import db
from .forms import PlanForm, LEVELS, DAYS
from .builder import get_plan
from ..models import Workout


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
            wo = Workout(workout.date, str(workout),
                         workout.color, workout.textColor)
            db.session.add(wo)
            db.session.commit()

        # plan.create_cals()

        return render_template('plan.html', plan=plan)
    return render_template('index.html', form=form)


@main.route('/data')
def data():
    calendar = []
    workouts = Workout.query.all()
    for row in workouts:
        calendar.append({'title': row.title,
                         'start': row.date,
                         'color': row.color,
                         'textColor': row.textColor})
    return Response(json.dumps(calendar))
