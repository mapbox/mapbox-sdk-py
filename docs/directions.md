# Directions

The `Directions` class from the `mapbox.services.directions` module provides
access to the Mapbox Directions API. You can also import it directly from the
`mapbox` module.

```python
>>> from mapbox import Directions

```

See https://www.mapbox.com/api-documentation/navigation/#directions for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information.

## Directions methods

The methods of the `Directions` class that provide access to the Directions API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).
In addition to the `json()` method that returns Python data parsed from the
API, the `Directions` responses provide a `geojson()` method that converts that
data to a GeoJSON like form.

## Usage

To get travel directions between waypoints, you can use the Directions API to
route up to 25 points.  Each of your input waypoints will be visited in order
and should be represented by a GeoJSON point feature.

```python
>>> service = Directions(access_token="pk.YOUR_ACCESS_TOKEN")

```

The input waypoints to the `directions` method are
[features](input_features.md), typically GeoJSON-like feature dictionaries.

```python
>>> origin = {
...    'type': 'Feature',
...    'properties': {'name': 'Portland, OR'},
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-122.7282, 45.5801]}}
>>> destination = {
...    'type': 'Feature',
...    'properties': {'name': 'Bend, OR'},
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-121.3153, 44.0582]}}

```

The `directions()` method can be called with a list of features and the desired
profile.

```python
>>> response = service.directions([origin, destination],
...     'mapbox.driving')
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/json; charset=utf-8'

```

It returns a response object with a `geojson()` method for accessing the
route(s) as a GeoJSON-like FeatureCollection dictionary.

```python
>>> driving_routes = response.geojson()
>>> driving_routes['features'][0]['geometry']['type']
'LineString'

```

See ``import mapbox; help(mapbox.Directions)`` for more detailed usage.
