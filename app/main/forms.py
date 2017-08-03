from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Required

LEVELS = [('beg', 'Beginner'),
          ('int', 'Intermediate'),
          ]

# ('adv', 'Advanced')

DAYS = [('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')]


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    event = SelectField('Which event are you training for?',
                        choices=[],
                        default="2018 EMF 5k")

    level = SelectField('What is your current level?',
                        choices=LEVELS,
                        default='Beginner')

    days = SelectMultipleField('On which days would you like to train?',
                               choices=DAYS,
                               default=['0', '2', '4'])

    submit = SubmitField('Submit')
