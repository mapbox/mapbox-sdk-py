# Uploads

The `Uploads` class from the `mapbox.services.uploads` module provides
access to the Mapbox Uploads API. You can also import it directly from the
`mapbox` module.

```python
>>> from mapbox import Uploader

```

See https://www.mapbox.com/developers/api/uploads/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access tokens](access_tokens.md) documentation for more information. To use the Uploads API, you must use a token created with ``uploads:*`` scopes. See https://www.mapbox.com/account/apps/.

## Upload methods

The methods of the `Uploads` class that provide access to the Uploads API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage
Then upload any supported file to your account using the ``Uploader`` 

```python
>>> service = Uploader('username')

```

```python
>>> response = service.upload('RGB.byte.tif', 'RGB-byte-tif')
>>> upload_id = resp.json()['id']

```


```python
>>> response = service.status(upload_id).json()
>>> resp['complete']
False
>>> resp['tileset']
"username.RGB-byte-tif"
```

See ``import mapbox; help(mapbox.Uploader)`` for more detailed usage.
