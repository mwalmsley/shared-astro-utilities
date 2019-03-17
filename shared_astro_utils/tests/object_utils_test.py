import pytest

from shared_astro_utils import object_utils

class SomeObject():

    def __init__(self, some_string, some_int, some_float):
        self.some_string = some_string
        self.some_int = some_int
        self.some_float = some_float
        
@pytest.fixture()
def some_string():
    return 'hello world'

@pytest.fixture()
def some_int():
    return 12

@pytest.fixture()
def some_float():
    return 14.

@pytest.fixture()
def some_object(some_string, some_int, some_float):
    return SomeObject(some_string, some_int, some_float)


def test_object_to_dict(some_object, some_string, some_int, some_float):
    some_dict = object_utils.object_to_dict(some_object)
    assert some_dict['some_string'] == some_string
    assert some_dict['some_int'] == some_int
    assert some_dict['some_float'] == some_float

