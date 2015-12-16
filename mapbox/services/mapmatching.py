import json

from uritemplate import URITemplate

from mapbox.services.base import Service
from mapbox import errors


class MapMatcher(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/matching/v4'
        self.session = self.get_session(access_token)
        self.valid_profiles = ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking']

    def _validate_profile(self, profile):
        if profile not in self.valid_profiles:
            raise errors.InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    def _validate_feature(self, val):
        # validate single feature with linestring geometry up to 100 pts
        try:
            assert val['type'] == 'Feature'
            assert val['geometry']['type'] == 'LineString'
            assert len(val['geometry']['coordinates']) <= 100
        except (TypeError, KeyError, AssertionError):
            raise errors.InvalidFeatureError(
                "Feature must have LineString geometry with <= 100 points")
        return val

    def match(self, feature, gps_precision=None, profile='mapbox.driving'):
        profile = self._validate_profile(profile)

        feature = self._validate_feature(feature)
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
