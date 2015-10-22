from uritemplate import URITemplate
from mapbox.encoding import encode_waypoints, encode_polyline
from .base import Service


class Surface(Service):

    def __init__(self, profile='mapbox.driving', access_token=None):
        self.profile = self._validate_profile(profile)
        self.baseuri = 'https://api.mapbox.com/v4/surface'
        self.session = self.get_session(access_token)

    def _validate_profile(self, profile):
        valid_profiles = ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking']
        if profile not in valid_profiles:
            raise ValueError("{} is not a valid profile".format(profile))
        return profile

    def surface(self,
                features,
                mapid="mapbox.mapbox-terrain-v1",
                layer="contour",
                fields=["ele"],
                geojson=False):

        waypoints = encode_waypoints(features, precision=6,
                                     min_limit=2, max_limit=300)

        # TODO other params
        params = {
            'layer': layer,
            'fields': ','.join(fields),
            'geojson': geojson,  # 'true' if geojson else 'fasle'
            'point': waypoints}

        uri = URITemplate('%s/{mapid}.json' % self.baseuri).expand(mapid=mapid)
        return self.session.get(uri, params=params)

    def surface_geojson(self, *args, **kwargs):
        kwargs['geojson'] = True
        res = self.surface(*args, **kwargs)
        if res.status_code == 200:
            data = res.json()
            fc = data['results']
            return fc
        else:
            raise Exception(res.text)
