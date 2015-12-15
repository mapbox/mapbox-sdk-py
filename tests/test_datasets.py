import base64
import json

import responses

from mapbox.services.datasets import Datasets, batch, iter_features


username = 'testuser'
access_token = 'pk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))


def test_datasets_name():
    """Default name is set"""
    datasets = Datasets(access_token=access_token)
    assert datasets.username == username
    assert datasets.baseuri == 'https://api.mapbox.com/datasets/v1'


def test_iter_features_collection():
    src = json.dumps(
        {'type': 'FeatureCollection', 'features': [{'type': 'Feature'}]},
        indent=2).split('\n')
    assert list(iter_features(iter(src))) == [{'type': 'Feature'}]


def test_batch_features_collection():
    src = json.dumps(
        {'type': 'FeatureCollection', 'features': [{'type': 'Feature'}]},
        indent=2).split('\n')
    assert list(next(batch(iter_features(iter(src)), size=1))) == [{'type': 'Feature'}]


def test_iter_features_sequence():
    src = [json.dumps({'type': 'Feature'}), json.dumps({'type': 'Feature'})]
    assert list(iter_features(iter(src), is_sequence=True)) == [{'type': 'Feature'}, {'type': 'Feature'}]


def test_iter_features_rs_sequence():
    src = (u'\x1e' + 
            json.dumps(
                {'type': 'Feature', 'id': '1', 'properties': {'foo': 'bar'}},
                indent=2) +
            '\n'
            u'\x1e' + 
            json.dumps(
                {'type': 'Feature', 'id': '2', 'properties': {'foo': 'bar'}},
                indent=2)).split('\n')
    assert [ob['id'] for ob in iter_features(iter(src))] == ['1', '2']


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
        payload = json.loads(request.body)
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
        payload = json.loads(request.body)
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


@responses.activate
def test_dataset_update_features():
    """Features update works"""

    def request_callback(request):
        payload = json.loads(request.body)
        assert payload['put'] == [{'type': 'Feature'}]
        assert payload['delete'] == ['1']
        return (200, {}, "")

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(
            username, 'test', access_token),
        match_querystring=True,
        callback=request_callback)

    response = Datasets(access_token=access_token).update_features(
            'test', put=[{'type': 'Feature'}], delete=['1'])
    assert response.status_code == 200
