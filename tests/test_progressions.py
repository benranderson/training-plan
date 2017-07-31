import pytest
import app.main.progressions as p


@pytest.mark.parametrize("week, plan_length, expected", [
    (0, 8, False),
    (1, 8, False),
    (2, 8, False),
    (3, 8, True),
    (4, 8, False),
    (5, 8, False),
    (6, 8, False),
    (7, 8, True),
    (0, 9, False),
    (1, 9, False),
    (2, 9, False),
    (3, 9, False),
    (4, 9, True),
    (5, 9, False),
    (6, 9, False),
    (7, 9, False),
    (8, 9, True),
])
def test_rest_week(week, plan_length, expected):
    assert p.rest_week(
        week, plan_length) == expected, "failed @ week {}".format(week)


@pytest.mark.parametrize("weeks, start, freq, max, expected", [
    (8, 25, 3, 35, [25, 25, 30, 25, 30, 35, 35, 30]),
    (9, 25, 3, 35, [25, 25, 30, 30, 25, 35, 35, 35, 30]),
])
def test_run_easy_progress(weeks, start, freq, max, expected):
    for i, week in enumerate(list(p.run_easy_progress(weeks, start, freq,
                                                      max))):
        assert str(expected[i]) in repr(
            week), "failed on {0} weeks test @ week {1}".format(weeks, i)


@pytest.mark.parametrize("weeks, start_week, step, reps_start, reps_freq, reps_max, fast_start, fast_freq, fast_max, expected", [
    (8, 0, 2, 5, 1, 8, 0.5, 2, 1, [
     (5, 0.5), (6, 0.5), (6, 0.75), (7, 0.75)]),
])
def test_interval_progress(weeks, start_week, step, reps_start, reps_freq,
                           reps_max, fast_start, fast_freq, fast_max,
                           expected):
    for i, week in enumerate(list(p.interval_progress(weeks, start_week, step,
                                                      reps_start, reps_freq,
                                                      reps_max, fast_start,
                                                      fast_freq, fast_max))):
        assert "{}x".format(expected[i][0]) in repr(
            week), "reps failed on {0} weeks test @ week {1}".format(weeks, i)
        assert "({}".format(expected[i][1]) in repr(
            week), "dur failed on {0} weeks test @ week {1}".format(weeks, i)


@pytest.mark.parametrize("weeks, start_week, step, reps_start, reps_freq, reps_max, expected", [
    (8, 1, 2, 6, 3, 8, [
     (6, 0.25), (6, 0.25), (8, 0.25), (8, 0.25)]),
])
def test_hillsprint_progress(weeks, start_week, step, reps_start, reps_freq,
                             reps_max, expected):
    for i, week in enumerate(list(p.hillsprint_progress(weeks, start_week, step,
                                                        reps_start, reps_freq,
                                                        reps_max))):
        assert "{}x".format(expected[i][0]) in repr(
            week), "reps failed on {0} weeks test @ week {1}".format(weeks, i)
        assert "({}".format(expected[i][1]) in repr(
            week), "dur failed on {0} weeks test @ week {1}".format(weeks, i)


def test_RunEasy_repr():
    run_easy = p.RunEasy(10)
    assert repr(run_easy) == "RunEasy(10)"


def test_Interval_duration():
    interval = p.Interval(6, 1, 0.25)
    assert interval.duration == 27.5


def test_HillSprint_repr():
    hillsprint = p.HillSprint(6, 1)
    assert repr(hillsprint) == "6x HillSprint(1)"


def test_HillSprint_duration():
    hillsprint = p.HillSprint(6, 1)
    assert hillsprint.duration == 30
