import pytest
import responses

import mapbox


points = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -87.337875,
            36.539156]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -86.577791,
            36.722137
            ]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -88.247685,
            36.922175]}}]


def test_class_attrs():
    """Get expected class attr values"""
    serv = mapbox.Distance()
    assert serv.api_name == 'distances'
    assert serv.api_version == 'v1'


def test_profile_invalid():
    """'jetpack' is not a valid profile."""
    with pytest.raises(ValueError):
        mapbox.Distance(access_token='pk.test')._validate_profile('jetpack')


@pytest.mark.parametrize('profile', ['driving', 'cycling', 'walking'])
def test_profile_valid(profile):
    """Profiles are valid"""
    assert profile == mapbox.Distance(
        access_token='pk.test')._validate_profile(profile)


@responses.activate
def test_distance():

    responses.add(
        responses.POST,
        'https://api.mapbox.com/distances/v1/mapbox/driving?access_token=pk.test',
        match_querystring=True,
        body='{"durations":[[0,4977,5951],[4963,0,9349],[5881,9317,0]]}',
        status=200,
        content_type='application/json')

    res = mapbox.Distance(access_token='pk.test').distances(points)
    assert res.status_code == 200
    assert list(res.json().keys()) == ["durations", ]


@responses.activate
def test_distances_matrix():

    responses.add(
        responses.POST,
        'https://api.mapbox.com/distances/v1/mapbox/driving?access_token=pk.test',
        match_querystring=True,
        body='{"durations":[[0,4977,5951],[4963,0,9349],[5881,9317,0]]}',
        status=200,
        content_type='application/json')

    res = mapbox.Distance(access_token='pk.test').distances(points)
    matrix = res.json()['durations']
    # 3x3 list
    assert len(matrix) == 3
    assert len(matrix[0]) == 3
