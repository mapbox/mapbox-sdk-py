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
>>> new_id = create_resp.json()['id']

```

You can find it in your account's list of datasets.

```python
>>> listing_resp = datasets.list()
>>> new_id in [ds['id'] for ds in listing_resp.json()]
True

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

You can delete the dataset and it will no longer be present in your listing.

```python
>>> resp = datasets.delete_dataset(new_id)
>>> resp.status_code
204
>>> listing_resp = datasets.list()
>>> new_id in [ds['id'] for ds in listing_resp.json()]
False

```
