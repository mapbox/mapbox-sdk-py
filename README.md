# mapbox-sdk-py

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
