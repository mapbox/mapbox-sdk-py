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

Upload any supported file to your account using the ``Uploader``. The name of
the destination dataset can be any string of <= 32 chars. Choose one suited to
your application or generate one using, e.g., `uuid.uuid4().hex`.

```python
>>> service = Uploader()
>>> with open('tests/twopoints.geojson', 'rb') as fileobj:
...     resp = service.upload(fileobj, 'test-tileset')
...
>>> resp.status_code
201

```

The "201 Created" response indicates that your data file has been received and
is being processed. Processing may take several seconds or minutes depending on
the size of your data file. You may poll the Upload API to determine if the
processing has finished using the upload identifier from the the body of the
response.

```python
>>> from time import sleep
>>> info = resp.json()
>>> upload_id = info['id']
>>> for i in range(1, 5):
...     resp = service.status(upload_id)
...     info = resp.json()
...     if info['complete']:
...         print("Tileset completed")
...         break
...     sleep((5**i - 1)/2)
... else:
...     print("Maximum polling requests exceeded")
...
Tileset completed

```

See ``import mapbox; help(mapbox.Uploader)`` for more detailed usage.
