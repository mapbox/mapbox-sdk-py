# Tilequery

The `Tilequery` class provides access to the Mapbox Tilequery API.  You can import it from either the `mapbox` module or the `mapbox.services.tilequery` module.

__mapbox__:

```python
>>> from mapbox import Tilequery

```

__mapbox.services.tilequery__:

```python
>>> from mapbox.services.tilequery import Tilequery

```

See https://www.mapbox.com/api-documentation/#tilequery for general documentation of the API.

Use of the Tilequery API requires an access token, which you should set in your environment.  For more information, see the [access tokens](access_tokens.md) documentation.

## Tilequery Method

The public method of the `Tilequery` class provides access to the Tilequery API and returns an instance of [`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).


## Usage: Retrieving Features

Instantiate `Tilequery`.

```python
>>> tilequery = Tilequery()

```

Call the `tilequery` method, passing in values for `map_id`, `lon`, and `lat`.  Pass in values for optional arguments as necessary - `radius`, `limit`, `dedupe`, `geometry`, and `layers`.

```python
>>> response = tilequery.tilequery("mapbox.mapbox-streets-v10", lon=0.0, lat=1.1)

```

Evaluate whether the request succeeded, and retrieve the features from the response object.

```python
>>> if response.status_code == 200:
...     features = response.json()

```
