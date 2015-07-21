mapbox.py
=========
.. image:: https://travis-ci.org/mapbox/mapbox-sdk-py.svg
    :target: https://travis-ci.org/mapbox/mapbox-sdk-py
.. image:: https://coveralls.io/repos/mapbox/mapbox-sdk-py/badge.svg?branch=setup-module&service=github
  :target: https://coveralls.io/github/mapbox/mapbox-sdk-py?branch=setup-module

usage - surface api
-----

::

    import mapbox


    access_token = '{your mapbox access token}'

    with mapbox.Mapbox(access_token) as mbx:
        surface_response = mbx.surface('{username.mapid}',
            [
                [lng, lat],
                ...
            ],
            layer='{name of layer to query}',
            fields=[])

        surface_response.json()

