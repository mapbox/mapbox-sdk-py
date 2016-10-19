import base64
import json

import responses

from mapbox.services.datasets import Datasets


username = 'testuser'
access_token = 'pk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))


def test_datasets_service_properties():
    """Get expected username and baseuri."""
    datasets = Datasets(access_token=access_token)
    assert datasets.username == username
    assert datasets.baseuri == 'https://api.mapbox.com/datasets/v1'


@responses.activate
def test_datasets_list():
    """Listing datasets works"""

    body = '''
[
  {
    "owner": "testuser",
    "id": "ds1",
    "created": "2015-09-19",
    "modified": "2015-09-19"
  },
  {
    "owner": "testuser",
    "id": "ds2",
    "created": "2015-09-19",
    "modified": "2015-09-19"
  }
]
'''

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).list()
    assert response.status_code == 200
    assert [item['id'] for item in response.json()] == ['ds1', 'ds2']


@responses.activate
def test_datasets_create():
    """Creating a named and described dataset works."""

    def request_callback(request):
        payload = json.loads(request.body.decode())
        resp_body = {
            'owner': username,
            'id': 'new',
            'name': payload['name'],
            'description': payload['description'],
            'created': '2015-09-19',
            'modified': '2015-09-19'}
        headers = {}
        return (200, headers, json.dumps(resp_body))

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        callback=request_callback)

    response = Datasets(access_token=access_token).create(
        name='things', description='a collection of things')
    assert response.status_code == 200
    assert response.json()['name'] == 'things'
    assert response.json()['description'] == 'a collection of things'


@responses.activate
def test_dataset_read():
    """Dataset name and description reading works."""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(
            username, 'test', access_token),
        match_querystring=True,
        body=json.dumps(
            {'name': 'things', 'description': 'a collection of things'}),
        status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).read_dataset('test')
    assert response.status_code == 200
    assert response.json()['name'] == 'things'
    assert response.json()['description'] == 'a collection of things'

@responses.activate
def test_dataset_update():
    """Updating dataset name and description works."""

    def request_callback(request):
        payload = json.loads(request.body.decode())
        resp_body = {
            'owner': username,
            'id': 'foo',
            'name': payload['name'],
            'description': payload['description'],
            'created': '2015-09-19',
            'modified': '2015-09-19'}
        headers = {}
        return (200, headers, json.dumps(resp_body))

    responses.add_callback(
        responses.PATCH,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(
            username, 'foo', access_token),
        match_querystring=True,
        callback=request_callback)

    response = Datasets(access_token=access_token).update_dataset(
        'foo', name='things', description='a collection of things')
    assert response.status_code == 200
    assert response.json()['name'] == 'things'
    assert response.json()['description'] == 'a collection of things'


@responses.activate
def test_delete_dataset():
    """Delete a dataset"""

    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(
            username, 'test', access_token),
        match_querystring=True,
        status=204)

    response = Datasets(access_token=access_token).delete_dataset('test')
    assert response.status_code == 204


@responses.activate
def test_dataset_list_features():
    """Features retrieval work"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(
            username, 'test', access_token),
        match_querystring=True,
        body=json.dumps({'type': 'FeatureCollection'}),
        status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).list_features('test')
    assert response.status_code == 200
    assert response.json()['type'] == 'FeatureCollection'


@responses.activate
def test_dataset_list_features_reverse():
    """Features retrieval in reverse works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&reverse=true'.format(
            username, 'test', access_token),
        match_querystring=True,
        body=json.dumps({'type': 'FeatureCollection'}),
        status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).list_features(
        'test', reverse=True)
    assert response.status_code == 200
    assert response.json()['type'] == 'FeatureCollection'


@responses.activate
def test_dataset_list_features_pagination():
    """Features retrieval pagination works"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=1&limit=1'.format(
            username, 'test', access_token),
        match_querystring=True,
        body=json.dumps({'type': 'FeatureCollection'}),
        status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).list_features(
        'test', start=1, limit=1)
    assert response.status_code == 200
    assert response.json()['type'] == 'FeatureCollection'


# Tests of feature-scoped methods.

@responses.activate
def test_read_feature():
    """Feature read works."""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(
            username, 'test', '1', access_token),
        match_querystring=True,
        body=json.dumps({'type': 'Feature', 'id': '1'}),
        status=200,
        content_type='application/json')

    response = Datasets(access_token=access_token).read_feature('test', '1')
    assert response.status_code == 200
    assert response.json()['type'] == 'Feature'
    assert response.json()['id'] == '1'


@responses.activate
def test_update_feature():
    """Feature update works."""

    def request_callback(request):
        payload = json.loads(request.body.decode())
        assert payload == {'type': 'Feature'}
        return (200, {}, "")

    responses.add_callback(
        responses.PUT,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(
            username, 'test', '1', access_token),
        match_querystring=True,
        callback=request_callback)

    response = Datasets(access_token=access_token).update_feature(
            'test', '1', {'type': 'Feature'})
    assert response.status_code == 200


@responses.activate
def test_delete_feature():
    """Deletes a feature."""

    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(
            username, 'test', '1', access_token),
        match_querystring=True,
        status=204)

    response = Datasets(access_token=access_token).delete_feature('test', '1')
    assert response.status_code == 204
