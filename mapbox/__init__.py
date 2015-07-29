# mapbox

import requests
from uritemplate import URITemplate


__version__ = "0.1.0"


class Geocoder:
    """A very simple Geocoding API proxy"""

    def __init__(self, name='mapbox.places', access_token=None):
        self.name = name
        self.baseuri = 'http://api.mapbox.com/v4/geocode'
        self.session = requests.Session()
        if access_token:
            self.session.params.update(access_token=access_token)

    def fwd(self, address, params=None):
        """A forward geocoding request

        See: https://www.mapbox.com/developers/api/geocoding/#forward."""
        uri = URITemplate('%s/{dataset}/{query}.json' % self.baseuri).expand(
            dataset=self.name, query=address)
        return self.session.get(uri, params=params)
