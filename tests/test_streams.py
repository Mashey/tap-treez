import pytest
from tap_treez.streams import set_latest_bookmark


def test_set_latest_bookmark():
    compared = '2021-02-11T16:01:44.007000Z'
    current = "2021-02-11T08:01:44.000-07:00"

    assert set_latest_bookmark(
        current, compared) == '2021-02-11T16:01:44.000-07:00'
