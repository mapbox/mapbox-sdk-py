# Geocoding

The `Geocoder` class from the `mapbox.services.geocoding` module provides
access to the Mapbox Geocoding API. You can also import it directly from the
`mapbox` module.

```python

>>> from mapbox import Geocoder

```

See https://www.mapbox.com/developers/api/geocoding/ for general documentation
of the API.

Your Mapbox access token should be set in your environment; see the [access tokens](access_tokens.md) documentation for more information.

## Geocoding sources

If your account enables access to the *mapbox.places-permanent* dataset, you
can use it specify it with a keyword argument to the `Geocoder` constructor.

```python

>>> perm_geocoder = Geocoder(name='mapbox.places-permanent')

```

For the default *mapbox.places* geocoder, you don't need to specify any arguments

```python

>>> geocoder = Geocoder()

```

## Geocoder methods

The methods of the `Geocoder` class that provide access to the Geocoding API
return an instance of
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).
In addition to the `json()` method that returns Python data parsed from the
API, the `Geocoder` responses provide a `geojson()` method that converts that
data to a GeoJSON like form.

## Limits

The Geocoding API is rate limited. Details of the limits and current state
are accessible through response headers.

```python

>>> response = geocoder.forward('Chester, NJ')
>>> response.headers['x-rate-limit-interval']
'60'
>>> response.headers['x-rate-limit-limit']
'600'
>>> response.headers['x-rate-limit-remaining'] # doctest: +SKIP
'599'
>>> response.headers['x-rate-limit-reset'] # doctest: +SKIP
'1447701074'

```

## Response format

The JSON response extends GeoJSON's `FeatureCollection`.

```python

>>> response = geocoder.forward('Chester, NJ')
>>> collection = response.json()
>>> collection['type'] == 'FeatureCollection'
True
>>> sorted(collection.keys())
['attribution', 'features', 'query', 'type']
>>> collection['query']
['chester', 'nj']

```

Zero or more objects that extend GeoJSON's `Feature` are contained in the
collection, sorted by relevance to the query.

```python

>>> first = collection['features'][0]
>>> first['type'] == 'Feature'
True
>>> sorted(first.keys())
['bbox', 'center', 'context', 'geometry', 'id', 'place_name', 'properties', 'relevance', 'text', 'type']

```

## Forward geocoding

Places at an address may be found using `Geocoder.forward()`.

```python

>>> response = geocoder.forward("200 queen street")
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/vnd.geo+json; charset=utf-8'
>>> response.geojson()['features'][0]['place_name']
'200 Queen St W, Toronto, M5T 1T9, Canada'

```

## Forward geocoding with proximity

Place results may be biased toward a given longitude and latitude.

```python

>>> response = geocoder.forward(
...     "200 queen street", lon=-66.1, lat=45.3)
>>> response.status_code
200
>>> response.geojson()['features'][0]['place_name']
'200 Queen St, Saint John, E2L 2X1, Canada'

```

## Reverse geocoding

Places at a longitude, latitude point may be found using `Geocoder.reverse()`.

```python

>>> response = geocoder.reverse(lon=-73.989, lat=40.733)
>>> response.status_code
200
>>> for f in response.geojson()['features']:
...     print('{place_name}: {id}'.format(**f))
Atlas Installation, 124 E 13th St, New York, New York 10003, United States: poi...
Gramercy-Flatiron, New York, 10003, New York, United States: neighborhood...
New York, New York, United States: place...
10003, New York, United States: postcode...
New York, United States: region...
United States: country...

```

## Filtering by type

Both `forward()` and `reverse()` can be restricted to one or more place types.

```python

>>> response = geocoder.reverse(
...     lon=-73.989, lat=40.733, types=['poi', 'neighborhood'])
>>> response.status_code
200
>>> for f in response.geojson()['features']:
...     print('{place_name}: {id}'.format(**f))
Atlas Installation, 124 E 13th St, New York, New York 10003, United States: poi...
Gramercy-Flatiron, New York, 10003, New York, United States: neighborhood...

```
