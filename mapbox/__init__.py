# mapbox

import os

import requests
from uritemplate import URITemplate


__version__ = "0.1.0"


class InvalidPlaceTypeError(KeyError):
    pass


class Service:
    """Base service class"""

    def get_session(self, token=None, env=None):
        access_token = (
            token or
            (env or os.environ).get('MapboxAccessToken') or
            (env or os.environ).get('MAPBOX_ACCESS_TOKEN'))
        session = requests.Session()
        session.params.update(access_token=access_token)
        return session


class Geocoder(Service):
    """A very simple Geocoding API proxy"""

    def __init__(self, name='mapbox.places', access_token=None):
        self.name = name
        self.baseuri = 'https://api.mapbox.com/v4/geocode'
        self.session = self.get_session(access_token)

    def _validate_place_types(self, place_types):
        """Validate place types and return a mapping for use in requests"""
        for pt in place_types:
            if pt not in self.place_types:
                raise InvalidPlaceTypeError(pt)
        return {'types': ",".join(place_types)}

    def forward(self, address, place_types=None, lng=None, lat=None):
        """A forward geocoding request

        Results may be constrained to those in a sequence of place_types or
        biased toward a given longitude and latitude.

        See: https://www.mapbox.com/developers/api/geocoding/#forward."""
        uri = URITemplate('%s/{dataset}/{query}.json' % self.baseuri).expand(
            dataset=self.name, query=address)
        params = {}
        if place_types:
            params.update(self._validate_place_types(place_types))
        if lng is not None and lat is not None:
            params.update(proximity='{0},{1}'.format(lng, lat))
        return self.session.get(uri, params=params)

    def reverse(self, lon, lat, place_types=None):
        """A reverse geocoding request

        See: https://www.mapbox.com/developers/api/geocoding/#reverse."""
        uri = URITemplate(self.baseuri + '/{dataset}/{lon},{lat}.json').expand(
            dataset=self.name, lon=str(lon), lat=str(lat))
        params = {}
        if place_types:
            params.update(self._validate_place_types(place_types))
        return self.session.get(uri, params=params)

    @property
    def place_types(self):
        """A mapping of place type names to descriptions"""
        return {
            'address': "A street address with house number. Examples: 1600 Pennsylvania Ave NW, 1051 Market St, Oberbaumstrasse 7.",
            'country': "Sovereign states and other political entities. Examples: United States, France, China, Russia.",
            'place': "City, town, village or other municipality relevant to a country's address or postal system. Examples: Cleveland, Saratoga Springs, Berlin, Paris.",
            'poi': "Places of interest including commercial venues, major landmarks, parks, and other features. Examples: Yosemite National Park, Lake Superior.",
            'postcode': "Postal code, varies by a country's postal system. Examples: 20009, CR0 3RL.",
            'region': "First order administrative divisions within a country, usually provinces or states. Examples: California, Ontario, Essonne."}
