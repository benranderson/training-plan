import pytest
import itertools
from datetime import date

import app.main.builder as b


@pytest.mark.parametrize('start_date, num_weeks, start_week, step, expected', [
    (date(2017, 8, 16), 8, 0, 1, [
        (0, date(2017, 8, 16), 'prog'),
        (1, date(2017, 8, 23), 'prog'),
        (2, date(2017, 8, 30), 'prog'),
        (3, date(2017, 9, 6), 'rest'),
        (4, date(2017, 9, 13), 'prog'),
        (5, date(2017, 9, 20), 'prog'),
        (6, date(2017, 9, 27), 'prog'),
        (7, date(2017, 10, 4), 'race'),
    ]),
    (date(2017, 8, 16), 8, 1, 2, [
        (1, date(2017, 8, 23), 'prog'),
        (3, date(2017, 9, 6), 'rest'),
        (5, date(2017, 9, 20), 'prog'),
        (7, date(2017, 10, 4), 'race'),
    ]),
])
def test_plan_week_range(start_date, num_weeks, start_week, step, expected):
    assert list(b.plan_week_range(
        start_date, num_weeks, start_week, step)) == expected


@pytest.fixture
def plan():
    '''Returns an 8 week 5k Plan'''
    return b.Plan5k(date(2017, 8, 16), date(2017, 9, 30), '2018 EMF 5k')


def test_Plan_event_day_in_schedule(plan):
    assert repr(plan.schedule[0]) == repr(
        b.Workout(date(2017, 9, 30), 'Event Day'))


def test_Plan_event_date_property(plan):
    assert plan.event_date == '30 Sep 2017'


def test_Plan_beginner_plan(plan):
    plan.create_schedule('Beginner', [0])
    print(plan.schedule)


@pytest.mark.parametrize('now, weekday, expected', [
    (date(2017, 8, 16), 0, date(2017, 8, 21)),
    (date(2017, 8, 16), 2, date(2017, 8, 23)),
    (date(2017, 8, 16), 4, date(2017, 8, 25))
])
def test_determine_next_weekday(now, weekday, expected):
    assert b.determine_next_weekday(now, weekday) == expected


# def test_weekrange():
#     assert list(b.weekrange(date(2017, 8, 14), 4)) == [date(2017, 8, 14),
#                                                        date(2017, 8, 21),
#                                                        date(2017, 8, 28),
#                                                        date(2017, 9, 4)]


def test_mins_to_seconds_formatter():
    assert b.mins_to_seconds_formatter(0.5) == '30s'


def test_Exercise():
    ex = b.Exercise('RunEasy', 20)
    assert 'RunEasy' in repr(ex)


def test_WorkoutSet_add_exercise():
    ws = b.WorkoutSet(5)
    e = b.Exercise('RunFast', 1)
    ws.add_exercise(e)
    assert e in ws.exercises


@pytest.fixture
def workoutset():
    '''Returns a workout set'''
    ws = b.WorkoutSet(5)
    es = [b.Exercise('RunFast', 1), b.Exercise('RunEasy', 0.5)]
    for e in es:
        ws.add_exercise(e)
    return ws


def test_WorkoutSet_repr(workoutset):
    assert '5' in repr(workoutset)
    assert 'RunFast' in repr(workoutset)
    assert 'RunEasy' in repr(workoutset)


def test_WorkoutSet_duration(workoutset):
    assert workoutset.duration == 7.5


def test_Workout_add_workoutset(workoutset):
    w = b.Workout(date(2017, 8, 14), 'RunEasy')
    w.add_workoutset(workoutset)
    assert workoutset in w.workoutsets


@pytest.fixture
def workout(workoutset):
    '''Returns a workout set'''
    w = b.Workout(date(2017, 8, 14), 'RunEasy')
    w.add_workoutset(workoutset)
    return w


def test_Workout_repr(workout):
    assert '14 Aug 2017 - RunEasy' in repr(workout)


def test_Workout_str(workout):
    assert 'RunEasy' in str(workout)
    assert '5x [RunFast(1), RunEasy(0.5)]' in str(workout)


def test_Workout_duration(workout, workoutset):
    workout.add_workoutset(workoutset)
    assert workout.duration == 15


def test_Workout_formatting(workout):
    assert workout.color == '#2ECC40'
    assert workout.textColor == 'hsla(127, 63%, 15%, 1.0)'


def test_Progression_runeasy():
    p = b.Progression(date(2017, 8, 11), 8, func=b.create_runeasy)
    p.create('5k', 'Beginner', 0)
    expected = ['25', '25', '30', '25', '30', '35', '35', '30']
    for wk, dur in enumerate(expected):
        assert dur in str(p.sessions[wk]), "dur failed at week {}".format(wk)


