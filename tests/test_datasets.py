import json
import responses

import mapbox


def test_datasets_name():
    """Default name is set"""
    datasets = mapbox.Datasets('juser')
    assert datasets.name == 'juser'
    assert datasets.baseuri == 'https://api.mapbox.com/datasets/v1'


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

    response = mapbox.Datasets('juser', access_token='pk.test').list()
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

    response = mapbox.Datasets('juser', access_token='pk.test').create(
        name='things', description='a collection of things')
    assert response.status_code == 200
    assert response.json()['name'] == 'things'
    assert response.json()['description'] == 'a collection of things'
