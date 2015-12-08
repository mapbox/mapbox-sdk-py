from uritemplate import URITemplate
from mapbox.encoding import encode_waypoints, encode_polyline
from .base import Service


class Surface(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/v4/surface'
        self.session = self.get_session(access_token)

    def surface(self,
                features,
                mapid="mapbox.mapbox-terrain-v1",
                layer="contour",
                fields=["ele"],
                geojson=True,
                polyline=False,
                interpolate=None,
                zoom=None):

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

        uri = URITemplate('%s/{mapid}.json' % self.baseuri).expand(mapid=mapid)
        res = self.session.get(uri, params=params)
        self.handle_http_error(res)

        def geojson():
            return res.json()['results']
        res.geojson = geojson

        return res
