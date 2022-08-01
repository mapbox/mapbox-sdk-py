# mapbox-sdk-py

A Python client for Mapbox web services. The Mapbox Python SDK is a low-level client API, not a Resource API such as the ones in [](http://aws.amazon.com/sdk-for-python). Its methods return objects containing [HTTP responses](http://docs.python-requests.org/en/latest/api/#requests.Response) from the Mapbox API.

## Services

- **Analytics V1** [examples](./docs/analytics.md), [website](https://www.mapbox.com/api-documentation/accounts/#analytics)

  - API usage for services by resource.
  - available for premium and enterprise plans.

- **Directions V5** [examples](./docs/directions.md), [website](https://www.mapbox.com/api-documentation/navigation/#directions)

  - Profiles for driving, walking, and cycling
  - GeoJSON & Polyline formatting

- **Distance V1** **DEPRECATED**
- **Geocoding V5** [examples](./docs/geocoding.md), [website](https://www.mapbox.com/api-documentation/search/#geocoding)

  - Forward (place names ⇢ longitude, latitude)
  - Reverse (longitude, latitude ⇢ place names)

- **Map Matching V4** [examples](./docs/mapmatching.md), [website](https://www.mapbox.com/api-documentation/navigation/#map-matching)

  - Snap GPS traces to OpenStreetMap data

- **Static Maps V4** [examples](./docs/static.md), [website](https://www.mapbox.com/api-documentation/legacy/static-classic)

  - Generate standalone images from existing Mapbox *mapids* (tilesets)
  - Render with GeoJSON overlays

- **Static Styles V1** [examples](./docs/static.md), [website](https://www.mapbox.com/api-documentation/maps/#static)

  - Generate standalone images from existing Mapbox *styles*
  - Render with GeoJSON overlays
  - Adjust pitch and bearing, decimal zoom levels

- **Surface V4** [examples](./docs/surface.md), [website](https://www.mapbox.com/developers/api/surface/)

  - Interpolates values along lines. Useful for elevation traces.

- **Uploads V1** [examples](./docs/uploads.md), [website](https://www.mapbox.com/api-documentation/maps/#uploads)

  - Upload data to be processed and hosted by Mapbox.

- **Datasets V1** [examples](./docs/datasets.md), [website](https://www.mapbox.com/api-documentation/maps/#datasets)

  - Manage editable collections of GeoJSON features
  - Persistent storage for custom geographic data

- **Tilequery V4** [examples](./docs/tilequery.md), [website](https://www.mapbox.com/api-documentation/maps/#tilequery)

  - Retrieve data about specific features from a vector tileset

- **Maps V4** [examples](./docs/maps.md), [website](https://www.mapbox.com/api-documentation/maps/#maps)

  - Retrieve an image tile, vector tile, or UTFGrid in the specified format
  - Retrieve vector features from Mapbox Editor projects as GeoJSON or KML
  - Retrieve TileJSON metadata for a tileset
  - Retrieve a single marker image without any background map

Please note that there may be some lag between the release of new Mapbox web
services and releases of this package.

## Documentation

Please see https://mapbox-mapbox.readthedocs-hosted.com/en/latest/

## Installation

```bash
$ pip install mapbox
```

## Testing

```bash
pip install -e ".[test]"
python -m pytest
```

To run the examples as integration tests on your own Mapbox account

```bash
MAPBOX_ACCESS_TOKEN="MY_ACCESS_TOKEN" python -m pytest --doctest-glob='*.md' docs/*.md
```

## See Also

* Mapbox API Documentation: https://www.mapbox.com/api-documentation/
* Javascript SDK: https://github.com/mapbox/mapbox-sdk-js
* Mapbox API command line interface: https://github.com/mapbox/mapbox-cli-py
