## mapbox.py
from __future__ import with_statement
import click
from mapbox.scripts import surface_query

class Mapbox:
    def __init__(self, access_token):
        self.access_token = access_token

    def __enter__(self):
        return self

    def __exit__(self, ext_t, ext_v, trace):
        if ext_t:
            click.echo("in __exit__", err=True)

    def exists(self):
        return "Mapbox exists with access token %s" % (self.access_token,)

    def surface(self, mapid, points, **kwargs):
        return surface_query.surface(mapid, points, self.access_token, **kwargs)