from flask import render_template, url_for
from . import main
from .forms import PlanForm, LEVELS, DAYS
from .plan_builder import Plan

import datetime

from .events import events_dict


@main.route('/', methods=['GET', 'POST'])
def index():
    # Filter events to only show future events and those in less than 12 months
    events = [(event, "{0} ({1})".format(event,
                                         info[1].strftime('%d %b %Y')))
              for (event, info) in events_dict.items()
              if info[1] > datetime.date.today()
              and info[1] < (datetime.date.today() +
                             datetime.timedelta(weeks=4 * 12))]
    form = PlanForm()
    form.event.choices = events
    if form.validate_on_submit():
        event = form.event.data
        level = dict(LEVELS).get(form.level.data)
        days = [int(day) for day in form.days.data]

        plan = Plan(event, level)
        plan.create_schedule(days)
        plan.create_cals()

        return render_template('plan.html', plan=plan)
    return render_template('index.html', form=form)
