import datetime


def group_log_entries(user, year, month):
    '''
    Processes and regroups a list of workouts so they can be more easily
    used in the different calendar pages

    :param user: the user to filter the logs for
    :param year: year
    :param month: month

    :return: a dictionary with grouped logs by date and exercise
    '''

    workouts = Workout.query.filter_by(
        date__year=year, date__month=month).all()

    # There can be workout sessions without any associated log entries, so it is
    # not enough so simply iterate through the logs
    if day:
        filter_date = datetime.date(year, month, day)
        logs = WorkoutLog.objects.filter(user=user, date=filter_date)
        sessions = WorkoutSession.objects.filter(user=user, date=filter_date)

    else:
        logs = WorkoutLog.objects.filter(user=user,
                                         date__year=year,
                                         date__month=month)

        sessions = WorkoutSession.objects.filter(user=user,
                                                 date__year=year,
                                                 date__month=month)

    logs = logs.order_by('date', 'id')
    out = cache.get(cache_mapper.get_workout_log_list(log_hash))
    # out = OrderedDict()

    if not out:
        out = OrderedDict()

        # Logs
        for entry in logs:
            if not out.get(entry.date):
                out[entry.date] = {'date': entry.date,
                                   'workout': entry.workout,
                                   'session': entry.get_workout_session(),
                                   'logs': OrderedDict()}

            if not out[entry.date]['logs'].get(entry.exercise):
                out[entry.date]['logs'][entry.exercise] = []

            out[entry.date]['logs'][entry.exercise].append(entry)

        # Sessions
        for entry in sessions:
            if not out.get(entry.date):
                out[entry.date] = {'date': entry.date,
                                   'workout': entry.workout,
                                   'session': entry,
                                   'logs': {}}

        cache.set(cache_mapper.get_workout_log_list(log_hash), out)
    return out
