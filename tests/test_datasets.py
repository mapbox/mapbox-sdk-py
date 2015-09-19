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
        'https://api.mapbox.com/datasets/v1/juser',
        body=body, status=200,
        content_type='application/json')

    response = mapbox.Datasets('juser').list()
    assert response.status_code == 200
    assert len(response.json()) == 2
