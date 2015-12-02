# Access Tokens

All Mapbox API's require an access token. Your Mapbox access token can be exported
into your environment

```bash

export MAPBOX_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"

```

and it will be found automatically when creating a new instance. We'll use the `Geocoder` in this 
example but the same applies for all `mapbox` classes.

```python

>>> from mapbox import Geocoder
>>> geocoder = Geocoder()
>>> import os
>>> geocoder.session.params['access_token'] == os.environ['MAPBOX_ACCESS_TOKEN']
True

```

Or it can be passed explicitly to the constructor.

```python


>>> YOUR_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
>>> geocoder = Geocoder(access_token=YOUR_ACCESS_TOKEN)

```

Best practice for access tokens and geocoding sources is to create a new
instance for each new access token or source dataset.


## Special considerations

You access token can be associated with different *scopes*. **TODO**
How to get an access token. **TODO**
