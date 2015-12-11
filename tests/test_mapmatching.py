import pytest
import responses

import mapbox

@pytest.fixture
def line_feature():
    return {
        "type": "Feature",
        "properties": {
            "coordTimes": [
                "2015-04-21T06:00:00Z",
                "2015-04-21T06:00:05Z",
                "2015-04-21T06:00:10Z",
                "2015-04-21T06:00:15Z",
                "2015-04-21T06:00:20Z"]},
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [13.418946862220764, 52.50055852688439],
                [13.419011235237122, 52.50113000479732],
                [13.419756889343262, 52.50171780290061],
                [13.419885635375975, 52.50237416816131],
                [13.420631289482117, 52.50294888790448]]}}


@responses.activate
def test_matching(line_feature):

    body = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"confidence":0.8165504318718629,"matchedPoints":[[13.418805122375488,52.5005989074707],[13.419145584106445,52.501094818115234],[13.419618606567383,52.50175094604492],[13.420042037963867,52.50233459472656],[13.420494079589844,52.50298309326172]],"indices":[0,1,2,3,4]},"geometry":{"type":"LineString","coordinates":[[13.418805,52.500599],[13.418851,52.500659],[13.419121,52.501057],[13.419146,52.501095],[13.419276,52.501286],[13.419446,52.501518],[13.419619,52.501753],[13.419981,52.502249],[13.420042,52.502335],[13.420494,52.502984]]}}]}'

    responses.add(
        responses.POST,
        'https://api.mapbox.com/matching/v4/mapbox.driving.json?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    service = mapbox.MapMatcher(access_token='pk.test')
    res = service.match(line_feature)
    assert res.status_code == 200
    assert res.json() == res.geojson()


@responses.activate
def test_matching_precision(line_feature):

    body = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"confidence":0.8165504318718629,"matchedPoints":[[13.418805122375488,52.5005989074707],[13.419145584106445,52.501094818115234],[13.419618606567383,52.50175094604492],[13.420042037963867,52.50233459472656],[13.420494079589844,52.50298309326172]],"indices":[0,1,2,3,4]},"geometry":{"type":"LineString","coordinates":[[13.418805,52.500599],[13.418851,52.500659],[13.419121,52.501057],[13.419146,52.501095],[13.419276,52.501286],[13.419446,52.501518],[13.419619,52.501753],[13.419981,52.502249],[13.420042,52.502335],[13.420494,52.502984]]}}]}'

    responses.add(
        responses.POST,
        'https://api.mapbox.com/matching/v4/mapbox.cycling.json?gps_precision=4&access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    service = mapbox.MapMatcher(access_token='pk.test')
    res = service.match(line_feature, gps_precision=4, profile='mapbox.cycling')
    assert res.status_code == 200


def test_invalid_feature():
    service = mapbox.MapMatcher(access_token='pk.test')
    with pytest.raises(ValueError) as exc:
        service.match({'type': 'not-a-feature'})
        assert 'feature must have' in exc.message


def test_invalid_profile(line_feature):
    service = mapbox.MapMatcher(access_token='pk.test')
    with pytest.raises(ValueError):
        service.match(line_feature, profile="covered_wagon")
