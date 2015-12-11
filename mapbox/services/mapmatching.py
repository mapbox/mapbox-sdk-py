import json

from uritemplate import URITemplate

from mapbox.services.base import Service


class MapMatcher(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/matching/v4'
        self.session = self.get_session(access_token)

    def _validate_profile(self, profile):
        valid_profiles = ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking']
        if profile not in valid_profiles:
            raise ValueError("{} is not a valid profile".format(profile))
        return profile

    def match(self, feature, gps_precision=None, profile='mapbox.driving'):
        profile = self._validate_profile(profile)

        # validate single feature with linestring geometry up to 100 pts
        try:
            assert feature['type'] == 'Feature'
            assert feature['geometry']['type'] == 'LineString'
            assert len(feature['geometry']['coordinates']) <= 100
        except (TypeError, KeyError, AssertionError):
            raise ValueError("feature must have LineString geometry "
                             "with <= 100 points")

        geojson_line_feature = json.dumps(feature)

        uri = URITemplate('%s/{profile}.json' % self.baseuri).expand(
            profile=profile)

        params = None
        if gps_precision:
            params = {'gps_precision': gps_precision}

        res = self.session.post(uri, data=geojson_line_feature, params=params,
                                headers={'Content-Type': 'application/json'})
        self.handle_http_error(res)

        def geojson():
            return res.json()

        res.geojson = geojson

        return res
