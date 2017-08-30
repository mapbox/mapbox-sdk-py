# coding=utf-8

import json
import re
import responses
import pytest

import mapbox


def test_class_attrs():
    """Get expected class attr values"""
    serv = mapbox.Geocoder()
    assert serv.api_name == 'geocoder'
    assert serv.api_version == 'v5'


def test_geocoder_default_name():
    """Default name is set"""
    geocoder = mapbox.Geocoder()
    assert geocoder.name == 'mapbox.places'


def test_geocoder_name():
    """Named dataset name is set"""
    geocoder = mapbox.Geocoder('mapbox.places-permanent')
    assert geocoder.name == 'mapbox.places-permanent'

def _check_coordinate_precision(coord, precision):
    """Coordinate precision is <= specified number of digits"""
    if '.' not in coord:
        return True
    else:
        return len(coord.split('.')[-1]) <= precision


@responses.activate
def test_geocoder_forward():
    """Forward geocoding works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').forward('1600 pennsylvania ave nw')
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]


@responses.activate
def test_geocoder_forward_geojson():
    """Forward geocoding .geojson method works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').forward('1600 pennsylvania ave nw')
    assert response.status_code == 200
    assert response.geojson() == response.json()


@responses.activate
def test_geocoder_reverse():
    """Reverse geocoding works"""

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').reverse(lon=lon, lat=lat)
    assert response.status_code == 200
    assert response.json()['query'] == [lon, lat]

@responses.activate
def test_geocoder_reverse_geojson():
    """Reverse geocoding geojson works"""

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').reverse(lon=lon, lat=lat)
    assert response.status_code == 200
    assert response.geojson() == response.json()

def test_geocoder_place_types():
    """Place types are enumerated"""
    assert sorted(mapbox.Geocoder().place_types.items()) == [
        ('address', "A street address with house number. Examples: 1600 Pennsylvania Ave NW, 1051 Market St, Oberbaumstrasse 7."),
        ('country', "Sovereign states and other political entities. Examples: United States, France, China, Russia."),
        ('district', "Second order administrative division. Only used when necessary. Examples: Tianjin, Beijing"),
        ('locality', "A smaller area within a place that possesses official status and boundaries. Examples: Oakleigh (Melbourne)"),
        ('neighborhood', 'A smaller area within a place, often without formal boundaries. Examples: Montparnasse, Downtown, Haight-Ashbury.'),
        ('place', "City, town, village or other municipality relevant to a country's address or postal system. Examples: Cleveland, Saratoga Springs, Berlin, Paris."),
        ('poi', "Places of interest including commercial venues, major landmarks, parks, and other features. Examples: Subway Restaurant, Yosemite National Park, Statue of Liberty."),
        ('poi.landmark', "Places of interest that are particularly notable or long-lived like parks, places of worship and museums. A strict subset of the poi place type. Examples: Yosemite National Park, Statue of Liberty."),
        ('postcode', "Postal code, varies by a country's postal system. Examples: 20009, CR0 3RL."),
        ('region', "First order administrative divisions within a country, usually provinces or states. Examples: California, Ontario, Essonne.")]


def test_validate_country_codes_err():
    try:
        mapbox.Geocoder()._validate_country_codes(('us', 'bogus'))
    except mapbox.InvalidCountryCodeError as err:
        assert str(err) == "bogus"


def test_validate_country():
    assert mapbox.Geocoder()._validate_country_codes(
        ('us', 'br')) == {'country': 'us,br'}


def test_validate_place_types_err():
    try:
        mapbox.Geocoder()._validate_place_types(('address', 'bogus'))
    except mapbox.InvalidPlaceTypeError as err:
        assert str(err) == "bogus"


def test_validate_place_types():
    assert mapbox.Geocoder()._validate_place_types(
        ('address', 'poi')) == {'types': 'address,poi'}


