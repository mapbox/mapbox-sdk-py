# Surface

The `Surface` class from the `mapbox.services.surface` module provides
access to the Mapbox Surface API. You can also import it directly from the
`mapbox` module.

```python
>>> from mapbox import Surface

```

See https://www.mapbox.com/developers/api/surface/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access tokens](access_tokens.md) documentation for more information.

## Surface methods

The methods of the `Surface` class that provide access to the Surface API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage

To query vector tile attributes along a series of points or a line, you can use the Surface API.
For example, you could create an elevation profile against a GeoJSON LineString feature or
list of GeoJSON point features.


```python
>>> service = Surface()

```

Create a series of point features

```python
>>> features = [{
...    'type': 'Feature',
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-112.084004, 36.053220]}}, {
...    'type': 'Feature',
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-112.083914, 36.053573]}}, {
...    'type': 'Feature',
...    'geometry': {
...        'type': 'Point',
...        'coordinates': [-112.083965, 36.053845]}}]

```

Use the `surface` method to query the terrain dataset

```python
>>> response = service.surface(features, mapid='mapbox.mapbox-terrain-v1', layer='contour', fields=['ele'])
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/json; charset=utf-8'

```

And the response geojson FeatureCollection contains your input points with an `ele` property
```python
>>> points = response.geojson()
>>> [f['properties']['ele'] for f in points['features']]
[2186.361304424316, 2187.6233827411997, 2163.921475128245]

```

See ``import mapbox; help(mapbox.Surface)`` for more detailed usage.

