from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Required
import datetime

from .events import EVENTS

LEVELS = [('beg', 'Beginner'),
          ('int', 'Intermediate'),
          ]

# ('adv', 'Advanced')

DAYS = [(0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')]


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    event = SelectField('Which event are you training for?',
                        default="2018 EMF 5k")

    level = SelectField('What is your current level?',
                        choices=LEVELS,
                        default='Beginner')

    days = SelectMultipleField('On which days would you like to train?',
                               choices=DAYS,
                               default=[0, 2, 4],
                               coerce=int)

    submit = SubmitField('Submit')

    def __init__(self, date):
        super(PlanForm, self).__init__()
        # Filter events to only show future events and those in less than 12 months
        self.event.choices = [(event, "{0} ({1})".format(event,
                                                         info[1].strftime('%d %b %Y')))
                              for (event, info) in EVENTS.items()
                              if info[1] > date and
                              info[1] < (date + datetime.timedelta(weeks=4 * 12))]
