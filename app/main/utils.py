''' Utility Functions '''
import json


def open_json(file_name):
    try:
        with open(file_name, 'r') as i:
            return json.load(i)
    except FileNotFoundError:
        raise FileNotFoundError('Check {} exists'.format(file_name))


def determine_next_weekday(now, weekday):
    '''
    datetime, int -> datetime
    '''
    days_ahead = weekday - now.weekday() + 7
    return now + datetime.timedelta(days_ahead)


def plan_week_range(start_date, num_weeks, start_week=0, step=1):
    # ('prog', 'rest', 'race')
    for wk in range(start_week, num_weeks, step):
        date = start_date + datetime.timedelta(weeks=wk)
        if wk == (num_weeks - 1):
            week_type = 'race'
        elif rest_week(wk, num_weeks):
            week_type = 'rest'
        else:
            week_type = 'prog'
        yield (wk, date, week_type)


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
