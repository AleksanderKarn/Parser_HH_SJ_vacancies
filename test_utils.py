import pytest
from utils import get_top, sorting


@pytest.fixture
def coll():
    return [1, 5, 7, 4, 5, 6, 9, 8, 7]


def test_get_top(coll):
    assert get_top(coll, 3) == [9, 8, 7]


def test_sorting(coll):
    assert sorting(coll) == [9, 8, 7, 7, 6, 5, 5, 4, 1]
