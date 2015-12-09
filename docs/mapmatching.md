# Map Matching

The `MapMatcher` class from the `mapbox.services.mapmatching` module provides
access to the Mapbox Map Matching API. You can also import it directly from the
`mapbox` module.

```python
>>> from mapbox import MapMatcher

```

See https://www.mapbox.com/developers/api/map-matching/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information.

## MapMatcher methods

The methods of the `MapMatcher` class return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

In addition to the `json()` method that returns Python data parsed from the
API, the responses provide a `geojson()` method that converts that
data to a GeoJSON like form.

## Usage

The Mapbox Map Matching API lets you take recorded GPS traces and snap them to the OpenStreetMap road and path network. This is helpful for aligning noisy traces and displaying them cleanly on a map.

The Map Matching API is limited to 60 requests per minute and results must be displayed on a Mapbox map using one of our SDKs. For high volume or other use cases, contact us.


```python
>>> service = MapMatcher()

```

The input data to the Map Matcher must be a single GeoJSON-like Feature with a LineString geometry.
The optional `coordTimes` property should be an array of the same length as the coordinates
containing timestamps to help make the matching more accurate.

```
>>> line = {
...     "type": "Feature",
...     "properties": {
...         "coordTimes": [
...             "2015-04-21T06:00:00Z",
...             "2015-04-21T06:00:05Z",
...             "2015-04-21T06:00:10Z",
...             "2015-04-21T06:00:15Z",
...             "2015-04-21T06:00:20Z"]},
...     "geometry": {
...         "type": "LineString",
...         "coordinates": [
...             [13.418946862220764, 52.50055852688439],
...             [13.419011235237122, 52.50113000479732],
...             [13.419756889343262, 52.50171780290061],
...             [13.419885635375975, 52.50237416816131],
...             [13.420631289482117, 52.50294888790448]]}}

```

Use the `surface()` method to query the terrain dataset.

```python
>>> response = service.match(line, profile='mapbox.driving')
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/json; charset=utf-8'

```

The response geojson contains a FeatureCollection with a single feature,
with the new LineString corrected to match segments from the selected profile.

```python
>>> corrected = response.geojson()['features'][0]
>>> corrected['geometry']['type']
'LineString'
>>> corrected['geometry'] == line['geometry']
False
>>> len(corrected['geometry']) == len(line['geometry'])
True

```

See ``import mapbox; help(mapbox.MapMatcher)`` for more detailed usage.
