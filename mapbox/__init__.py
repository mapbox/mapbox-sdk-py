# mapbox

import os

import requests
from uritemplate import URITemplate


__version__ = "0.1.0"


class Service:
    """Base service class"""

    def get_session(self, token):
        access_token = token or os.environ.get('MapboxAccessToken')
        session = requests.Session()
        session.params.update(access_token=access_token)
        return session


class Geocoder(Service):
    """A very simple Geocoding API proxy"""

    def __init__(self, name='mapbox.places', access_token=None):
        self.name = name
        self.baseuri = 'http://api.mapbox.com/v4/geocode'
        self.session = self.get_session(access_token)

    def fwd(self, address, params=None):
        """A forward geocoding request

        See: https://www.mapbox.com/developers/api/geocoding/#forward."""
        uri = URITemplate('%s/{dataset}/{query}.json' % self.baseuri).expand(
            dataset=self.name, query=address)
        return self.session.get(uri, params=params)
