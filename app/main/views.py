from flask import render_template, url_for
from . import main
from .forms import PlanForm
from .builder import plan_builder


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm()
    if form.validate_on_submit():
        distance = form.distance.data
        ability = form.ability.data
        length = form.length.data
        plan = plan_builder(distance, ability, length)
        return render_template('plan.html', plan=plan)
    return render_template('index.html', form=form)
