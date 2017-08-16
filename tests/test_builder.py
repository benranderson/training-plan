import pytest
import itertools
from datetime import date

import app.main.builder as b


# @pytest.mark.parametrize('event, expected', [
#     (date(2017, 8, 16), 0, date(2017, 8, 21)),
#     (date(2017, 8, 16), 2, date(2017, 8, 23)),
#     (date(2017, 8, 16), 4, date(2017, 8, 25))
# ])
# def test_get_plan(now, weekday, expected):
#     assert b.determine_next_weekday(now, weekday) == expected


@pytest.fixture
def plan():
    '''Returns an 8 week Plan'''
    return b.Plan(date(2017, 8, 16), date(2017, 9, 30), "Event Day!")


def test_Plan_event_day_in_schedule(plan):
    assert repr(plan.schedule[0]) == repr(
        b.EventDay(date(2017, 9, 30), "Event Day!"))


def test_Plann_event_date_property(plan):
    assert plan.event_date == '30 Sep 2017'


@pytest.mark.parametrize('now, weekday, expected', [
    (date(2017, 8, 16), 0, date(2017, 8, 21)),
    (date(2017, 8, 16), 2, date(2017, 8, 23)),
    (date(2017, 8, 16), 4, date(2017, 8, 25))
])
def test_determine_next_weekday(now, weekday, expected):
    assert b.determine_next_weekday(now, weekday) == expected


def test_mins_to_seconds_formatter():
    assert b.mins_to_seconds_formatter(0.5) == '30s'


def test_Exercise():
    ex = b.Exercise('RunEasy', 20)
    assert 'RunEasy' in repr(ex)


def test_WorkoutSet():
    ex = [b.Exercise('RunFast', 1), b.Exercise('RunEasy', 0.5)]
    ws = b.WorkoutSet(5, ex)
    assert '5' in repr(ws)


def test_WorkoutSet_calculate_duration():
    ex = [b.Exercise('RunFast', 1), b.Exercise('RunEasy', 0.5)]
    ws = b.WorkoutSet(5, ex)
    assert ws.calculate_duration() == 7.5


def test_Workout():
    ex = [b.Exercise('RunFast', 1), b.Exercise('RunEasy', 0.5)]
    ws = [b.WorkoutSet(1, b.Exercise('RunEasy', 0.5)), b.WorkoutSet(5, ex)]

    w = b.Workout(date(2017, 8, 11), 'Intervals')
    w.workoutsets = ws

    print(w)


def test_Interval():
    interval = b.Interval(date(2017, 8, 11), 5, 1, 1)
    assert 'Interval' in repr(interval)


def test_Hillsprint():
    hillsprint = b.HillSprint(date(2017, 8, 11), 6, 0.25)
    assert 'HillSprint' in repr(hillsprint)


def test_interval_progress():
    start = date(2017, 8, 14)
    expected = [b.Interval(date(2017, 8, 14), 5, 0.25, 1),
                b.Interval(date(2017, 8, 21), 6, 0.25, 1),
                b.Interval(date(2017, 8, 28), 6, 0.5, 1),
                b.Interval(date(2017, 9, 4), 6, 0.5, 1),
                b.Interval(date(2017, 9, 11), 7, 0.5, 1),
                b.Interval(date(2017, 9, 18), 7, 0.75, 1),
                b.Interval(date(2017, 9, 25), 8, 0.75, 1),
                b.Interval(date(2017, 10, 2), 8, 0.75, 1)]
    assert str(list(b.interval_progress(start, 8))) == str(expected)


def test_runeasy_progress():
    start = date(2017, 8, 14)
    expected = [b.Run(date(2017, 8, 14), 25),
                b.Run(date(2017, 8, 21), 25),
                b.Run(date(2017, 8, 28), 30),
                b.Run(date(2017, 9, 4), 25),
                b.Run(date(2017, 9, 11), 30),
                b.Run(date(2017, 9, 18), 30),
                b.Run(date(2017, 9, 25), 35),
                b.Run(date(2017, 10, 2), 35)]
    assert str(list(b.runeasy_progress(start, 8))) == str(expected)


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
