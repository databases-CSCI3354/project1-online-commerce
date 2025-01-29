import pytest


def test_addition():
    assert 1 + 1 == 2


@pytest.mark.parametrize("input,expected", [(2, 4), (3, 9), (4, 16)])
def test_square(input, expected):
    assert input * input == expected
