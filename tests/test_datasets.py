import json
import responses

import mapbox
from mapbox.datasets import Dataset, Datasets, batch, iter_features


def test_datasets_name():
    """Default name is set"""
    datasets = Datasets('juser')
    assert datasets.name == 'juser'
    assert datasets.baseuri == 'https://api.mapbox.com/datasets/v1'


def test_iter_features_collection():
    src = json.dumps(
        {'type': 'FeatureCollection', 'features': [{'type': 'Feature'}]},
        indent=2).split('\n')
    assert list(iter_features(iter(src))) == [{'type': 'Feature'}]


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
    "owner": "juser",
    "id": "ds1",
    "created": "2015-09-19",
    "modified": "2015-09-19"
  },
  {
    "owner": "juser",
    "id": "ds2",
    "created": "2015-09-19",
    "modified": "2015-09-19"
  }
]
'''

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/juser?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    response = Datasets('juser', access_token='pk.test').list()
    assert response.status_code == 200
    assert [item['id'] for item in response.json()] == ['ds1', 'ds2']


@responses.activate
def test_datasets_create_with_name_description():
    """Creating a named and described dataset works"""

    def request_callback(request):
        payload = json.loads(request.body)
        resp_body = {
            'owner': 'juser',
            'id': 'new',
            'name': payload['name'],
            'description': payload['description'],
            'created': '2015-09-19',
            'modified': '2015-09-19'}
        headers = {}
        return (200, headers, json.dumps(resp_body))

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/juser?access_token=pk.test',
        match_querystring=True,
        callback=request_callback)

    response = Datasets('juser', access_token='pk.test').create(
        name='things', description='a collection of things')
    assert response.status_code == 200
    assert response.json()['name'] == 'things'
    assert response.json()['description'] == 'a collection of things'


@responses.activate
def test_dataset_retrieve_features():
    """Features retrieval work"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/juser/test/features?access_token=pk.test',
        match_querystring=True,
        body=json.dumps({'type': 'FeatureCollection'}),
        status=200,
        content_type='application/json')

    response = Dataset(
        'juser', 'test', access_token='pk.test').retrieve_features()
    assert response.status_code == 200
    assert response.json()['type'] == 'FeatureCollection'


@responses.activate
def test_dataset_update_features():
    """Features update works"""

    def request_callback(request):
        payload = json.loads(request.body)
        assert payload['put'] == [{'type': 'Feature'}]
        return (200, {}, "")

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/juser/test/features?access_token=pk.test',
        match_querystring=True,
        callback=request_callback)

    response = Dataset(
        'juser', 'test', access_token='pk.test').update_features(
            put=[{'type': 'Feature'}])
    assert response.status_code == 200
