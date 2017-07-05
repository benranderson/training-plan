from flask import render_template, url_for
from . import main
from .forms import PlanForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PlanForm()
    if form.validate_on_submit():
        return render_template('plan.html')
    return render_template('index.html', form=form)