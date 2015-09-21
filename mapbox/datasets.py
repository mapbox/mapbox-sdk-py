# mapbox.datasets

import requests
from uritemplate import URITemplate

from mapbox.service import Service


BASE_URI = 'https://api.mapbox.com/datasets/v1'


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


class Dataset(Service):
    """A Datasets API proxy"""

    def __init__(self, owner, id, access_token=None):
        self.owner = owner
        self.id = id
        self.baseuri = URITemplate(BASE_URI + '/{owner}/{id}').expand(
            owner=self.owner, id=self.id)
        self.session = self.get_session(access_token)

    def retrieve_features(self):
        """Return a Requests response object that contains the features
        of the dataset.

        `response.json()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/developers/api/datasets/."""
        uri = URITemplate(self.baseuri + '/features').expand()
        return self.session.get(uri)


    def update_features(self, **updates):
        """Return a Requests response object that contains the features
        of the dataset.

        `response.json()` returns the geocoding result as GeoJSON.
        `response.status_code` returns the HTTP API status code.

        See: https://www.mapbox.com/developers/api/datasets/."""
        uri = URITemplate(self.baseuri + '/features').expand()
        return self.session.post(uri, json=updates)
