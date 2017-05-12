import json
import pytest
import responses
import mapbox

try:
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6
    from ordereddict import OrderedDict


@pytest.fixture
def points():
    return [
        OrderedDict(
            type="Feature",
            properties=OrderedDict(title="point1"),
            geometry=OrderedDict(
                type="Point",
                coordinates=[-61.7, 12.1])),
        OrderedDict(
            type="Feature",
            properties=OrderedDict(title="point2"),
            geometry=OrderedDict(
                type="Point",
                coordinates=[-61.6, 12.0]))]


@responses.activate
def test_staticmap_lonlatzpitchbearing():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/styles/v1/mapbox/streets-v9/static/-61.7,12.1,12.5,75,25/600x600?access_token=pk.test',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').image(
        'mapbox', 'streets-v9', -61.7, 12.1, 12.5, pitch=25, bearing=75)
    assert res.status_code == 200


@responses.activate
def test_staticmap_lonlatz_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points}, separators=(',', ':'))
    overlay = quote(overlay)

    url = ('https://api.mapbox.com/styles/v1/mapbox/streets-v9/static/geojson({0})/'
           '-61.7,12.1,12,0,0/600x600?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').image(
        'mapbox', 'streets-v9', -61.7, 12.1, 12, points)
    assert res.status_code == 200


@responses.activate
def test_staticmap_auto_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points}, separators=(',', ':'))
    overlay = quote(overlay)

    url = ('https://api.mapbox.com/styles/v1/mapbox/streets-v9/static/geojson({0})/'
           'auto/600x600?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').image(
        'mapbox', 'streets-v9', features=points)
    assert res.status_code == 200


def test_staticmap_auto_nofeatures(points):
    with pytest.raises(ValueError):
        mapbox.StaticStyle(access_token='pk.test').image('mapbox', 'streets-v9')


def test_staticmap_featurestoolarge(points):
    from mapbox.services.static_style import validate_overlay
    with pytest.raises(mapbox.errors.ValidationError):
        validate_overlay(json.dumps(points * 100))


def test_staticmap_validate_bearing():
    from mapbox.services.static_style import validate_bearing
    assert validate_bearing(1) == 1
    with pytest.raises(mapbox.errors.ValidationError):
        validate_bearing(-1)
    with pytest.raises(mapbox.errors.ValidationError):
        validate_bearing(375)


def test_staticmap_validate_pitch():
    from mapbox.services.static_style import validate_pitch
    assert validate_pitch(1) == 1
    with pytest.raises(mapbox.errors.ValidationError):
        validate_pitch(-1)
    with pytest.raises(mapbox.errors.ValidationError):
        validate_pitch(89)


def test_staticmap_imagesize():
    from mapbox.services.static_style import validate_image_size
    with pytest.raises(mapbox.errors.ValidationError):
        validate_image_size(0)
    with pytest.raises(mapbox.errors.ValidationError):
        validate_image_size(999999)


def test_latlon():
    from mapbox.services.static_style import validate_lat, validate_lon
    assert -179.0 == validate_lon(-179.0)
    assert -85.0 == validate_lat(-85.0)


def test_lon_invalid():
    from mapbox.services.static_style import validate_lat, validate_lon
    with pytest.raises(mapbox.errors.ValidationError):
        validate_lat(-86.0)
    with pytest.raises(mapbox.errors.ValidationError):
        validate_lon(-181.0)


@responses.activate
def test_staticmap_options():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/styles/v1/mapbox/streets-v9/static/-61.7,12.1,12.5,0,0/600x600?access_token=pk.test&attribution=true&logo=false&before_layer=a',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').image(
        'mapbox', 'streets-v9', -61.7, 12.1, 12.5,
        attribution=True, logo=False, before_layer='a')
    assert res.status_code == 200


@responses.activate
def test_staticmap_tile():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/512/10/163/395?access_token=pk.test',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').tile(
        'mapbox', 'streets-v9', 10, 163, 395)
    assert res.status_code == 200


def test_bad_tilesize():
    with pytest.raises(mapbox.errors.ValidationError):
        mapbox.StaticStyle(access_token='pk.test').tile(
            'mapbox', 'streets-v9', 10, 163, 395, tile_size=333)


@responses.activate
def test_staticmap_tile():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/10/163/395@2x?access_token=pk.test',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.StaticStyle(access_token='pk.test').tile(
        'mapbox', 'streets-v9', 10, 163, 395, tile_size=256, retina=True)
    assert res.status_code == 200


@responses.activate
def test_staticmap_wmts():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/styles/v1/mapbox/streets-v9/wmts?access_token=pk.test',
        match_querystring=True,
        body='<Capabilities xmlns=...',
        status=200,
        content_type='application/xml')

    res = mapbox.StaticStyle(access_token='pk.test').wmts('mapbox', 'streets-v9')
    assert res.status_code == 200
