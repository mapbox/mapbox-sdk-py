## mapbox.py
from __future__ import with_statement
import requests

class Mapbox:
    def __init__(self, access_token):
        self.access_token = access_token
    def __enter__(self):
        return self
    def __exit__(self, ext_t, ext_v, trace):
        if ext_t:
            click.echo("in __exit__")
    def exists(self):
        return "Mapbox exits with access token %s" % (self.access_token,)