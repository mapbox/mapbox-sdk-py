=============
mapbox-sdk-py
=============

.. image:: https://travis-ci.org/mapbox/mapbox-sdk-py.png
   :target: https://travis-ci.org/mapbox/mapbox-sdk-py

.. image:: https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.png
   :target: https://coveralls.io/r/mapbox/mapbox-sdk-py

A Python client for Mapbox web services

The Mapbox Python SDK is a low-level client API, not a Resource API such as the ones in `boto3 <http://aws.amazon.com/sdk-for-python/>`__ or `github3.py <https://github3py.readthedocs.org/en/master/>`__. Its methods return objects containing `HTTP responses <http://docs.python-requests.org/en/latest/api/#requests.Response>`__ from the Mapbox API.

Services
========

Generally Available

- `Geocoding <https://www.mapbox.com/developers/api/geocoding/>`__

  - Forward (place names ⇢ longitude, latitude)
  - Reverse (longitude, latitude ⇢ place names)

- `Uploads <https://www.mapbox.com/developers/api/uploads/>`__

  - Upload data to be processed and hosted by Mapbox.

- `Directions <https://www.mapbox.com/developers/api/directions/>`__

  - Profiles for driving, walking, and cycling
  - GeoJSON & Polyline formatting
  - Instructions as text or HTML

Contact help@mapbox.com for information

- `Distance <https://www.mapbox.com/developers/api/distance/>`__

  - Travel-time tables between up to 100 points
  - Profiles for driving, walking and cycling

- `Surface <https://www.mapbox.com/developers/api/surface/>`__

  - Interpolates values along lines. Useful for elevation traces.

Other services coming soon


Installation
============

.. code:: bash

    $ pip install mapbox


API Usage
=========

Geocoder
--------

To begin geocoding, import the mapbox module and create a new
``Geocoder`` object with your `Mapbox access token 
<https://www.mapbox.com/developers/api/#access-tokens>`__.

.. code:: python

    import mapbox

    geocoder = mapbox.Geocoder(access_token='YOUR_ACCESS_TOKEN')


``Geocoder``'s methods return `Requests <http://www.python-requests.org/en/latest/>`__ style response objects.

.. code:: python

    response = geocoder.forward('Chester, NJ')

    # response.json() returns the geocoding result as GeoJSON.
    # response.status_code returns the HTTP API status code.

    response = geocoder.reverse(lon=-74.7083, lat=40.7851)

See ``import mapbox; help(mapbox.Geocoder)`` for more detailed usage.


Upload
------
To upload data, you must created a token with ``uploads:*`` scopes at https://www.mapbox.com/account/apps/.
Then upload any supported file to your account using the ``Uploader`` 

.. code:: python
    
    from mapbox import Uploader
    conxn = Uploader('username', access_token='MY_TOKEN')
    resp = conxn.upload('RGB.byte.tif', 'RGB-byte-tif')
    upload_id = resp.json()['id']

    resp = conxn.status(upload_id).json()
    resp['complete']  # True
    resp['tileset']   # "username.RGB-byte-tif"

See ``import mapbox; help(mapbox.Uploader)`` for more detailed usage.


Directions
----------
To get travel directions between waypoints, you can use the Directions API to route up to 25 points.
Each of your input waypoints will be visited in order and should be 
represented by a GeoJSON point feature.

.. code:: python
    
    from mapbox import Directions
    resp = Directions('mapbox.driving').directions([origin, destination])
    driving_routes = resp.geojson()
    first_route = driving_routes['features'][0]

See ``import mapbox; help(mapbox.Directions)`` for more detailed usage.


Distance
--------
If you need to optimize travel between several waypoints, you can use the Distance API to
create a "Distance Matrix" showing travel times between all waypoints.
Each of your input waypoints should be a GeoJSON point feature.

.. code:: python
    
    from mapbox import Distance
    resp = Distance('mapbox.driving').distance(points['features'])
    resp.json()

which returns::

    {
      "durations": [
        [ 0,    2910, null ],
        [ 2903, 0,    5839 ],
        [ 4695, 5745, 0    ]
      ]
    }
    
See ``import mapbox; help(mapbox.Distance)`` for more detailed usage.


Surface
-------
To query vector tile attributes along a series of points or a line, you can use the Surface API.
For example, you could create an elevation profile against a GeoJSON LineString feature

.. code:: python

    from mapbox import Surface
    Surface().surface([route], mapid='mapbox.mapbox-terrain-v1',
                      layer='contour', fields=['ele'])
    profile_pts = resp.geojson()

See ``import mapbox; help(mapbox.Surface)`` for more detailed usage.


Testing
=======

.. code:: bash

    pip install -e .[test]
    py.test

See Also
========

* Command line interface: https://github.com/mapbox/mapbox-cli-py
* Javascript SDK: https://github.com/mapbox/mapbox-sdk-js
