from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required

DISTANCES = [('5k', '5k'),
             ('10k', '10k'),
             ('half', 'Half Marathon'),
             ('full', 'Full Marathon')
             ]

EVENTS = [("2017 Big Fun Run Glasgow", "2017 Big Fun Run Glasgow"),
          ("2017 Dog Jog Glasgow", "2017 Dog Jog Glasgow"),
          ("2017 Dog Jog Edinburgh", "2017 Dog Jog Edinburgh"),
          ("2017 Big Fun Run Edinburgh", "2017 Big Fun Run Edinburgh"),
          ("2017 Big Fun Run Leeds", "2017 Big Fun Run Leeds"),
          ("2017 Dog Jog Leeds", "2017 Dog Jog Leeds"),
          ("2017 Big Fun Run Nottingham", "2017 Big Fun Run Nottingham"),
          ("2017 Dog Jog Nottingham", "2017 Dog Jog Nottingham"),
          ("2017 Big Fun Run Liverpool", "2017 Big Fun Run Liverpool"),
          ("2017 Dog Jog Liverpool", "2017 Dog Jog Liverpool"),
          ("2017 Big Fun Run Sheffield", "2017 Big Fun Run Sheffield"),
          ("2017 Dog Jog Sheffield", "2017 Dog Jog Sheffield"),
          ("2017 Big Fun Run Derby", "2017 Big Fun Run Derby"),
          ("2017 Dog Jog Derby", "2017 Dog Jog Derby"),
          ("2017 Big Fun Run Manchester", "2017 Big Fun Run Manchester"),
          ("2017 Dog Jog Manchester", "2017 Dog Jog Manchester"),
          ("2017 Big Fun Run Birmingham", "2017 Big Fun Run Birmingham"),
          ("2017 Dog Jog Birmingham", "2017 Dog Jog Birmingham"),
          ("2017 Big Fun Run Coventry", "2017 Big Fun Run Coventry"),
          ("2017 Dog Jog Coventry", "2017 Dog Jog Coventry"),
          ("2017 Scottish 10K", "2017 Scottish 10K"),
          ("2017 Scottish Half Marathon", "2017 Scottish Half Marathon"),
          ("2017 BMF Kids Kilometre", "2017 BMF Kids Kilometre"),
          ("2017 BMF 1.5K Junior Race", "2017 BMF 1.5K Junior Race"),
          ("2017 BMF 2K Junior Race", "2017 BMF 2K Junior Race"),
          ("2017 BMF Junior 5K", "2017 BMF Junior 5K"),
          ("2017 BMF Supersonic 10K", "2017 BMF Supersonic 10K"),
          ("2017 BMF Supernova 5K", "2017 BMF Supernova 5K"),
          ("2017 Bournemouth Half Marathon", "2017 Bournemouth Half Marathon"),
          ("2017 Bournemouth Marathon", "2017 Bournemouth Marathon"),
          ("2017 Big Fun Run Ipswich", "2017 Big Fun Run Ipswich"),
          ("2017 Dog Jog Ipswich", "2017 Dog Jog Ipswich"),
          ("2017 Big Fun Run Milton Keynes", "2017 Big Fun Run Milton Keynes"),
          ("2017 Dog Jog Milton Keynes", "2017 Dog Jog Milton Keynes"),
          ("2017 Big Fun Run Newcastle", "2017 Big Fun Run Newcastle"),
          ("2017 Big Fun Run London (Crystal Palace Park)",
           "2017 Big Fun Run London (Crystal Palace Park)"),
          ("2017 Dog Jog London (Crystal Palace Park)",
           "2017 Dog Jog London (Crystal Palace Park)"),
          ("2017 Big Fun Run London (Victoria Park)",
           "2017 Big Fun Run London (Victoria Park)"),
          ("2017 Dog Jog London (Victoria Park)",
           "2017 Dog Jog London (Victoria Park)"),
          ("2017 Men's 10K Edinburgh", "2017 Men's 10K Edinburgh"),
          ("2017 Supernova Kelpies - Friday", "2017 Supernova Kelpies - Friday"),
          ("2017 Supernova Kelpies - Saturday",
           "2017 Supernova Kelpies - Saturday"),
          ("2017 Supernova Kelpies - Sunday", "2017 Supernova Kelpies - Sunday"),
          ("2018 Supernova London", "2018 Supernova London"),
          ("2018 Kilomathon Scotland 13.1k", "2018 Kilomathon Scotland 13.1k"),
          ("2018 Mini Kilo Scotland 2.62k", "2018 Mini Kilo Scotland 2.62k"),
          ("2018 Kilomathon Scotland 6.5k", "2018 Kilomathon Scotland 6.5k"),
          ("2018 EMF 10k", "2018 EMF 10k"),
          ("2018 EMF 5k", "2018 EMF 5k"),
          ("2018 EMF Junior 5K", "2018 EMF Junior 5K"),
          ("2018 EMF Kids Kilometre", "2018 EMF Kids Kilometre"),
          ("2018 EMF 1.5k Junior Race", "2018 EMF 1.5k Junior Race"),
          ("2018 EMF 2k Junior Race", "2018 EMF 2k Junior Race"),
          ("2018 Edinburgh Half Marathon", "2018 Edinburgh Half Marathon"),
          ("2018 Edinburgh Marathon", "2018 Edinburgh Marathon"),
          ("2018 EMF Hairy Haggis Team Relay", "2018 EMF Hairy Haggis Team Relay"),
          ("2018 Men's 10K Glasgow", "2018 Men's 10K Glasgow"),
          ("2018 BMF Kids Kilometre", "2018 BMF Kids Kilometre"),
          ("2018 BMF 1.5K Junior Race", "2018 BMF 1.5K Junior Race"),
          ("2018 BMF 2K Junior Race", "2018 BMF 2K Junior Race"),
          ("2018 BMF Junior 5K", "2018 BMF Junior 5K"),
          ("2018 BMF Supersonic 10K", "2018 BMF Supersonic 10K"),
          ("2018 BMF Supernova 5K", "2018 BMF Supernova 5K"),
          ("2018 Bournemouth Half Marathon", "2018 Bournemouth Half Marathon"),
          ("2018 Bournemouth Marathon", "2018 Bournemouth Marathon"),
          ("2018 Men's 10K Edinburgh", "2018 Men's 10K Edinburgh"),
          ("2018 Supernova Kelpies - Friday", "2018 Supernova Kelpies - Friday"),
          ("2018 Supernova Kelpies - Saturday",
           "2018 Supernova Kelpies - Saturday"),
          ("2018 Supernova Kelpies - Sunday", "2018 Supernova Kelpies - Sunday"),
          ]

LEVELS = [('beg', 'Beginner'),
          ('int', 'Intermediate'),
          ('adv', 'Advanced')
          ]


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    event = SelectField('Select your event',
                        default="2017 Big Fun Run Glasgow",
                        choices=EVENTS)

    level = SelectField('What is your current level?',
                        default='Beginner',
                        choices=LEVELS)

    # days_per_week = SelectField('How many days a week can you train?',
    #                             default='3',
    #                             choices=[('1', '1'), ('2', '2'), ('3', '3')])

    submit = SubmitField('Submit')
