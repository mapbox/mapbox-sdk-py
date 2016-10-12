# Datasets

The `Datasets` class from the `mapbox.services.datasets` module provides access
to the Mapbox Datasets API. You can also import it directly from the `mapbox`
module.

```python
>>> from mapbox import Datasets

```

See https://www.mapbox.com/developers/api/datasets/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information. To use the
Datasets API, you must use a token created with ``datasets:*`` scopes. See
https://www.mapbox.com/account/apps/.

## Upload methods

The methods of the `Datasets` class that provide access to the Datasets API
generally take dataset id and feature id arguments and return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage

Create a new dataset using the `Dataset` class, giving it a name and
description. The `id` of the created dataset is in JSON data of the response.

```python
>>> datasets = Datasets()
>>> create_resp = datasets.create(
...     name='example', description='An example dataset')
>>> new = create_resp.json()
>>> new['name']
'example'
>>> new['description']
'An example dataset'
>>> new_id = new['id']

```

You can find it in your account's list of datasets.

```python
>>> listing_resp = datasets.list()
>>> [ds['id'] for ds in listing_resp.json()]
[...]

```

Instead of scanning the list for attributes of the dataset, you can read
them directly by dataset id.

```python
>>> attrs = datasets.read_dataset(new_id).json()
>>> attrs['id'] == new_id
True
>>> attrs['name']
'example'
>>> attrs['description']
'An example dataset'

```

If you want to change a dataset's name or description, you can.

```python
>>> attrs = datasets.update_dataset(
...     new_id, name='updated example', description='An updated example dataset'
...     ).json()
>>> # attrs = datasets.read_dataset(new_id).json()
>>> attrs['id'] == new_id
True
>>> attrs['name']
'updated example'
>>> attrs['description']
'An updated example dataset'

```

You can delete the dataset and it will no longer be present in your listing.

```python
>>> resp = datasets.delete_dataset(new_id)
>>> resp.status_code
204
>>> listing_resp = datasets.list()
>>> new_id in [ds['id'] for ds in listing_resp.json()]
False

```

## Dataset features

The main point of a dataset is store a collection of GeoJSON features. Let us
create a new dataset and then add a GeoJSON feature to it.

```python
>>> resp = datasets.create(
...     name='features-example', description='An example dataset with features')
>>> new_id = resp.json()['id']
>>> feature = {
...     'type': 'Feature', 'id': '1', 'properties': {'name': 'Insula Nulla'},
...     'geometry': {'type': 'Point', 'coordinates': [0, 0]}}
>>> resp = datasets.batch_update_features(new_id, put=[feature])
>>> resp.status_code
200

```

In the feature collection of the dataset you will see this feature.

```python
>>> collection = datasets.list_features(new_id).json()
>>> len(collection['features'])
1
>>> first = collection['features'][0]
>>> first['id']
'1'
>>> first['properties']['name']
'Insula Nulla'

```

Using the same `batch_update_features()` method, you can modify or delete
up to 100 features.

```python
>>> feature2 = {
...     'type': 'Feature', 'id': '2', 'properties': {'name': 'Insula Nulla B'},
...     'geometry': {'type': 'Point', 'coordinates': [0, 0]}}
>>> resp = datasets.batch_update_features(new_id, put=[feature2], delete=['1'])
>>> resp.status_code
200

```

Replication of the updates across data centers takes a small but finite amount
of time. Your next call to `datasets.list_features()` may not reflect the most
recent updates.

## Individual feature access

You can also read, update, and delete features individually.

### Read

The `read_feature()` method has the semantics of HTTP GET.

```python
>>> resp = datasets.read_feature(new_id, '2')
>>> resp.status_code
200
>>> feature = resp.json()
>>> feature['id']
'2'
>>> feature['properties']['name']
'Insula Nulla B'

```

### Update

The `update_feature()` method has the semantics of HTTP PUT. If there is no
feature in the dataset with the given id, a new feature will be created.

```python
>>> update = {
...     'type': 'Feature', 'id': '2', 'properties': {'name': 'Insula Nulla C'},
...     'geometry': {'type': 'Point', 'coordinates': [0, 0]}}
>>> update = datasets.update_feature(new_id, '2', update).json()
>>> update['id']
'2'
>>> update['properties']['name']
'Insula Nulla C'

```

### Delete

The `delete_feature()` method has the semantics of HTTP DELETE.

```python
>>> resp = datasets.delete_feature(new_id, '2')
>>> resp.status_code
204

```

Finally, let's clean up the features example dataset.

```python
>>> resp = datasets.delete_dataset(new_id)
>>> resp.status_code
204
>>> listing_resp = datasets.list()
>>> [ds['id'] for ds in listing_resp.json()]
[...]

```

