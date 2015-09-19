import json
import responses

import mapbox


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

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/{0},{1}.json?access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').reverse(lon=lon, lat=lat)
    assert response.status_code == 200
    assert response.json()['query'] == [lon, lat]


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
            types=('address', 'country', 'place', 'poi', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]


@responses.activate
def test_geocoder_reverse_types():
    """Type filtering of reverse geocoding works"""

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/{0},{1}.json?types=address,country,place,poi,postcode,region&access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').reverse(
            lon=lon, lat=lat,
            types=('address', 'country', 'place', 'poi', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == [lon, lat]


@responses.activate
def test_geocoder_forward_proximity():
    """Proximity parameter works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?proximity=0,0&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            '1600 pennsylvania ave nw', lon=0, lat=0)
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]
