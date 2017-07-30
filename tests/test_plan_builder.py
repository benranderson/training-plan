import pytest
import itertools
from datetime import date

from app.main.plan_builder import Plan, rest_week, RunEasy, Interval, HillSprint


@pytest.fixture
def plan():
    '''Returns a Plan instance with set start date'''
    return Plan("2018 EMF 5k", "Beginner", date(2018, 3, 30))


def test_Plan_repr(plan):
    assert repr(
        plan) == "8 week Beginner Plan for the 2018 EMF 5k"


def test_Plan_determine_start_date(plan):
    assert plan.determine_start_date() == date(2018, 4, 2)
    assert plan.start_date == date(2018, 4, 2)


# def test_Plan_calculate_weeks_to_event(plan):
#     event_date = date(2018, 5, 26)  # for reference
#     assert plan.calculate_weeks_to_event() == 8
#     assert plan.weeks_to_event == 8


def test_Plan_determine_schedule_weeks(plan):
    assert len(plan.determine_schedule_weeks()) == 8
    assert len(plan.schedule_weeks) == 8
    for week in plan.schedule_weeks:
        assert len(week) == 7


# def test_Plan_calculate_mins_training_per_week(plan):
#     plan.create_schedule()
#     assert plan.calculate_mins_training_per_week(0) == 55


# def test_Plan_add_progression_to_schedule():
#     plan = Plan("2018 EMF 5k", "Beginner")
#     plan.add_progression_to_schedule("A", [1, 2, 3])
#     assert plan.schedule == [{"A": 1},
#                              {"A": 2},
#                              {"A": 3}]
#     plan.add_progression_to_schedule("B", [1, 2, 3])
#     assert plan.schedule == [{"A": 1, "B": 1},
#                              {"A": 2, "B": 2},
#                              {"A": 3, "B": 3}]

def test_Plan_builder_5k_beg(plan):
    assert plan.schedule == 0


# def test_builder_5k_beg_day_A():
#     plan = Plan("2018 EMF 5k", "Beginner")
#     plan.builder_5k_beg()
#     expected = [25, 25, 30, 25, 30, 30, 30, 30, 25]
#     for i, week in enumerate(plan.schedule):
#         assert str(expected[i]) in repr(week["A"]), "week " + str(i)


# def test_Plan_builder_5k_beg_day_C():
#     plan = Plan("2018 EMF 5k", "Beginner")
#     plan.builder_5k_beg()
#     expected = [30, 30, 30, 30, 30, 30, 30, 35, 35]
#     for i, week in enumerate(plan.schedule):
#         assert str(expected[i]) in repr(week["C"]), "week " + str(i)


def test_RunEasy_repr():
    run_easy = RunEasy(10)
    assert repr(RunEasy(10)) == "Run for 10 minutes at an easy pace"


def test_Interval_duration():
    interval = Interval(6, 1, 0.25)
    assert interval.duration == 27.5


def test_HillSprint_repr():
    hillsprint = HillSprint(6, 1)
    assert repr(hillsprint) == "Run fast uphill for 1 minutes.  Repeat 6 times."


def test_HillSprint_duration():
    hillsprint = HillSprint(6, 1)
    assert hillsprint.duration == 30
