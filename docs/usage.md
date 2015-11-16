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
>>> geocoder = mapbox.Geocoder(access_token="YOUR_ACCESS_TOKEN")

```

# Geocoding

```python

>>> geocoder = mapbox.Geocoder(access_token='YOUR_ACCESS_TOKEN')

```
