from flask import render_template, url_for
from . import main
from .forms import PlanForm, DISTANCES, ABILITIES
from .builder import Plan


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm()
    if form.validate_on_submit():
        distance = dict(DISTANCES).get(form.distance.data)
        ability = dict(ABILITIES).get(form.ability.data)
        length = int(form.length.data)
        days_per_week = int(form.days_per_week.data)
        plan = Plan(form.distance.data, form.ability.data, length,
                    days_per_week)
        return render_template('plan.html', plan=plan, ability=ability,
                               distance=distance)
    return render_template('index.html', form=form)
