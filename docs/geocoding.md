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
>>> response.headers['X-Rate-Limit-Interval']
'60'
>>> response.headers['X-Rate-Limit-Limit'] # doctest: +SKIP
'600'
>>> response.headers['X-Rate-Limit-Reset'] # doctest: +SKIP
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

```

## Forward geocoding

Places at an address may be found using `Geocoder.forward()`.

```python

>>> response = geocoder.forward("200 queen street")
>>> response.status_code
200
>>> response.headers['Content-Type']
'application/vnd.geo+json; charset=utf-8'
>>> first = response.geojson()['features'][0]
>>> first['place_name']
'200 Queen St...'

```

## Forward geocoding with proximity

Place results may be biased toward a given longitude and latitude.

```python

>>> response = geocoder.forward(
...     "200 queen street", lon=-66.05, lat=45.27)
>>> response.status_code
200
>>> first = response.geojson()['features'][0]
>>> first['place_name']
'200 Queen St...'
>>> [int(coord) for coord in first['geometry']['coordinates']]
[-66, 45]

```

## Forward geocoding with bounding box

Place results may be limited to those falling within a given bounding box.

```python

>>> response = geocoder.forward(
...     "washington", bbox=[-78.338320,38.520792,-77.935454,38.864909], types=('place',))
>>> response.status_code
200
>>> first = response.geojson()['features'][0]
>>> first['place_name']
'Washington, Virginia, United States'
>>> [round(coord, 2) for coord in first['geometry']['coordinates']]
[-78.16, 38.71]

```
## Forward geocoding with limited results

The number of results may be limited.

```python

>>> response = geocoder.forward(
...     "washington", limit=3)
>>> response.status_code
200
>>> len(response.geojson()['features'])
3

```

## Reverse geocoding

Places at a longitude, latitude point may be found using `Geocoder.reverse()`.

```python

>>> response = geocoder.reverse(lon=-73.989, lat=40.733)
>>> response.status_code
200
>>> features = sorted(response.geojson()['features'], key=lambda x: x['place_name'])
>>> for f in features:
...     print('{place_name}: {id}'.format(**f))
10003... postcode...
120 East 13th Street, Manhattan, New York, New York 10003... address...
Greenwich Village... neighborhood...
Manhattan... locality...
New York, New York... postcode...
New York, New York... place...
New York... region...
United States: country...

```

## Reverse geocoding with limited results by location type

The number of results may be limited by a single type

```python

>>> response = geocoder.reverse(lon=-73.989, lat=40.733, limit=1, types=['country'])
>>> response.status_code
200
>>> features = response.geojson()['features']
>>> len(features)
1
>>> print('{place_name}: {id}'.format(**features[0]))
United States: country...

```

## Filtering by country code

`forward()` can be restricted to a list of country codes. No results in Canada
will be returned if the query is filtered for 'us' results only.

```python

>>> response = geocoder.forward("200 queen street", country=['us'])
>>> response.status_code
200
>>> any(['Canada' in f['place_name'] for f in response.geojson()['features']])
False

```

## Filtering by type

Both `forward()` and `reverse()` can be restricted to one or more place types.

```python

>>> response = geocoder.reverse(
...     lon=-73.989, lat=40.733, types=['poi'])
>>> response.status_code
200
>>> features = response.geojson()['features']
>>> all([f['id'].startswith('poi') for f in features])
True

```
