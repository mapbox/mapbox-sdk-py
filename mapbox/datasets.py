# mapbox.datasets

import requests
from uritemplate import URITemplate

from mapbox.service import Service


class Datasets(Service):
    """A Datasets API proxy"""

    def __init__(self, name, access_token=None):
        self.name = name
        self.baseuri = 'https://api.mapbox.com/datasets/v1'
        self.session = self.get_session(access_token)

    def list(self):
        """Returns a Requests response object that contains a listing of
        the owner's datasets.

        `response.json()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/developers/api/datasets/."""
        uri = URITemplate(self.baseuri + '/{owner}').expand(owner=self.name)
        return self.session.get(uri)

    def create(self, **kwargs):
        """Create a new dataset and return a Requests response object
        that contains information about the new dataset.

        `response.json()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/developers/api/datasets/."""
        uri = URITemplate(self.baseuri + '/{owner}').expand(owner=self.name)
        return self.session.post(uri, json=kwargs)
