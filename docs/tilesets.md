# Tilesets

The `Tilesets` class provides access to the Mapbox Tilesets API.  You can import it from either the `mapbox` module or the `mapbox.services.tilesets` module.

__mapbox__:

```python
>>> from mapbox import Tilesets
```

__mapbox.services.tilesets__:

```python
>>> from mapbox.services.tilesets import Tilesets
```

See https://www.mapbox.com/api-documentation/#tilesets for general documentation of the API.

Use of the Tilesets API requires an access token, which you should set in your environment.  For more information, see the [access tokens](access_tokens.md) documentation.

## Tilesets Methods

The public method of the `Tilesets` class provides access to the Tilesets API and returns an instance of [`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage: Listing Tilesets

Instantiate `Tilesets`.

```python
>>> tilesets = Tilesets()
```

Call the `list_tilesets` method, passing in values for optional arguments as necessary - `tileset_type`, `visibility`, `sortby`, and `limit`.

```python
>>> response = tilesets.list_tilesets()
```

Evaluate whether the request succeeded, and retrieve the tileset object from the response object.

```python
>>> if response.status_code == 200:
...     tileset_object = response.get_json()
