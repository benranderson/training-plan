import pytest
import itertools

from app.main.builder import Plan, WorkoutSet, Exercise, rest_week


@pytest.mark.parametrize("week, plan_length, expected", [
    (0, 4, False),
    (1, 4, False),
    (2, 4, False),
    (3, 4, True),
    (0, 10, False),
    (1, 10, False),
    (5, 10, True),
])
def test_rest_week(week, plan_length, expected):
    assert rest_week(week, plan_length) == expected

# Plan tests


@pytest.fixture
def fivek_beginner_plan():
    '''Returns a 5k Beginner plan instance'''
    return Plan("5k", "Beginner", 12, 3)


@pytest.mark.parametrize("plan, week, expected", [
    (Plan("5k", "Beginner", 12, 3), 0, 82.5),
])
def test_run_easy_progression(plan, week, expected):
    assert plan.calculate_duration_of_week(week) == expected


# WorkoutSet tests

def test_workout_set():

    workout_set = WorkoutSet(5)
    workout_set.add_exercise(Exercise("Fast", 0.5))
    workout_set.add_exercise(Exercise("Easy", 1))

    assert workout_set.calculate_duration() == 7.5

# @pytest.mark.parametrize("plan_length, distance, ability, expected", [
#     (0, 4, False),
#     (1, 4, False),
#     (2, 4, False),
#     (3, 4, True),
#     (0, 10, False),
#     (1, 10, False),
#     (5, 10, True),
# ])
# def test_run_easy_progression(plan_length, distance, ability, expected):
#     assert 1 == 1


# @pytest.mark.parametrize("exercise, plan_length, start_conds, progress_conds, expected",
#     [
#         ("Easy", 4, (25, 1), (5, 0, 3), [(1, [("Easy", 25)]])
#     ]
#     )
# def test_progression(exercise, plan_length, start_conds, progress_conds, expected):
#     assert tuple(plan.progression(exercise, plan_length,
#                                   start_conds, progress_conds)) == expected
