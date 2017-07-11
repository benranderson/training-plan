from flask import render_template, url_for
from . import main
from .forms import PlanForm
from .builder import Plan


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm()
    if form.validate_on_submit():
        distance = form.distance.data
        ability = form.ability.data
        length = int(form.length.data)
        days_per_week = int(form.days_per_week.data)
        plan = Plan(distance, ability, length, days_per_week)
        return render_template('plan.html', plan=plan)
    return render_template('index.html', form=form)
