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

    res = mapbox.Static(access_token='pk.test').staticmap('mapbox.satellite', -61.7, 12.1, 12)
    assert res.status_code == 200


@responses.activate
def test_staticmap_lonlatz_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points})
    overlay = quote(overlay)
    url = ('https://api.mapbox.com/v4/mapbox.satellite/geojson({0})/'
           '-61.7,12.1,12/600x600.png256?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').staticmap('mapbox.satellite',
                                                          -61.7, 12.1, 12,
                                                          points)
    assert res.status_code == 200

@responses.activate
def test_staticmap_auto_features(points):

    overlay = json.dumps({'type': 'FeatureCollection',
                          'features': points})
    overlay = quote(overlay)
    url = ('https://api.mapbox.com/v4/mapbox.satellite/geojson({0})/'
           'auto/600x600.png256?access_token=pk.test'.format(overlay))

    responses.add(
        responses.GET, url,
        match_querystring=True,
        body='png123',
        status=200,
        content_type='image/png')

    res = mapbox.Static(access_token='pk.test').staticmap('mapbox.satellite',
                                                          features=points)
    assert res.status_code == 200


def test_staticmap_auto_nofeatures(points):
    with pytest.raises(ValueError):
        mapbox.Static(access_token='pk.test').staticmap('mapbox.satellite')
