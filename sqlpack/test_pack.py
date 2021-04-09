import pytest
from . import pack

varmap = {
    "base_name": "AWS_CLOUDTRAIL_conn_EVENTS",
    "landing_table": "data.{base_name}_CONNECTION",
    "pipe": "data.{base_name}_PIPE",
}


@pytest.mark.parametrize(
    "find,found",
    [
        (
            "base_name",
            "base_name",
        ),  # no replacement occurs for variables without the swiggly {} brackets
        (
            "{not_in_varmap}",
            "{not_in_varmap}",
        ),  # no replacement occurs for string in swiggly{} brackets that is not a key in the varmap
    ],
)
def test_format_no_replacement(find, found):
    result = pack.format(find, varmap)
    assert result == found


@pytest.mark.parametrize(
    "find,found",
    [
        (
            "{base_name}",
            "AWS_CLOUDTRAIL_conn_EVENTS",
        )  # single replacement of a valid key in swiggly brackets by the respective value from the varmap
    ],
)
def test_format_single_replacement(find, found):
    result = pack.format(find, varmap)
    assert result == found


@pytest.mark.parametrize(
    "find,found",
    [
        (
            "{landing_table}",
            "data.AWS_CLOUDTRAIL_conn_EVENTS_CONNECTION",
        )  # recursive replacement of a valid key in swiggly brackets which also contains a valid key that needs to be replaced by the respective value from the varmap
    ],
)
def test_format_recursive_replacement(find, found):
    result = pack.format(find, varmap)
    assert result == found


@pytest.mark.parametrize(
    "find,found",
    [
        (
            "{base_name} is used in {landing_table}",
            "AWS_CLOUDTRAIL_conn_EVENTS is used in data.AWS_CLOUDTRAIL_conn_EVENTS_CONNECTION",
        )  # A single and a recursice replacement in a single line
    ],
)
def test_format_multiple_and_recursive_replacement(find, found):
    result = pack.format(find, varmap)
    assert result == found
