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

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/datasets/v1'
        self.session = self.get_session(access_token)

    def _attribs(self, name=None, description=None):
        """Form an attributes dictionary from keyword args."""
        a = {}
        if name:
            a['name'] = name
        if description:
            a['description'] = description
        return a

    def create(self, name=None, description=None):
        """Create a new dataset.
        
        Returns a :class:`requests.Response` containing the attributes
        of the new dataset as a JSON object.

        :param name: the dataset name (optional).
        :param description: the dataset description (optional).
        """
        uri = URITemplate(self.baseuri + '/{owner}').expand(
            owner=self.username)
        return self.session.post(uri, json=self._attribs(name, description))

    def list(self):
        """List datasets.
        
        Returns a :class:`requests.Response` containing a list of
        objects describing datasets.
        """
        uri = URITemplate(self.baseuri + '/{owner}').expand(
            owner=self.username)
        return self.session.get(uri)

    def read_dataset(self, dataset):
        """Read the attributes of a dataset.
        
        Returns a :class:`requests.Response` containing the attributes
        as a JSON object. The attributes: owner (a Mapbox account), 
        id (dataset id), created (Unix timestamp), modified 
        (timestamp), name (string), and description (string).

        :param dataset: the dataset identifier string.
        """
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.get(uri)

    def update_dataset(self, dataset, name=None, description=None):
        """Update the name and description of a dataset.
        
        Returns a :class:`requests.Response` containing the updated
        attributes as a JSON object.

        :param dataset: the dataset identifier string.
        :param name: the dataset name.
        :param description: the dataset description.
        """
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.patch(uri, json=self._attribs(name, description))

    def delete_dataset(self, dataset):
        """Delete a dataset.

        :param dataset: the dataset identifier string.
        """
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.delete(uri)

    def list_features(self, dataset, reverse=False, start=None, limit=None):
        """Get features of a dataset.
        
        Returns a :class:`requests.Response` containing the features of
        the dataset as a GeoJSON feature collection.

        :param dataset: the dataset identifier string.
        """
        uri = URITemplate(
            self.baseuri + '/{owner}/{id}/features').expand(
            owner=self.username, id=dataset)
        params = {}
        if reverse:
            params['reverse'] = 'true'
        if start:
            params['start'] = start
        if limit:
            params['limit'] = int(limit)
        return self.session.get(uri, params=params)

    def update_features(self, dataset, put=None, delete=None):
        """Update features of a dataset.
        
        Up to 100 features may be deleted or modified in one request.

        :param dataset: the dataset identifier string.
        :param put: an array of GeoJSON features to be created or
            modified with the semantics of HTTP PUT.
        :param delete: an array of feature ids to be deleted with
            the semantics of HTTP DELETE.
        """
        uri = URITemplate(self.baseuri + '/{owner}/{id}/features').expand(
            owner=self.username, id=dataset)
        updates = {}
        if put:
            updates['put'] = put
        if delete:
            updates['delete'] = delete
        return self.session.post(uri, json=updates)

    def read_feature(self, dataset, fid):
        """Read a dataset feature.

        Returns a :class:`requests.Response` containing a GeoJSON
        representation of the feature.

        :param dataset: the dataset identifier string.
        :param fid: the feature identifier string.
        """
        pass

    def update_feature(self, dataset, fid, feature):
        """Create or update a dataset feature.

        The semantics of HTTP PUT apply: if the dataset has no feature
        with the given `fid` a new feature will be created. Returns a
        :class:`requests.Response` containing a GeoJSON representation
        of the new or updated feature.

        :param dataset: the dataset identifier string.
        :param fid: the feature identifier string.
        :param feature: a GeoJSON feature object.
        """
        pass

    def delete_feature(self, dataset, fid):
        """Delete a dataset feature.

        :param dataset: the dataset identifier string.
        :param fid: the feature identifier string.
        """
        pass
