import pytest

import responses

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

@pytest.mark.parametrize(
    'start, end',[('2016-03-22T00:00:00.000Z', None),
                ('2016-03-22T00:00:00.000Z', '2016-03-20T00:00:00.000Z'),
                ('2016-03-22T00:00:00.000Z', '2017-04-20T00:00:00.000Z')])
def test_period_invalid(start, end):
    with pytest.raises(errors.InvalidPeriodError):
        mapbox.Analytics(access_token='pk.test')._validate_period(start, end)

@pytest.mark.parametrize(
    'start, end', [('2016-03-22T00:00:00.000Z', '2016-03-24T00:00:00.000Z'),
                   (None, None)])
def test_period_valid(start, end):
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

def test_id_invalid():
    """id is required when resource type is other than accounts"""
    resource_type = 'tokens'
    id = None
    with pytest.raises(errors.InvalidId):
        mapbox.Analytics(access_token='pk.test')._validate_id(resource_type, id)

@pytest.mark.parametrize(
    'resource_type, id', [('accounts', None),
                   ('tokens', 'abc')])
def test_id_valid(resource_type, id):
    """id is not required when resource type is accounts"""
    assert id == mapbox.Analytics(access_token='pk.test')._validate_id(resource_type, id)

@responses.activate
def test_analytics():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/analytics/v1/accounts/sanjayb?access_token=pk.test&id=abc&period=2016-03-22T00%3A00%3A00.000Z%2C2016-03-24T00%3A00%3A00.000Z',
        match_querystring=True,
        body='{"key": "value"}',
        status=200)

    res = mapbox.Analytics(access_token='pk.test').analytics('accounts', 'sanjayb', 'abc', '2016-03-22T00:00:00.000Z', '2016-03-24T00:00:00.000Z')
    assert res.status_code == 200
