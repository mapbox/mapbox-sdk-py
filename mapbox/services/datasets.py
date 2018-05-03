# mapbox.datasets
import json

import requests
from uritemplate import URITemplate

from mapbox.services.base import Service


class Datasets(Service):
    """Access to the Datasets API V1
    
    Attributes
    ----------
    api_name : str
        The API's name.
    
    api_version : str
        The API's version number.
    """

    api_name = 'datasets'
    api_version = 'v1'

    def _attribs(self, name=None, description=None):
        """Form an attributes dictionary from keyword args."""
        a = {}
        if name:
            a['name'] = name
        if description:
            a['description'] = description
        return a

    def create(self, name=None, description=None):
        """Creates a new, empty dataset.

        Parameters
        ----------
        name : str, optional
            The name of the dataset.

        description : str, optional
            The description of the dataset.

        Returns
        -------
        request.Response
            The response contains the properties of a new dataset as a JSON object.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}').expand(
            owner=self.username)
        return self.session.post(uri, json=self._attribs(name, description))

    def list(self):
        """Lists all datasets for a particular account.

        Returns
        -------
        request.Response
            The response contains a list of JSON objects describing datasets.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}').expand(
            owner=self.username)
        return self.session.get(uri)

    def read_dataset(self, dataset):
        """Retrieves (reads) a single dataset.

        Parameters
        ----------
        dataset : str
            The dataset id.

        Returns
        -------
        request.Response
            The response contains the properties of the retrieved dataset as a JSON object.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.get(uri)

    def update_dataset(self, dataset, name=None, description=None):
        """Updates a single dataset.

        Parameters
        ----------
        dataset : str
            The dataset id.

        name : str, optional
            The name of the dataset.

        description : str, optional
            The description of the dataset.

        Returns
        -------
        request.Response
            The response contains the properties of the updated dataset as a JSON object.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.patch(uri, json=self._attribs(name, description))

    def delete_dataset(self, dataset):
        """Deletes a single dataset, including all of the features that it contains.

        Parameters
        ----------
        dataset : str
            The dataset id.

        Returns
        -------
        HTTP status code.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}/{id}').expand(
            owner=self.username, id=dataset)
        return self.session.delete(uri)

    def list_features(self, dataset, reverse=False, start=None, limit=None):
        """Lists features in a dataset.

        Parameters
        ----------
        dataset : str             
            The dataset id.

        reverse : str, optional
            List features in reverse order.

            Possible value is "true".

        start : str, optional
            The id of the feature after which to start the list (pagination).

        limit : str, optional
            The maximum number of features to list (pagination).

        Returns
        -------
        request.Response
            The response contains the features of a dataset as a GeoJSON FeatureCollection.
        """
        
        uri = URITemplate(self.baseuri + '/{owner}/{id}/features').expand(
            owner=self.username, id=dataset)

        params = {}
        if reverse:
            params['reverse'] = 'true'
        if start:
            params['start'] = start
        if limit:
            params['limit'] = int(limit)
        return self.session.get(uri, params=params)

    def read_feature(self, dataset, fid):
        """Retrieves (reads) a feature in a dataset.

        Parameters
        ----------
        dataset : str
            The dataset id.

        fid : str
            The feature id.

        Returns
        -------
        request.Response
            The response contains a GeoJSON representation of the feature.
        """
        
        uri = URITemplate(
            self.baseuri + '/{owner}/{did}/features/{fid}').expand(
                owner=self.username, did=dataset, fid=fid)
        return self.session.get(uri)

    def update_feature(self, dataset, fid, feature):
        """Inserts or updates a feature in a dataset.
           
        Parameters
        ----------
        dataset : str
            The dataset id.

        fid : str
            The feature id.
               
            If the dataset has no feature with the given feature id, 
            then a new feature will be created.

        feature : dict
            The GeoJSON feature object.

            This should be one individual GeoJSON feature and not a 
            GeoJSON FeatureCollection.

        Returns
        -------
        request.Response
            The response contains a GeoJSON representation of the new or updated feature.
        """
        
        uri = URITemplate(
            self.baseuri + '/{owner}/{did}/features/{fid}').expand(
                owner=self.username, did=dataset, fid=fid)
        return self.session.put(uri, json=feature)

    def delete_feature(self, dataset, fid):
        """Removes a feature from a dataset.

        Parameters
        ----------
        dataset : str
            The dataset id.

        fid : str
            The feature id.

        Returns
        -------
        HTTP status code.
        """
        
        uri = URITemplate(
            self.baseuri + '/{owner}/{did}/features/{fid}').expand(
                owner=self.username, did=dataset, fid=fid)
        return self.session.delete(uri)
