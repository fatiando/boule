"""
Test the function module
"""
import pytest

from ..function import function


@pytest.mark.parametrize("name", ["Gauss", "Green", "Newton"])
def test_function(name):
    "Check that function returns the right welcome message"
    assert function(name=name) == "Welcome to the project, {}!".format(name)
