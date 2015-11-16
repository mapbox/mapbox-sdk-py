SDK Usage Examples
==================

# Module import

The Mapbox Python SDK is accessed from classes and methods of the `mapbox`
module.

```python

>>> import mapbox

```

# Access Tokens

Your Mapbox access token can be exported into your environment

```bash

export MAPBOX_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"

```

or can be passed explicitly to service constructors.

```python

>>> import os
>>> YOUR_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
>>> geocoder = mapbox.Geocoder(access_token=YOUR_ACCESS_TOKEN)

```

# Geocoding

```python

>>> geocoder = mapbox.Geocoder()

```

## Coverage

## Limits

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
>>> data = response.json()
>>> data['type'] == 'FeatureCollection'
True
>>> for key in sorted(data.keys()):
...     print(key)
attribution
features
query
type
>>> for token in data['query']:
...     print(token)
chester
nj

```

Zero or more objects that extend GeoJSON's `Feature` are contained in the
collection, sorted by relevance to the query.

```python

>>> first = data['features'][0]
>>> first['type'] == 'Feature'
True
>>> for key in sorted(first.keys()):
...     print(key)
bbox
center
context
geometry
id
place_name
properties
relevance
text
type

```

## Forward geocoding

```python

>>> response = geocoder.forward('1600 pennsylvania ave nw')
>>> response.status_code
200

```
