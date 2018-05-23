# Maps

The `Maps` class provides access to the Mapbox Maps API.  You can import it from either the `mapbox` module or the `mapbox.services.maps` module.

__mapbox__:

```python
>>> from mapbox import Maps
```

__mapbox.services.maps__:

```python
>>> from mapbox.services.maps import Maps
```

See https://www.mapbox.com/api-documentation/#maps for general documentation of the API.

Use of the Maps API requires an access token, which you should set in your environment.  For more information, see the [access tokens](access_tokens.md) documentation.

## Maps Methods

The public methods of the `Maps` class provide access to the Maps API and return an instance of [`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage: Retrieving Tiles

Instantiate `Maps`.

```python
>>> maps = Maps()
```

Call the `get_tile` method, passing in values for `map_id`, `z` (zoom), `x` (column), and `y` (row).  Pass in values for optional arguments as necessary - `retina` (double scale), `file_format`, `style_id`, and `timestamp`.

```python
>>> response = maps.get_tile("mapbox.streets", z=0, x=0, y=0)
```

Evaluate whether the request succeeded, and retrieve the tile from the response object.

```python
>>> if response.status_code == 200:
...     with open("./0.png", "wb") as output:
...         output.write(response.content)
```

## Usage: Retrieving HTML Slippy Maps

Instantiate `Maps`.

```python
>>> maps = Maps()
```

Call the `get_html_slippy_map` method, passing in a value for `map_id`.  Pass in values for optional arguments as necessary - `options` (map controls and behaviors), `z`, `lat`, and `lon`.

```python
>>> response = maps.get_html_slippy_map("mapbox.streets")
```

Evaluate whether the request succeeded, and retrieve the HTML slippy map from the response object.

```python
>>> if response.status_code == 200:
...     with open("./mapbox.streets.html", "w") as output:
...         output.write(response.text)
```

## Usage: Retrieving Features from Mapbox Editor Projects

Instantiate `Maps`.

```python
>>> maps = Maps()
```

Call the `get_vector_features` method, passing in a value for `map_id`.  Pass in a value for the optional argument, `feature_format`, as necessary.

```python
>>> response = maps.get_html_slippy_map("mapbox.streets")
```

Evaluate whether the request succeeded, and retrieve the vector features from the response object.  The approach will depend upon the format of the vector features.

__GeoJSON__:

```python
>>> if response.status_code == 200:
...     features = response.get_json()
```

__KML__:

```python
>>> if response.status_code == 200:
...     with open("./features.kml", "w") as output:
...         output.write(response.text)
```

## Usage: Retrieving TileJSON Metadata

Instantiate `Maps`.

```python
>>> maps = Maps()
```

Call the `get_tilejson_metadata` method, passing in a value for `map_id`.  Pass in a value for the optional argument, `secure`, as necessary.

```python
>>> response = maps.get_tilejson_metadata("mapbox.streets")
```

Evaluate whether the request succeeded, and retrieve the TileJSON metadata from the response object.

```python
>>> if response.status_code == 200:
...     features = response.get_json()
```

## Usage: Retrieving a Standalone Marker

Instantiate `Maps`.

```python
>>> maps = Maps()
```

Call the `get_standalone_marker` method, passing in a value for `marker_name`.  Pass in values for optional arguments as necessary - 
`label`, `color`, and `retina`.

```python
>>> response = maps.get_standalone_marker(marker_name="pin-s")
```

Evaluate whether the request succeeded, and retrieve the marker from the response object.

```python
>>> if response.status_code == 200:
...     with open("pin-s.png", "wb") as output:
...         output.write(response.content)
```
