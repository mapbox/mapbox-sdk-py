# mapbox-sdk-py

[![Build Status](https://travis-ci.org/mapbox/mapbox-sdk-py.svg?branch=master)](https://travis-ci.org/mapbox/mapbox-sdk-py)
[![Coverage Status](https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mapbox/mapbox-sdk-py?branch=master)

A Python client for Mapbox services

## Services

* [Geocoding](https://www.mapbox.com/developers/api/geocoding/)
  * Forward (place names ⇢  longitude, latitude)
  * Reverse (longitude, latitude ⇢ place names)

## Installation

```sh
$ pip install mapbox
```

## Usage

Basic usage of the geocoder:

```python
import mapbox

geocoder = mapbox.Geocoder(access_token='YOUR_ACCESS_TOKEN')
response = geocoder.fwd('Chester, NJ')

# response.json() returns the geocoding result as GeoJSON.
```

## Testing

```bash
pip install -e .[test]
py.test
```

## See Also

https://github.com/mapbox/mapbox-sdk-js
