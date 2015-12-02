# mapbox.datasets
from itertools import chain, count, groupby
import json

import requests
from uritemplate import URITemplate

from mapbox.services.base import Service


# Constants
BASE_URI = 'https://api.mapbox.com/datasets/v1'
MAX_BATCH_SIZE = 100


def iter_features(src, is_sequence=False):
    """Yield features from a src that may be either a GeoJSON feature
    text sequence or GeoJSON feature collection."""
    first_line = next(src)
    # If input is RS-delimited JSON sequence.
    if first_line.startswith(u'\x1e'):
        buffer = first_line.strip(u'\x1e')
        for line in src:
            if line.startswith(u'\x1e'):
                if buffer:
                    feat = json.loads(buffer)
                    yield feat
                buffer = line.strip(u'\x1e')
            else:
                buffer += line
        else:
            feat = json.loads(buffer)
            yield feat
    elif is_sequence:
        yield json.loads(first_line)
        for line in src:
            feat = json.loads(line)
            yield feat
    else:
        text = "".join(chain([first_line], src))
        for feat in json.loads(text)['features']:
            yield feat


def batch(iterable, size=MAX_BATCH_SIZE):
    """Yield batches of features."""
    c = count()
    for k, g in groupby(iterable, lambda x:next(c)//size):
         yield g


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
