# mapbox
from iso3166 import countries
from uritemplate import URITemplate

from mapbox.errors import InvalidCountryCodeError, InvalidPlaceTypeError
from mapbox.services.base import Service


class Geocoder(Service):
    """Access to the Geocoding API V5"""

    api_name = 'geocoding'
    api_version = 'v5'
    precision = {'reverse': 5, 'proximity': 3}

    def __init__(self, name='mapbox.places', access_token=None, cache=None,
                 host=None):
        """Constructs a Geocoding Service object.

        :param name: name of a geocoding dataset.
        :param access_token: Mapbox access token string.
        :param cache: CacheControl cache instance (Dict or FileCache).
        """
        self.name = name
        super(Geocoder, self).__init__(access_token=access_token, cache=cache,
                                       host=host)

    def _validate_country_codes(self, ccs):
        """Validate country code filters for use in requests."""
        for cc in ccs:
            if cc not in self.country_codes:
                raise InvalidCountryCodeError(cc)
        return {'country': ",".join(ccs)}

    def _validate_place_types(self, types):
        """Validate place types and return a mapping for use in requests."""
        for pt in types:
            if pt not in self.place_types:
                raise InvalidPlaceTypeError(pt)
        return {'types': ",".join(types)}

    def forward(self, address, types=None, lon=None, lat=None,
                country=None, bbox=None, limit=None, languages=None):
        """Returns a Requests response object that contains a GeoJSON
        collection of places matching the given address.

        `response.geojson()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        Place results may be constrained to those of one or more types
        or be biased toward a given longitude and latitude.

        See: https://www.mapbox.com/api-documentation/#geocoding."""
        uri = URITemplate(self.baseuri + '/{dataset}/{query}.json').expand(
            dataset=self.name, query=address.encode('utf-8'))
        params = {}
        if country:
            params.update(self._validate_country_codes(country))
        if types:
            params.update(self._validate_place_types(types))
        if lon is not None and lat is not None:
            params.update(proximity='{0},{1}'.format(
                round(float(lon), self.precision.get('proximity', 3)),
                round(float(lat), self.precision.get('proximity', 3))))
        if languages:
            params.update(language=','.join(languages))
        if bbox is not None:
            params.update(bbox='{0},{1},{2},{3}'.format(*bbox))
        if limit is not None:
            params.update(limit='{0}'.format(limit))
        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        # for consistency with other services
        def geojson():
            return resp.json()
        resp.geojson = geojson

        return resp

    def reverse(self, lon, lat, types=None, limit=None):
        """Returns a Requests response object that contains a GeoJSON
        collection of places near the given longitude and latitude.

        `response.geojson()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/api-documentation/#retrieve-places-near-a-location."""
        uri = URITemplate(self.baseuri + '/{dataset}/{lon},{lat}.json').expand(
            dataset=self.name,
            lon=str(round(float(lon), self.precision.get('reverse', 5))),
            lat=str(round(float(lat), self.precision.get('reverse', 5))))
        params = {}

        if types:
            types = list(types)
            params.update(self._validate_place_types(types))

        if limit is not None:
            if not types or len(types) != 1:
                raise InvalidPlaceTypeError(
                    'Specify a single type when using limit with reverse geocoding')
            params.update(limit='{0}'.format(limit))

        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        # for consistency with other services
        def geojson():
            return resp.json()
        resp.geojson = geojson

        return resp

    @property
    def country_codes(self):
        """A list of valid country codes"""
        return [c.alpha2.lower() for c in countries]

    @property
    def place_types(self):
        """A mapping of place type names to descriptions"""
        return {
            'address': "A street address with house number. Examples: 1600 Pennsylvania Ave NW, 1051 Market St, Oberbaumstrasse 7.",
            'country': "Sovereign states and other political entities. Examples: United States, France, China, Russia.",
            'place': "City, town, village or other municipality relevant to a country's address or postal system. Examples: Cleveland, Saratoga Springs, Berlin, Paris.",
            'locality': "A smaller area within a place that possesses official status and boundaries. Examples: Oakleigh (Melbourne)",
            'neighborhood': "A smaller area within a place, often without formal boundaries. Examples: Montparnasse, Downtown, Haight-Ashbury.",
            'poi': "Places of interest including commercial venues, major landmarks, parks, and other features. Examples: Subway Restaurant, Yosemite National Park, Statue of Liberty.",
            'poi.landmark': "Places of interest that are particularly notable or long-lived like parks, places of worship and museums. A strict subset of the poi place type. Examples: Yosemite National Park, Statue of Liberty.",
            'postcode': "Postal code, varies by a country's postal system. Examples: 20009, CR0 3RL.",
            'district': "Second order administrative division. Only used when necessary. Examples: Tianjin, Beijing",
            'region': "First order administrative divisions within a country, usually provinces or states. Examples: California, Ontario, Essonne."}
