from cachecontrol.cache import DictCache
import mapbox
import pytest
import responses


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
@pytest.mark.parametrize("cache", [None, DictCache()])
def test_directions(cache):
    with open('tests/moors.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/' +
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test', cache=cache).directions(points)
    assert res.status_code == 200
    assert 'distance' in res.json()['routes'][0].keys()


@responses.activate
def test_directions_polyline_as_geojson():
    with open('tests/moors.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(points)
    fc = res.geojson()
    assert fc['type'] == 'FeatureCollection'
    assert fc['features'][0]['geometry']['type'] == 'LineString'


@responses.activate
def test_directions_geojson_as_geojson():
    with open('tests/moors_geojson.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test'
        '&geometries=geojson',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(
        points, geometries='geojson')
    fc = res.geojson()
    assert fc['type'] == 'FeatureCollection'
    assert fc['features'][0]['geometry']['type'] == 'LineString'


def test_invalid_profile():
    with pytest.raises(ValueError):
        mapbox.Directions(access_token='pk.test').directions(
            points, profile='bogus')


@responses.activate
def test_direction_params():
    params = "&alternatives=false&geometries=polyline&overview=false&steps=false" \
             "&continue_straight=false&annotations=distance%2Cspeed&language=en" \
             "&radiuses=10%3Bunlimited"

    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test' + params,
        match_querystring=True,
        body="not important, only testing URI templating", status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(
        points,
        alternatives=False,
        geometries='polyline',
        overview=False,
        continue_straight=True,
        annotations=['distance', 'speed'],
        language='en',
        radiuses=[10, 'unlimited'],
        steps=False)
    assert res.status_code == 200


@responses.activate
def test_direction_backwards_compat():
    """Ensure old calls to directions method work against v5 API
    """
    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/cycling/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test'
        '&geometries=polyline',
        match_querystring=True,
        body="not important, only testing URI templating", status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(
        points,
        geometry='polyline',   # plural in v5
        profile='mapbox.cycling',  # '/' delimited in v5
    )
    # TODO instructions parameter removed in v5
    assert res.status_code == 200


@responses.activate
def test_direction_bearings():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test'
        '&radiuses=10%3B20&bearings=270%2C45%3B315%2C90',
        match_querystring=True,
        body="not important, only testing URI templating", status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(
        points,
        radiuses=[10, 20],
        bearings=[(270, 45), (315, 90)])
    assert res.status_code == 200


@responses.activate
def test_direction_bearings_none():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/directions/v5/mapbox/driving/'
        '-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=pk.test'
        '&radiuses=10%3B20&bearings=%3B315%2C90',
        match_querystring=True,
        body="not important, only testing URI templating", status=200,
        content_type='application/json')

    res = mapbox.Directions(access_token='pk.test').directions(
        points,
        radiuses=[10, 20],
        bearings=[None, (315, 90)])
    assert res.status_code == 200


def test_invalid_geom_encoding():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_geom_encoding('wkb')


def test_v4_profile_aliases():
    service = mapbox.Directions(access_token='pk.test')
    assert 'mapbox/cycling' == service._validate_profile('mapbox.cycling')


def test_invalid_annotations():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError):
        service._validate_annotations(['awesomeness'])


def test_invalid_geom_overview():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError):
        service._validate_geom_overview('infinite')


def test_invalid_radiuses():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError) as e:
        service._validate_radiuses([-1, 'forever'], points)
        assert 'not a valid radius' in str(e)


def test_invalid_number_of_radiuses():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError) as e:
        service._validate_radiuses([1, 2, 3], points)
        assert 'exactly one' in str(e)


def test_invalid_number_of_bearings():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError) as e:
        service._validate_bearings([1, 2, 3], points)
        assert 'exactly one' in str(e)


def test_invalid_bearing_tuple():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError) as e:
        service._validate_bearings([(270, 45, 'extra'), (315,)], points)
        assert 'bearing tuple' in str(e)


def test_invalid_bearing_domain():
    service = mapbox.Directions(access_token='pk.test')
    with pytest.raises(mapbox.errors.InvalidParameterError) as e:
        service._validate_bearings([(-1, 90), (315, 90)], points)
        assert 'between 0 and 360' in str(e)


def test_bearings_without_radius():
    with pytest.raises(mapbox.errors.InvalidParameterError):
        mapbox.Directions(access_token='pk.test').directions(
            points, bearings=[(270, 45), (270, 45)])
