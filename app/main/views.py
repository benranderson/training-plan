from flask import render_template, url_for
from . import main
from .forms import PlanForm, LEVELS, DAYS
from .plan_builder import Plan
import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm(datetime.date.today())
    if form.validate_on_submit():
        event = form.event.data
        level = dict(LEVELS).get(form.level.data)
        days = [int(day) for day in form.days.data]

        plan = Plan(event, level)
        plan.create_schedule(days)
        plan.create_cals()

        return render_template('plan.html', plan=plan)
    return render_template('index.html', form=form)
