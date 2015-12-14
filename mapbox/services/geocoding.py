# mapbox
from uritemplate import URITemplate
from .base import Service
from mapbox.errors import InvalidPlaceTypeError


class Geocoder(Service):
    """A very simple Geocoding API proxy"""

    def __init__(self, name='mapbox.places', access_token=None):
        self.name = name
        self.baseuri = 'https://api.mapbox.com/geocoding/v5'
        self.session = self.get_session(access_token)
        self.precision = {'reverse': 5, 'proximity': 3}

    def _validate_place_types(self, types):
        """Validate place types and return a mapping for use in requests"""
        for pt in types:
            if pt not in self.place_types:
                raise InvalidPlaceTypeError(pt)
        return {'types': ",".join(types)}

    def forward(self, address, types=None, lon=None, lat=None):
        """Returns a Requests response object that contains a GeoJSON
        collection of places matching the given address.

        `response.geojson()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        Place results may be constrained to those of one or more types
        or be biased toward a given longitude and latitude.

        See: https://www.mapbox.com/developers/api/geocoding/#forward."""
        uri = URITemplate('%s/{dataset}/{query}.json' % self.baseuri).expand(
            dataset=self.name, query=address)
        params = {}
        if types:
            params.update(self._validate_place_types(types))
        if lon is not None and lat is not None:
            params.update(proximity='{0},{1}'.format(
                round(float(lon), self.precision.get('proximity', 3)),
                round(float(lat), self.precision.get('proximity', 3))))
        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        # for consistency with other services
        def geojson():
            return resp.json()
        resp.geojson = geojson

        return resp

    def reverse(self, lon=None, lat=None, types=None):
        """Returns a Requests response object that contains a GeoJSON
        collection of places near the given longitude and latitude.

        `response.geojson()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/developers/api/geocoding/#reverse."""
        uri = URITemplate(self.baseuri + '/{dataset}/{lon},{lat}.json').expand(
            dataset=self.name,
            lon=str(round(float(lon), self.precision.get('reverse', 5))),
            lat=str(round(float(lat), self.precision.get('reverse', 5))))
        params = {}
        if types:
            params.update(self._validate_place_types(types))
        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        # for consistency with other services
        def geojson():
            return resp.json()
        resp.geojson = geojson

        return resp

    @property
    def place_types(self):
        """A mapping of place type names to descriptions"""
        return {
            'address': "A street address with house number. Examples: 1600 Pennsylvania Ave NW, 1051 Market St, Oberbaumstrasse 7.",
            'country': "Sovereign states and other political entities. Examples: United States, France, China, Russia.",
            'place': "City, town, village or other municipality relevant to a country's address or postal system. Examples: Cleveland, Saratoga Springs, Berlin, Paris.",
            'neighborhood': "A smaller area within a place, often without formal boundaries. Examples: Montparnasse, Downtown, Haight-Ashbury.",
            'poi': "Places of interest including commercial venues, major landmarks, parks, and other features. Examples: Yosemite National Park, Lake Superior.",
            'postcode': "Postal code, varies by a country's postal system. Examples: 20009, CR0 3RL.",
            'region': "First order administrative divisions within a country, usually provinces or states. Examples: California, Ontario, Essonne."}
