import pytest


def test_pass():
    assert 1 == 1


def test_fail():
    assert 1 == 2


@pytest.mark.skip()
def test_skip():
    assert 1 == 1


def test_error(test):
    assert 1 == ""
