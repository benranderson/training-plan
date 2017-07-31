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


def test_Plan_add_progression_to_schedule(plan):
    day = 0
    progression = [25, 25, 25, 25]
    plan.add_progression_to_schedule(day, progression)
    assert len(plan.schedule) == 4


# def test_Plan_create_schedule_1_day(plan):
#     days = [0]
#     plan.create_schedule(days)
#     for i in range(0, len(plan.schedule), 7):
#         assert "RunEasy" in plan.schedule[i:i + 7][0]


# def test_Plan_create_schedule_3_days(plan):
#     days = [0, 2, 4]
#     plan.create_schedule(days)
#     for date, workout in plan.schedule.items():
#         assert "RunEasy" in repr(workout)
