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

Upload any supported file to your account using the ``Uploader``. The
name of the destination dataset can be any string of <= 32 chars. Choose one
suited to your application or generate one using, e.g., `uuid.uuid4().hex`.
In the example below, we use a string defined in a test fixture.

```python
>>> service = Uploader()
>>> from time import sleep
>>> from random import randint
>>> mapid = getfixture('uploads_dest_id') # 'uploads-test'
>>> with open('tests/twopoints.geojson', 'rb') as src:
...     upload_resp = service.upload(src, mapid)
...
>>> if upload_resp.status_code == 422:
...     for i in range(5):
...         sleep(5)
...         with open('tests/twopoints.geojson', 'rb') as src:
...             upload_resp = service.upload(src, mapid)
...         if upload_resp.status_code != 422:
...             break

```

This 201 Created response indicates that your data file has been received
and is being processed. Poll the Upload API to determine if the processing
has finished using the upload identifier from the the body of the above
response.

```python
>>> upload_resp.status_code
201
>>> upload_id = upload_resp.json()['id']
>>> for i in range(5):
...     status_resp = service.status(upload_id).json()
...     if status_resp['complete']:
...         break
...     sleep(5)
...
>>> mapid in status_resp['tileset']
True

```

See ``import mapbox; help(mapbox.Uploader)`` for more detailed usage.
