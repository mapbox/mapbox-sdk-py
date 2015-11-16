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

