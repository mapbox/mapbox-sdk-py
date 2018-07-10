=====================================================
Mapbox: The Mapbox Platform client library for Python
=====================================================

.. image:: https://travis-ci.org/mapbox/mapbox-sdk-py.png?branch=master
   :target: https://travis-ci.org/mapbox/mapbox-sdk-py

.. image:: https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.png
   :target: https://coveralls.io/r/mapbox/mapbox-sdk-py

A Python client for Mapbox web services

The Mapbox Python SDK is a low-level client API, not a Resource API such as the ones in `boto3 <http://aws.amazon.com/sdk-for-python/>`__ or `github3.py <https://github3py.readthedocs.org/en/master/>`__. Its methods return objects containing `HTTP responses <http://docs.python-requests.org/en/latest/api/#requests.Response>`__ from the Mapbox API.

Services
========

- **Analytics V1** `examples <./analytics.html>`__, `website <https://www.mapbox.com/api-documentation/#analytics>`__

  - API usage for services by resource. 
  - available for premium and enterprise plans.

- **Directions V4** `examples <./directions.html#directions>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#directions>`__

  - Profiles for driving, walking, and cycling
  - GeoJSON & Polyline formatting
  - Instructions as text or HTML

- **Geocoding V5** `examples <./geocoding.html#geocoding>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#geocoding>`__

  - Forward (place names ⇢ longitude, latitude)
  - Reverse (longitude, latitude ⇢ place names)

- **Map Matching V4** `examples <./mapmatching.html#map-matching>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#map-matching>`__

  - Snap GPS traces to OpenStreetMap data

- **Static Maps V4** `examples <./static.html#static-maps>`__, `website <https://www.mapbox.com/api-documentation/pages/static_classic.html>`__

  - Generate standalone images from existing Mapbox *mapids* (tilesets)
  - Render with GeoJSON overlays
  
- **Static Styles V1** `examples <./static.html#static-maps>`__, `website <https://www.mapbox.com/api-documentation/#static>`__

  - Generate standalone images from existing Mapbox *styles*
  - Render with GeoJSON overlays
  - Adjust pitch and bearing, decimal zoom levels
  
- **Surface V4** **DEPRECATED**
- **Uploads V1** `examples <./uploads.html#uploads>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#uploads>`__

  - Upload data to be processed and hosted by Mapbox.

- **Datasets V1** `examples <./datasets.html#datasets>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#datasets>`__

  - Manage editable collections of GeoJSON features
  - Persistent storage for custom geographic data

- **Tilesets V1** `examples <./tilesets.html#tilesets>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#tilesets>`__
  
  - Read metadata for raster and vector tilesets

- **Maps V4** `examples <./maps.html#maps>`__, `website <https://www.mapbox.com/api-documentation/?language=Python#maps>`__

  - Retrieve an image tile, vector tile, or UTFGrid in the specified format
  - Retrieve vector features from Mapbox Editor projects as GeoJSON or KML
  - Retrieve TileJSON metadata for a tileset
  - Retrieve a single marker image without any background map

Please note that there may be some lag between the release of new Mapbox web
services and releases of this package.

Installation
============

.. code:: bash

    $ pip install mapbox

Testing
=======

.. code:: bash

    $ pip install -e .[test]
    $ python -m pytest

To run the examples as integration tests on your own Mapbox account

.. code:: bash

    $ MAPBOX_ACCESS_TOKEN="MY_ACCESS_TOKEN" python -m pytest --doctest-glob='*.md' docs/*.md

See Also
========

* Command line interface: https://github.com/mapbox/mapbox-cli-py
* Javascript SDK: https://github.com/mapbox/mapbox-sdk-js

Documentation
=============

.. toctree::
   :maxdepth: 1

   access_tokens.md
   datasets.md
   geocoding.md
   matrix.md
   directions.md
   input_features.md
   static.md
   uploads.md
   analytics.md
   mapmatching.md
   static_style.md
   tilesets.md
   maps.md
   api/mapbox.rst
   api/mapbox.services.rst
   api/modules.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
