import pytest

import mapbox
from mapbox import errors

def test_resource_type_invalid():
    """'random' is not a valid resource type."""
    with pytest.raises(errors.InvalidResourceTypeError):
        mapbox.Analytics(access_token='pk.test')._validate_resource_type('random')

@pytest.mark.parametrize('resource_type', ['tokens', 'styles', 'accounts', 'tilesets'])
def test_profile_valid(resource_type):
    """Resource types are valid."""
    assert resource_type == mapbox.Analytics(
        access_token='pk.test')._validate_resource_type(resource_type)

def test_period_invalid():
	"""Providing only one timestamp is invalid."""
	with pytest.raises(errors.InvalidPeriodError):
		mapbox.Analytics(access_token='pk.test')._validate_period('2016-03-22T00:00:00.000Z', None)

def test_period_valid():
	"""Providing two valid timestamps."""
	start = '2016-03-22T00:00:00.000Z'
	end = '2016-03-24T00:00:00.000Z'
	period = start, end
	assert period == mapbox.Analytics(access_token='pk.test')._validate_period(start, end)

def test_username_invalid():
	"""Username is requird."""
	with pytest.raises(errors.InvalidUsernameError):
		mapbox.Analytics(access_token='pk.test')._validate_username(None)

def test_username_valid():
	"""Providing valid username"""
	user = 'abc'
	assert user == mapbox.Analytics(access_token='pk.test')._validate_username(user)
