# Access Tokens

All Mapbox APIs require an access token. Thus all service object constructors
take an `access_token` keyword argument. Access can be granted to a geocoding
service, for example, like so:

```python
>>> from mapbox import Geocoder
>>> geocoder = Geocoder(access_token="pk.YOUR_ACCESS_TOKEN")
```

Please note that an actual token string must be used. Tokens may be generated
using the web application at [https://www.mapbox.com/account/access-tokens](https://www.mapbox.com/account/access-tokens).

Your Mapbox access token can also be set in the environment of your program

```bash
export MAPBOX_ACCESS_TOKEN="pk.YOUR_ACCESS_TOKEN"
```

and it will be found automatically when creating a new instance. We'll use the
`Geocoder` in this example but the same applies for all `mapbox` classes.

```python
>>> geocoder = Geocoder()
>>> import os
>>> geocoder.session.params['access_token'] == os.environ['MAPBOX_ACCESS_TOKEN']
True
```

Best practice for access tokens and geocoding sources is to create a new
instance for each new access token or source dataset.


## Special considerations

You access token can be associated with different *scopes*. **TODO**
How to get an access token. **TODO**