@responses.activate
def test_geocoder_forward_types():
    """Type filtering of forward geocoding works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?types=address,country,place,poi.landmark,postcode,region&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            '1600 pennsylvania ave nw',
            types=('address', 'country', 'place', 'poi.landmark', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]


@responses.activate
def test_geocoder_reverse_types():
    """Type filtering of reverse geocoding works"""

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?types=address,country,place,poi.landmark,postcode,region&access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').reverse(
            lon=lon, lat=lat,
            types=('address', 'country', 'place', 'poi.landmark', 'postcode', 'region'))
    assert response.status_code == 200
    assert response.json()['query'] == [lon, lat]


@responses.activate
def test_geocoder_forward_proximity():
    """Proximity parameter works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?proximity=0.0,0.0&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            '1600 pennsylvania ave nw', lon=0, lat=0)
    assert response.status_code == 200
    assert response.json()['query'] == ["1600", "pennsylvania", "ave", "nw"]

@responses.activate
def test_geocoder_proximity_rounding():
    """Proximity parameter is rounded to 3 decimal places"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        match_querystring=False,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            '1600 pennsylvania ave nw', lon=0.123456, lat=0.987654)

    # check coordinate precision for proximity flag
    match = re.search(r'[&\?]proximity=([^&$]+)', response.url)
    assert match is not None
    for coord in re.split(r'(%2C|,)', match.group(1)):
        assert _check_coordinate_precision(coord, 3)

@responses.activate
def test_geocoder_forward_bbox():
    """Bbox parameter works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/washington.json?bbox=-78.3284%2C38.6039%2C-78.0428%2C38.7841&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["washington"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            'washington', bbox=(-78.3284, 38.6039, -78.0428, 38.7841))
    assert response.status_code == 200
    assert response.json()['query'] == ["washington"]

@responses.activate
def test_geocoder_forward_limit():
    """Limit parameter works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/washington.json?limit=3&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["washington"], "features": [1, 2, 3]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward(
            'washington', limit=3)
    assert response.status_code == 200
    assert len(response.json()['features']) == 3


@responses.activate
def test_geocoder_reverse_limit():
    """Limit parameter works"""

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat],
                       "features": [{'name': 'place'}]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=pk.test&limit=1&types=place'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    service = mapbox.Geocoder(access_token='pk.test')
    response = service.reverse(lon=lon, lat=lat, limit=1, types=['place'])
    assert response.status_code == 200
    assert len(response.json()['features']) == 1


@responses.activate
def test_geocoder_reverse_limit_requires_onetype():
    """Limit requires a single type"""

    lon, lat = -77.123456789, 37.987654321
    service = mapbox.Geocoder(access_token='pk.test')

    with pytest.raises(mapbox.InvalidPlaceTypeError):
        service.reverse(lon=lon, lat=lat, limit=1)

    with pytest.raises(mapbox.InvalidPlaceTypeError):
        service.reverse(lon=lon, lat=lat, limit=1, types=['places', 'country'])


@responses.activate
def test_geocoder_reverse_rounding():
    """Reverse geocoding parameters are rounded to 5 decimal places"""

    lon, lat = -77.123456789, 37.987654321
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        re.compile('https:\/\/api\.mapbox\.com\/geocoding\/v5\/mapbox\.places\/.+\.json'),
        match_querystring=False,
        body=body,
        status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').reverse(
            lon=lon, lat=lat)

    # check coordinate precision for reverse geocoding coordinates
    match = re.search(r'\/([\-\d\.\,]+)\.json', response.url)
    assert match is not None
    for coord in re.split(r'(%2C|,)', match.group(1)):
        assert _check_coordinate_precision(coord, 5)


@responses.activate
def test_geocoder_unicode():
    """Forward geocoding works with non-ascii inputs
    Specifically, the URITemplate needs to utf-8 encode all inputs
    """

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/Florian%C3%B3polis%2C%20Brazil.json?access_token=pk.test',
        match_querystring=True,
        body='{}', status=200,
        content_type='application/json')

    query = "Florianópolis, Brazil"
    try:
        query = query.decode('utf-8')  # Python 2
    except:
        pass  # Python 3

    response = mapbox.Geocoder(access_token='pk.test').forward(query)
    assert response.status_code == 200


@responses.activate
def test_geocoder_forward_country():
    """Country parameter of forward geocoding works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?country=us&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(
        access_token='pk.test').forward('1600 pennsylvania ave nw', country=['us'])
    assert response.status_code == 200


@responses.activate
def test_geocoder_language():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?language=en,de&access_token=pk.test',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    response = mapbox.Geocoder(access_token='pk.test').forward(
        '1600 pennsylvania ave nw', languages=['en', 'de'])
    assert response.status_code == 200
