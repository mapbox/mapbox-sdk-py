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


def test_service_session_os_environ_caps(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', 'pk.test_os_environ')
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
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=pk.test',
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
        'https://api.mapbox.com/v4/geocode/mapbox.places/%s.json?access_token=pk.test' % ','.join([str(x) for x in coords]),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').reverse(*[str(x) for x in coords])
    assert response.status_code == 200
    assert response.json()['query'] == coords


def test_geocoder_place_types():
    """Place types are enumerated"""
    assert sorted(mapbox.Geocoder().place_types.items()) == [
        ('address', "A street address with house number. Examples: 1600 Pennsylvania Ave NW, 1051 Market St, Oberbaumstrasse 7."),
        ('country', "Sovereign states and other political entities. Examples: United States, France, China, Russia."),
        ('place', "City, town, village or other municipality relevant to a country's address or postal system. Examples: Cleveland, Saratoga Springs, Berlin, Paris."),
        ('poi', "Places of interest including commercial venues, major landmarks, parks, and other features. Examples: Yosemite National Park, Lake Superior."),
        ('postcode', "Postal code, varies by a country's postal system. Examples: 20009, CR0 3RL."),
        ('region', "First order administrative divisions within a country, usually provinces or states. Examples: California, Ontario, Essonne.")]


def test_validate_place_types_err():
    try:
        mapbox.Geocoder()._validate_place_types(('address', 'bogus'))
    except mapbox.InvalidPlaceTypeError as err:
        assert str(err) == "'bogus'"


def test_validate_place_types():
    assert mapbox.Geocoder()._validate_place_types(
        ('address', 'poi')) == {'types': 'address,poi'}


@responses.activate
def test_geocoder_forward_types():
    """Type filtering of forward geocoding works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?types=address,country,place,poi,postcode,region&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            '1600 pennsylvania ave nw',
            place_types=('address', 'country', 'place', 'poi', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]


@responses.activate
def test_geocoder_reverse_types():
    """Type filtering of reverse geocoding works"""

    coords = [-77.4371, 37.5227]

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/%s.json?types=address,country,place,poi,postcode,region&access_token=pk.test' % ','.join([str(x) for x in coords]),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').reverse(
            *[str(x) for x in coords],
            place_types=('address', 'country', 'place', 'poi', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == coords