@pytest.mark.xfail
def test_Progression_interval():
    p = b.Progression(date(2017, 8, 11), 8, 1, 2, func=b.create_intervals)
    p.create(5, 2, 8, 0.5, 1, 1)
    expected = [('5', '0.5'), ('6', '0.5'), ('6', '0.75'), ('7', '0.75')]
    for wk, wo in enumerate(expected):
        assert all(x in str(p.sessions[wk]) for x in wo
                   ), "dur failed at week {}".format(wk)

# def test_interval_progress():
#     start = date(2017, 8, 14)
#     expected = [b.Interval(date(2017, 8, 14), 5, 0.25, 1),
#                 b.Interval(date(2017, 8, 21), 6, 0.25, 1),
#                 b.Interval(date(2017, 8, 28), 6, 0.5, 1),
#                 b.Interval(date(2017, 9, 4), 6, 0.5, 1),
#                 b.Interval(date(2017, 9, 11), 7, 0.5, 1),
#                 b.Interval(date(2017, 9, 18), 7, 0.75, 1),
#                 b.Interval(date(2017, 9, 25), 8, 0.75, 1),
#                 b.Interval(date(2017, 10, 2), 8, 0.75, 1)]
#     assert str(list(b.interval_progress(start, 8))) == str(expected)


# def test_runeasy_progress():
#     start = date(2017, 8, 14)
#     expected = [b.Run(date(2017, 8, 14), 25),
#                 b.Run(date(2017, 8, 21), 25),
#                 b.Run(date(2017, 8, 28), 30),
#                 b.Run(date(2017, 9, 4), 25),
#                 b.Run(date(2017, 9, 11), 30),
#                 b.Run(date(2017, 9, 18), 30),
#                 b.Run(date(2017, 9, 25), 35),
#                 b.Run(date(2017, 10, 2), 35)]
#     assert str(list(b.runeasy_progress(start, 8))) == str(expected)


# def test_hillsprint_progress():
#     start = date(2017, 8, 14)
#     expected = [b.HillSprint(date(2017, 8, 14), 6, 0.25),
#                 b.HillSprint(date(2017, 8, 21), 6, 0.25),
#                 b.HillSprint(date(2017, 8, 28), 8, 0.25),
#                 b.HillSprint(date(2017, 9, 4), 6, 0.25),
#                 b.HillSprint(date(2017, 9, 11), 8, 0.25),
#                 b.HillSprint(date(2017, 9, 18), 10, 0.25),
#                 b.HillSprint(date(2017, 9, 25), 10, 0.25),
#                 b.HillSprint(date(2017, 10, 2), 8, 0.25)]
#     assert str(list(b.hillsprint_progress(start, 8))) == str(expected)


# testdata = [
#     (b.Plan('2018 EMF 5k', 'Beginner', date(2018, 3, 30)), {
#         'repr': '8 week Beginner Plan for the 2018 EMF 5k',
#         'start_date': date(2018, 4, 2),
#         'length': 8
#     })
# ]

# @pytest.fixture
# def plan():
#     '''Returns an 8 week Beginner 5k Plan'''
#     return Plan("2018 EMF 5k", "Beginner", date(2018, 3, 30))


# @pytest.mark.parametrize('plan,expected', testdata)
# def test_Plan_repr(plan, expected):
#     assert repr(plan) == expected['repr']


# @pytest.mark.parametrize('plan,expected', testdata)
# def test_Plan_length(plan, expected):
#     assert plan.length == expected['length']


# @pytest.mark.parametrize('days,expected', [
#     ([0, 2], None)
# ])
# def test_Plan_create_schedule(days, expected):
#     p = b.Plan('2018 EMF 5k', 'Beginner', date(2018, 3, 30))
#     p.create_schedule(days)
#     print(p.schedule)
    # assert p.schedule = expected


# @pytest.mark.parametrize("weeks, start_week, step, reps_start, reps_freq, reps_max, fast_start, fast_freq, fast_max, expected", [
#     (8, 0, 2, 5, 1, 8, 0.5, 2, 1, [
#      (5, 0.5), (6, 0.5), (6, 0.75), (7, 0.75)]),
# ])
# def test_interval_progress(weeks, start_week, step, reps_start, reps_freq,
#                            reps_max, fast_start, fast_freq, fast_max,
#                            expected):
#     for i, week in enumerate(list(p.interval_progress(weeks, start_week, step,
#                                                       reps_start, reps_freq,
#                                                       reps_max, fast_start,
#                                                       fast_freq, fast_max))):
#         assert "{}x".format(expected[i][0]) in repr(
#             week), "reps failed on {0} weeks test @ week {1}".format(weeks, i)
#         assert "({}".format(expected[i][1]) in repr(
#             week), "dur failed on {0} weeks test @ week {1}".format(weeks, i)

