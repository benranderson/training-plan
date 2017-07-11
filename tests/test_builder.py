import pytest
import itertools

import app.main.builder as builder


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
    assert builder.rest_week(week, plan_length) == expected


@pytest.mark.parametrize("plan_length, distance, ability, expected", [
    (0, 4, False),
    (1, 4, False),
    (2, 4, False),
    (3, 4, True),
    (0, 10, False),
    (1, 10, False),
    (5, 10, True),
])
def test_run_easy_progression(plan_length, distance, ability, expected):
    assert 


# @pytest.mark.parametrize("exercise, plan_length, start_conds, progress_conds, expected",
#     [
#         ("Easy", 4, (25, 1), (5, 0, 3), [(1, [("Easy", 25)]])
#     ]
#     )
# def test_progression(exercise, plan_length, start_conds, progress_conds, expected):
#     assert tuple(plan.progression(exercise, plan_length,
#                                   start_conds, progress_conds)) == expected
