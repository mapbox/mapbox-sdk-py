# Uploads

The `Uploads` class from the `mapbox.services.uploads` module provides access
to the Mapbox Uploads API. You can also import it directly from the `mapbox`
module.

```python
>>> from mapbox import Uploader

```

See https://www.mapbox.com/developers/api/uploads/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information. To use the
Uploads API, you must use a token created with ``uploads:*`` scopes. See
https://www.mapbox.com/account/apps/.

## Upload methods

The methods of the `Uploads` class that provide access to the Uploads API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage

Then upload any supported file to your account using the ``Uploader``. The
name of the destination dataset can be any string of <= 32 chars. Choose one
suited to your application or generate one using, e.g., `uuid.uuid4().hex`.
In the example below, we use a string defined in a test fixture.

```python
>>> service = Uploader()
>>> dest_id = getfixture('uploads_dest_id') # 'uploads-test'
>>> response = service.upload('tests/twopoints.geojson', dest_id)
>>> response.status_code
201
>>> upload_id = response.json()['id']

```

You can check the status of the upload using the upload_id

```python
>>> response = service.status(upload_id).json()
>>> dest_id in response['tileset']
True

```

See ``import mapbox; help(mapbox.Uploader)`` for more detailed usage.
