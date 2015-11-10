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

- `Geocoding <https://www.mapbox.com/developers/api/geocoding/>`__

  - Forward (place names ⇢ longitude, latitude)
  - Reverse (longitude, latitude ⇢ place names)

- `Upload <https://www.mapbox.com/developers/api/uploads/>`__

  - Upload data to be processed and hosted by Mapbox.

-  Other services coming soon

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


Testing
=======

.. code:: bash

    pip install -e .[test]
    py.test

See Also
========

https://github.com/mapbox/mbx-cli
https://github.com/mapbox/mapbox-sdk-js
