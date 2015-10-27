import responses
import mapbox
import pytest


points = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -87.33787536621092,
            36.539156961321574]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -88.2476806640625,
            36.92217534275667]}}]


@responses.activate
def test_directions():
    with open('tests/moors.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').route(points)
    assert res.status_code == 200
    assert sorted(res.json()['routes'][0].keys()) == ['distance', 'duration', 'geometry', 'steps', 'summary']
    assert sorted(res.json().keys()) == ['destination', 'origin', 'routes', 'waypoints']


@responses.activate
def test_directions_geojson():
    with open('tests/moors.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').route(points)
    fc = res.geojson()
    assert fc['type'] == 'FeatureCollection'
    assert sorted(fc['features'][0]['properties'].keys()) == ['distance', 'duration', 'summary']
    assert fc['features'][0]['geometry']['type'] == "LineString"


def test_invalid_profile():
    with pytest.raises(ValueError):
        mapbox.Directions(profile="bogus", access_token='pk.test')


@responses.activate
def test_direction_params():
    params = "&alternatives=false&instructions=html&geometry=polyline&steps=false"

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test' + params,
        match_querystring=True,
        body="not important, only testing URI templating", status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').route(points,
                                                          alternatives=False,
                                                          instructions='html',
                                                          geometry='polyline',
                                                          steps=False)
    assert res.status_code == 200
