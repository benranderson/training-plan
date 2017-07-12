from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required

DISTANCES = [('5k', '5k'),
             ('10k', '10k'),
             ('half', 'Half Marathon'),
             ('full', 'Full Marathon')
             ]

ABILITIES = [('beg', 'Beginner'),
             ('int', 'Intermediate'),
             ('adv', 'Advanced')
             ]


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    distance = SelectField('What is your race distance?',
                           default='5k',
                           choices=DISTANCES)

    ability = SelectField('What is your ability level?',
                          default='Beginner',
                          choices=ABILITIES)

    length = IntegerField('Plan length in weeks', validators=[Required()])

    days_per_week = SelectField('Number of training days per week',
                                default='3',
                                choices=[('1', '1'), ('2', '2'), ('3', '3')])

    submit = SubmitField('Submit')
