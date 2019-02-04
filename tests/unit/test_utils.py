import warnings
from importlib import reload


import pytest


import openscm.utils


@pytest.fixture(scope="function")
def ensure_input_is_tuple_instance():
    # fresh import each time for counting number of calls
    reload(openscm.utils)
    yield openscm.utils.ensure_input_is_tuple


@pytest.fixture(scope="module")
def warn_message():
    yield "Converting input {} from string to tuple"


def test_convert_string_to_tuple_tuple_input(ensure_input_is_tuple_instance):
    with warnings.catch_warnings(record=True) as warn_tuple_input:
        ensure_input_is_tuple_instance(("test",))

    assert len(warn_tuple_input) == 0


def test_convert_string_to_tuple_tuple_forgot_comma(
    ensure_input_is_tuple_instance, warn_message
):
    tinp = "test"
    with warnings.catch_warnings(record=True) as warn_tuple_forgot_comma_input:
        ensure_input_is_tuple_instance(tinp)

    assert len(warn_tuple_forgot_comma_input) == 1
    assert str(warn_tuple_forgot_comma_input[0].message) == warn_message.format(tinp)


def test_convert_string_to_tuple_list_input(
    ensure_input_is_tuple_instance, warn_message
):
    with warnings.catch_warnings(record=True) as warn_list_input:
        ensure_input_is_tuple_instance(["test"])

    assert len(warn_list_input) == 0


def test_convert_string_to_tuple_str_input(
    ensure_input_is_tuple_instance, warn_message
):
    tinp1 = "test"
    with warnings.catch_warnings(record=True) as warn_tuple_str_input:
        ensure_input_is_tuple_instance(tinp1)
        ensure_input_is_tuple_instance("test 2")

    assert len(warn_tuple_str_input) == 1  # make sure only thrown once
    assert str(warn_tuple_str_input[0].message) == warn_message.format(tinp1)
