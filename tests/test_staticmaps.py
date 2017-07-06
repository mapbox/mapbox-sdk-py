import json

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

import pytest
import responses

import mapbox


@pytest.fixture
def points():
    points = [
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

    return points


@responses.activate
def test_staticmap_lonlatz_only():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/-61.7,12.1,12/600x600.png256?access_token=pk.test',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').image('mapbox.satellite', -61.7, 12.1, 12)
    assert res.status_code == 200


@responses.activate
def test_staticmap_lonlatz_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points}, separators=(',', ':'))
    overlay = quote(overlay)
    url = ('https://api.mapbox.com/v4/mapbox.satellite/geojson({0})/'
           '-61.7,12.1,12/600x600.png256?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').image('mapbox.satellite',
                                                      -61.7, 12.1, 12,
                                                      points)
    assert res.status_code == 200

@responses.activate
def test_staticmap_auto_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points}, separators=(',', ':'))
    overlay = quote(overlay)
    url = ('https://api.mapbox.com/v4/mapbox.satellite/geojson({0})/'
           'auto/600x600.png256?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').image('mapbox.satellite',
                                                      features=points)
    assert res.status_code == 200


def test_staticmap_auto_nofeatures(points):
    with pytest.raises(ValueError):
        mapbox.Static(access_token='pk.test').image('mapbox.satellite')


def test_staticmap_featurestoolarge(points):
    service = mapbox.Static(access_token='pk.test')
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_overlay(json.dumps(points * 100))


def test_staticmap_imagesize():
    service = mapbox.Static(access_token='pk.test')
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_image_size(0)
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_image_size(2000)


def test_latlon():
    service = mapbox.Static(access_token='pk.test')
    assert -179.0 == service._validate_lon(-179.0)
    assert -85.0 == service._validate_lat(-85.0)


def test_lon_invalid():
    service = mapbox.Static(access_token='pk.test')
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_lat(-86.0)
    with pytest.raises(mapbox.errors.ValidationError):
        service._validate_lon(-181.0)


@responses.activate
def test_staticmap_retina():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/-61.7,12.1,12/600x600@2x.png256?access_token=pk.test',
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').image(
        'mapbox.satellite', -61.7, 12.1, 12, retina=True)
    assert res.status_code == 200
