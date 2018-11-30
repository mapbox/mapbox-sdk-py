import pytest
import responses

from mapbox import DirectionsMatrix
from mapbox.errors import MapboxDeprecationWarning


points = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -87, 36]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -86, 36]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -88, 37]}}]


def test_class_attrs():
    """Get expected class attr values"""
    serv = DirectionsMatrix()
    assert serv.api_name == 'directions-matrix'
    assert serv.api_version == 'v1'


def test_profile_invalid():
    """'jetpack' is not a valid profile."""
    with pytest.raises(ValueError):
        DirectionsMatrix(access_token='pk.test')._validate_profile('jetpack')


@pytest.mark.parametrize('profile', ['mapbox/driving', 'mapbox/cycling', 'mapbox/walking'])
def test_profile_valid(profile):
    """Profiles are valid"""
    assert profile == DirectionsMatrix(
        access_token='pk.test')._validate_profile(profile)


@pytest.mark.parametrize('annotations', [['distance'], ['duration'], ['distance', 'duration'], None])
def test_annotations_valid(annotations):
    """Annotations are valid"""
    assert annotations == DirectionsMatrix(
        access_token='pk.test')._validate_annotations(annotations)


@pytest.mark.parametrize('profile', ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking'])
def test_deprecated_profile(profile):
    """Profiles are deprecated"""
    service = DirectionsMatrix()
    with pytest.warns(MapboxDeprecationWarning):
        assert profile.replace('.', '/') == service._validate_profile(profile)


def test_null_query():
    service = DirectionsMatrix()
    assert service._make_query(None, None) == {}


def test_query():
    service = DirectionsMatrix()
    params = service._make_query([0, 3], [1, 2])
    assert params['sources'] == '0;3'
    assert params['destinations'] == '1;2'


@responses.activate
@pytest.mark.parametrize('waypoints', [points, [p['geometry'] for p in points], [p['geometry']['coordinates'] for p in points]])
@pytest.mark.parametrize('annotations', [['distance'], ['duration'], ['distance', 'duration', None]])
def test_matrix(waypoints, annotations):
    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/-87,36;-86,36;-88,37?access_token=pk.test',
        match_querystring=True,
        body='{"durations":[[0,4977,5951],[4963,0,9349],[5881,9317,0]]}',
        status=200,
        content_type='application/json')

    # We need a second response because of the difference in rounding between
    # Python 2 (leaves a '.0') and 3 (no unnecessary '.0').
    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/-87.0,36.0;-86.0,36.0;-88.0,37.0?access_token=pk.test',
        match_querystring=True,
        body='{"durations":[[0,4977,5951],[4963,0,9349],[5881,9317,0]]}',
        status=200,
        content_type='application/json')
    res = DirectionsMatrix(access_token='pk.test').matrix(waypoints)
    matrix = res.json()['durations']
    # 3x3 list
    assert len(matrix) == 3
    assert len(matrix[0]) == 3