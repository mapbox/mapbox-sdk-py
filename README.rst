=============
mapbox-sdk-py
=============

.. image:: https://travis-ci.org/mapbox/mapbox-sdk-py.png?branch=master
   :target: https://travis-ci.org/mapbox/mapbox-sdk-py

.. image:: https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.png
   :target: https://coveralls.io/r/mapbox/mapbox-sdk-py

A Python client for Mapbox web services

The Mapbox Python SDK is a low-level client API, not a Resource API such as the ones in `boto3 <http://aws.amazon.com/sdk-for-python/>`__ or `github3.py <https://github3py.readthedocs.org/en/master/>`__. Its methods return objects containing `HTTP responses <http://docs.python-requests.org/en/latest/api/#requests.Response>`__ from the Mapbox API.

Services
========

- **Directions** `examples <./docs/directions.md#directions>`__, `website <https://www.mapbox.com/developers/api/directions/>`__

  - Profiles for driving, walking, and cycling
  - GeoJSON & Polyline formatting
  - Instructions as text or HTML

- **Distance** `examples <./docs/distance.md#distance>`__, `website <https://www.mapbox.com/developers/api/distance/>`__

  - Travel-time tables between up to 100 points
  - Profiles for driving, walking and cycling

- **Geocoding** `examples <./docs/geocoding.md#geocoding>`__, `website <https://www.mapbox.com/developers/api/geocoding/>`__

  - Forward (place names ⇢ longitude, latitude)
  - Reverse (longitude, latitude ⇢ place names)

- **Map Matching** `examples <./docs/mapmatching.md#map-matching>`__, `website <https://www.mapbox.com/developers/api/map-matching/>`__

  - Snap GPS traces to OpenStreetMap data

- **Static Maps** `examples <./docs/static.md#static-maps>`__, `website <https://www.mapbox.com/developers/api/static/>`__

  - Generate standalone images from existing Mapbox mapids
  - Render with GeoJSON overlays

- **Surface** `examples <./docs/surface.md#surface>`__, `website <https://www.mapbox.com/developers/api/surface/>`__

  - Interpolates values along lines. Useful for elevation traces.

- **Uploads** `examples <./docs/uploads.md#uploads>`__, `website <https://www.mapbox.com/developers/api/uploads/>`__

  - Upload data to be processed and hosted by Mapbox.

- **Datasets** `examples <./docs/datasets.md#datasets>`__

  - Manage editable collections of GeoJSON features
  - Persistent storage for custom geographic data

Other services coming soon.

Installation
============

.. code:: bash

    $ pip install mapbox

Testing
=======

.. code:: bash

    pip install -e .[test]
    py.test

To run the examples as integration tests on your own Mapbox account

.. code:: bash

    MAPBOX_ACCESS_TOKEN="MY_ACCESS_TOKEN" py.test --doctest-glob='*.md' docs/*.md

See Also
========

* Command line interface: https://github.com/mapbox/mapbox-cli-py
* Javascript SDK: https://github.com/mapbox/mapbox-sdk-js
