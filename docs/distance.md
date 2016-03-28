# Distance

The `Distance` class from the `mapbox.services.distance` module provides
access to the Mapbox Distance API. You can also import it directly from the
`mapbox` module.

```python
>>> from mapbox import Distance

```

See https://www.mapbox.com/developers/api/distance/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information.

## Distance methods

The methods of the `Distance` class that provide access to the Distance API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).
If the response is successful, the `json()` method returns Python data parsed
directly from the API.

## Usage

If you need to optimize travel between several waypoints, you can use the
Distance API to create a "Distance Matrix" showing travel times between all
waypoints.  Each of your input waypoints should be a GeoJSON point feature.

```python
>>> service = Distance()

```

The input waypoints to the `directions` method are
[features](input_features.md), typically GeoJSON-like feature dictionaries.

```python
>>> portland = {
...    'type': 'Feature',
...    'properties': {'name': 'Portland, OR'},
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-122.7282, 45.5801]}}
>>> bend = {
...    'type': 'Feature',
...    'properties': {'name': 'Bend, OR'},
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-121.3153, 44.0582]}}
>>> corvallis = {
...    'type': 'Feature',
...    'properties': {'name': 'Corvallis, OR'},
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-123.268, 44.5639]}}

```

The `distance` method can be called with a list of point features and the
travel profile.

```python
>>> response = service.distances([portland, bend, corvallis], 'driving')
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/json; charset=utf-8'

```

And the response JSON contains a durations matrix, a 2-D list with travel
times (seconds) between all input waypoints. The diagonal will be
zeros.

```python
>>> from pprint import pprint
>>> pprint(response.json()['durations'])
[[0, ..., ...], [..., 0, ...], [..., ..., 0]]

```

See ``import mapbox; help(mapbox.Distance)`` for more detailed usage.
