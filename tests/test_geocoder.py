import json
import responses
import mapbox


def test_service_session():
    """Get a session using a token"""
    session = mapbox.Service().get_session('pk.test')
    assert session.params.get('access_token') == 'pk.test'


def test_service_session_env():
    """Get a session using the env's token"""
    session = mapbox.Service().get_session(
        env={'MapboxAccessToken': 'pk.test_env'})
    assert session.params.get('access_token') == 'pk.test_env'


def test_service_session_os_environ(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MapboxAccessToken', 'pk.test_os_environ')
    session = mapbox.Service().get_session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()

def test_geocoder_default_name():
    """Default name is set"""
    geocoder = mapbox.Geocoder()
    assert geocoder.name == 'mapbox.places'


def test_geocoder_name():
    """Named dataset name is set"""
    geocoder = mapbox.Geocoder('mapbox.places-permanent')
    assert geocoder.name == 'mapbox.places-permanent'


@responses.activate
def test_geocoder_forward():
    """Forward geocoding works"""

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').forward('1600 pennsylvania ave nw')
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]

@responses.activate
def test_geocoder_reverse():
    """Reverse geocoding works"""

    coords = [-77.4371, 37.5227]

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/%s.json?access_token=pk.test' % ','.join(map(lambda x: str(x), coords)),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords), status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').reverse(*map(lambda x: str(x), coords))
    assert response.status_code == 200
    assert response.json()['query'] == coords
