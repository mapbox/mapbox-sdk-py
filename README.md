# mapbox-sdk-py

[![Build Status](https://travis-ci.org/mapbox/mapbox-sdk-py.svg?branch=master)](https://travis-ci.org/mapbox/mapbox-sdk-py)
[![Coverage Status](https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mapbox/mapbox-sdk-py?branch=master)

A Python client for Mapbox web services

## Services

* [Geocoding](https://www.mapbox.com/developers/api/geocoding/)
  * Forward (place names ⇢  longitude, latitude)
  * Reverse (longitude, latitude ⇢ place names)

* Other services coming soon

## Installation

```sh
$ pip install mapbox
```

## API Usage

To begin geocoding, import the mapbox module and create a new `Geocoder` object
with your [Mapbox access token](https://www.mapbox.com/developers/api/#access-tokens).

```python
import mapbox

geocoder = mapbox.Geocoder(access_token='YOUR_ACCESS_TOKEN')
```

`Geocoder`'s methods return [Requests](http://www.python-requests.org/en/latest/)
style response objects.

```python
response = geocoder.forward('Chester, NJ')

# response.json() returns the geocoding result as GeoJSON.
# response.status_code returns the HTTP API status code.

response = geocoder.reverse(lon=-74.7083, lat=40.7851)
```

See `import mapbox; help(mapbox.Geocoder)` for more detailed usage.

## Command Line Interface

The mapbox module includes a CLI program named `mbx`.

```
$ mbx --help
Usage: mbx [OPTIONS] COMMAND [ARGS]...

  This is the command line interface to Mapbox web services.

  Mapbox web services require an access token. Your token is shown on the
  https://www.mapbox.com/developers/api/ page when you are logged in. The
  token can be provided on the command line

    $ mbx --access-token MY_TOKEN ...

  or as an environment variable named MAPBOX_ACCESS_TOKEN or
  MapboxAccessToken.

    $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
    $ mbx ...

Options:
  --access-token TEXT  Your Mapbox access token.
  -v, --verbose        Increase verbosity.
  --version            Show the version and exit.
  -q, --quiet          Decrease verbosity.
  --help               Show this message and exit.

Commands:
  geocode  Geocode an address or coordinates.
```

The `mbx-geocode` command can do forward or reverse geocoding.

```
$ mbx geocode --help
Usage: mbx geocode [OPTIONS] [QUERY]

  This command returns places matching an address (forward mode) or places
  matching coordinates (reverse mode).

  In forward (the default) mode the query argument shall be an address such
  as '1600 pennsylvania ave nw'.

    $ mbx geocode '1600 pennsylvania ave nw'

  In reverse mode the query argument shall be a JSON encoded array of
  longitude and latitude (in that order) in decimal degrees.

    $ mbx geocode --reverse '[-77.4371, 37.5227]'

  An access token is required, see `mbx --help`.

Options:
  --forward / --reverse  Perform a forward or reverse geocode. [default:
                         forward]
  -i, --include          Include HTTP headers in the output.
  --lat FLOAT            Bias results toward this latitude (decimal degrees).
                         --lon is also required.
  --lon FLOAT            Bias results toward this longitude (decimal degrees).
                         --lat is also required.
  -t, --place-type NAME  Restrict results to one or more of these place types:
                         ['address', 'country', 'place', 'poi', 'postcode',
                         'region'].
  -o, --output TEXT      Save output to a file.
  --help                 Show this message and exit.
```

Its output can be piped to [geojsonio](http://geojson.io) using
[geojsonio-cli](https://github.com/mapbox/geojsonio-cli).

```bash
$ mbx geocode 'Chester, NJ' | geojsonio
```

<iframe frameborder="0" width="100%" height="300" src="http://bl.ocks.org/d/dc48d41d21ef054fe865">
</iframe>

## Testing

```bash
pip install -e .[test]
py.test
```

## See Also

https://github.com/mapbox/mapbox-sdk-js
