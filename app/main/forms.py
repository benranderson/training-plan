from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    distance = StringField('What is your race distance?', default="5k", validators=[Required()])
    ability = StringField('What is your ability level?', default="Beginner", validators=[Required()])
    length = IntegerField('Plan length in weeks', validators=[Required()])
    submit = SubmitField('Submit')