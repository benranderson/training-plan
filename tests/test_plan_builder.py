import pytest
import itertools
from datetime import date

from app.main.plan_builder import Plan


@pytest.fixture
def plan():
    '''Returns an 8 week Beginner 5k Plan'''
    return Plan("2018 EMF 5k", "Beginner", date(2018, 3, 30))


def test_Plan_repr(plan):
    assert repr(
        plan) == "8 week Beginner Plan for the 2018 EMF 5k"


def test_Plan_determine_start_date(plan):
    assert plan.determine_start_date() == date(2018, 4, 2)
    assert plan.start_date == date(2018, 4, 2)


def test_Plan_determine_schedule_weeks(plan):
    assert len(plan.determine_schedule_weeks()) == 8
    assert len(plan.schedule_weeks) == 8
    for week in plan.schedule_weeks:
        assert len(week) == 7


def test_Plan_weeks_to_event(plan):
    assert plan.weeks_to_event == 8


# def test_Plan_builder_5k_beg(plan):
#     assert len(plan.builder_5k_beg(8, 1)) == 8


# def test_builder_5k_beg_day_A(plan):
#     expected = [25, 25, 30, 25, 30, 30, 30, 30, 25]
#     for i, week in enumerate(plan.schedule):
#         assert str(expected[i]) in repr(week["A"]), "week " + str(i)