# def test_Plan_repr(plan):
#     assert repr(
#         plan) == "8 week Beginner Plan for the 2018 EMF 5k"


# def test_Plan_determine_start_date(plan):
#     assert plan.determine_start_date() == date(2018, 4, 2)
#     assert plan.start_date == date(2018, 4, 2)


# def test_Plan_determine_schedule_weeks(plan):
#     assert len(plan.determine_schedule_weeks()) == 8
#     assert len(plan.schedule_weeks) == 8
#     for week in plan.schedule_weeks:
#         assert len(week) == 7


# def test_Plan_weeks_to_event(plan):
#     assert plan.weeks_to_event == 8


# def test_Plan_add_progression_to_schedule(plan):
#     day = 0
#     progression = [25, 25, 25, 25]
#     plan.add_progression_to_schedule(day, progression)
#     assert len(plan.schedule) == 4


# @pytest.mark.parametrize("week, plan_length, expected", [
#     (0, 8, False),
#     (1, 8, False),
#     (2, 8, False),
#     (3, 8, True),
#     (4, 8, False),
#     (5, 8, False),
#     (6, 8, False),
#     (7, 8, True),
#     (0, 9, False),
#     (1, 9, False),
#     (2, 9, False),
#     (3, 9, False),
#     (4, 9, True),
#     (5, 9, False),
#     (6, 9, False),
#     (7, 9, False),
#     (8, 9, True),
# ])
# def test_rest_week(week, plan_length, expected):
#     assert p.rest_week(
#         week, plan_length) == expected, "failed @ week {}".format(week)


# @pytest.mark.parametrize("weeks, start, freq, max, expected", [
#     (8, 25, 3, 35, [25, 25, 30, 25, 30, 35, 35, 30]),
#     (9, 25, 3, 35, [25, 25, 30, 30, 25, 35, 35, 35, 30]),
# ])
# def test_run_easy_progress(weeks, start, freq, max, expected):
#     for i, week in enumerate(list(p.run_easy_progress(weeks, start, freq,
#                                                       max))):
#         assert str(expected[i]) in repr(
#             week), "failed on {0} weeks test @ week {1}".format(weeks, i)


# @pytest.mark.parametrize("weeks, start_week, step, reps_start, reps_freq, reps_max, fast_start, fast_freq, fast_max, expected", [
#     (8, 0, 2, 5, 1, 8, 0.5, 2, 1, [
#      (5, 0.5), (6, 0.5), (6, 0.75), (7, 0.75)]),
# ])
# def test_interval_progress(weeks, start_week, step, reps_start, reps_freq,
#                            reps_max, fast_start, fast_freq, fast_max,
#                            expected):
#     for i, week in enumerate(list(p.interval_progress(weeks, start_week, step,
#                                                       reps_start, reps_freq,
#                                                       reps_max, fast_start,
#                                                       fast_freq, fast_max))):
#         assert "{}x".format(expected[i][0]) in repr(
#             week), "reps failed on {0} weeks test @ week {1}".format(weeks, i)
#         assert "({}".format(expected[i][1]) in repr(
#             week), "dur failed on {0} weeks test @ week {1}".format(weeks, i)


# @pytest.mark.parametrize("weeks, start_week, step, reps_start, reps_freq, reps_max, expected", [
#     (8, 1, 2, 6, 3, 8, [
#      (6, 0.25), (6, 0.25), (8, 0.25), (8, 0.25)]),
# ])
# def test_hillsprint_progress(weeks, start_week, step, reps_start, reps_freq,
#                              reps_max, expected):
#     for i, week in enumerate(list(p.hillsprint_progress(weeks, start_week, step,
#                                                         reps_start, reps_freq,
#                                                         reps_max))):
#         assert "{}x".format(expected[i][0]) in repr(
#             week), "reps failed on {0} weeks test @ week {1}".format(weeks, i)
#         assert "({}".format(expected[i][1]) in repr(
#             week), "dur failed on {0} weeks test @ week {1}".format(weeks, i)


# def test_RunEasy_repr():
#     run_easy = p.RunEasy(10)
#     assert repr(run_easy) == "RunEasy(10)"


# def test_Interval_duration():
#     interval = p.Interval(6, 1, 0.25)
#     assert interval.duration == 27.5


# def test_HillSprint_repr():
#     hillsprint = p.HillSprint(6, 1)
#     assert repr(hillsprint) == "6x HillSprint(1)"


# def test_HillSprint_duration():
#     hillsprint = p.HillSprint(6, 1)
#     assert hillsprint.duration == 30
