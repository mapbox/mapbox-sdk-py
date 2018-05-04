import warnings

from uritemplate import URITemplate

from mapbox.encoding import encode_waypoints, encode_polyline
from mapbox.errors import MapboxDeprecationWarning
from mapbox.services.base import Service


class Surface(Service):
    """Access to the Surface API V4 **DEPRECATED**"""

    api_name = 'surface'
    api_version = 'v4'

    @property
    def baseuri(self):
        return 'https://{0}/{2}/{1}'.format(
            self.host, self.api_name, self.api_version)

    def surface(self,
                features,
                mapid="mapbox.mapbox-terrain-v1",
                layer="contour",
                fields=["ele"],
                geojson=True,
                polyline=False,
                interpolate=None,
                zoom=None):

        warnings.warn(
            "The surface module will be removed in the next version. "
            "It has no replacement.", MapboxDeprecationWarning)

        params = {
            'layer': layer,
            'fields': ','.join(fields),
            'geojson': 'true' if geojson else 'false',
        }

        if interpolate is not None:
            params['interpolate'] = 'true' if interpolate else 'false',

        if zoom is not None:
            params['zoom'] = zoom

        if polyline:
            params['encoded_polyline'] = encode_polyline(features)
        else:
            params['points'] = encode_waypoints(
                features, precision=6, min_limit=1, max_limit=300)

        uri = URITemplate(self.baseuri + '/{mapid}.json').expand(mapid=mapid)
        res = self.session.get(uri, params=params)
        self.handle_http_error(res)

        def geojson():
            return res.json()['results']
        res.geojson = geojson

        return res
