import pytest
import responses

import mapbox


@pytest.fixture
def points():
    return [{
        "type": "Feature",
        "properties": {'title': 'point1'},
        "geometry": {
            "type": "Point",
            "coordinates": [-61.7, 12.1]}}, {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [-61.6, 12.0]}}]


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

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/geojson(%7B%22type%22%3A%20%22FeatureCollection%22%2C%20%22features%22%3A%20%5B%7B%22geometry%22%3A%20%7B%22type%22%3A%20%22Point%22%2C%20%22coordinates%22%3A%20%5B-61.7%2C%2012.1%5D%7D%2C%20%22type%22%3A%20%22Feature%22%2C%20%22properties%22%3A%20%7B%22title%22%3A%20%22point1%22%7D%7D%2C%20%7B%22geometry%22%3A%20%7B%22type%22%3A%20%22Point%22%2C%20%22coordinates%22%3A%20%5B-61.6%2C%2012.0%5D%7D%2C%20%22type%22%3A%20%22Feature%22%2C%20%22properties%22%3A%20%7B%7D%7D%5D%7D)/-61.7,12.1,12/600x600.png256?access_token=pk.test', 
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

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/geojson(%7B%22type%22%3A%20%22FeatureCollection%22%2C%20%22features%22%3A%20%5B%7B%22geometry%22%3A%20%7B%22type%22%3A%20%22Point%22%2C%20%22coordinates%22%3A%20%5B-61.7%2C%2012.1%5D%7D%2C%20%22type%22%3A%20%22Feature%22%2C%20%22properties%22%3A%20%7B%22title%22%3A%20%22point1%22%7D%7D%2C%20%7B%22geometry%22%3A%20%7B%22type%22%3A%20%22Point%22%2C%20%22coordinates%22%3A%20%5B-61.6%2C%2012.0%5D%7D%2C%20%22type%22%3A%20%22Feature%22%2C%20%22properties%22%3A%20%7B%7D%7D%5D%7D)/auto/600x600.png256?access_token=pk.test',
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
