''' Utility Functions '''
import json
from datetime import timedelta


def next_weekday(now, weekday):
    '''
    datetime, int -> datetime
    '''
    days_ahead = weekday - now.weekday() + 7
    return now + timedelta(days_ahead)


def week_type(week, length):
    if week == (length - 1):
        return 'race'
    elif rest_week(week, length):
        return 'rest'
    else:
        return 'prog'


def rest_week(week, plan_length):
    '''
    int -> boolean

    Determine if current week is a rest week.

    Plans work on a 4 week block, with every 4th week being an easier week.
    Runner has at least 2 weeks, and a maximum of 5 weeks before they get an
    easier week.  So if they were on a 6 week plan they would only have an
    easier week on race week.

    Returns True if rest week and False if progression week.
    '''
    build_up = plan_length % 4
    if week <= build_up and build_up < 3:
        return False
    elif (week - build_up + 1) % 4 == 0:
        return True
    else:
        return False


def rest_duration(rest, dur):
    '''
    Return rest week duration based on whether rest duration reduction is applied as an absolute
    or % value
    '''
    if isinstance(rest, str):
        return (float(rest.strip('%')) / 100) * dur
    else:
        return dur - rest


def open_json(file_name):
    try:
        with open(file_name, 'r') as i:
            return json.load(i)
    except FileNotFoundError:
        raise FileNotFoundError('Check {} exists'.format(file_name))


class WorkoutEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            to_serialize = {
                'title': o.title,
                'start': o.date,
                'color': o.color,
                'textColor': o.textColor,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
