from uritemplate import URITemplate
from mapbox.encoding import encode_coordinates_json
from .base import Service


class Distance(Service):

    def __init__(self, profile='driving', access_token=None):
        self.profile = self._validate_profile(profile)
        self.baseuri = 'https://api.mapbox.com/distances/v1/mapbox'
        self.session = self.get_session(access_token)

    def _validate_profile(self, profile):
        valid_profiles = ['driving', 'cycling', 'walking']
        if profile not in valid_profiles:
            raise ValueError("{} is not a valid profile".format(profile))
        return profile

    def distances(self, features):
        coords = encode_coordinates_json(features)

        uri = URITemplate('%s/{profile}' % self.baseuri).expand(
            profile=self.profile)

        return self.session.post(uri, data=coords,
                                 headers={'Content-Type': 'application/json'})

    def distance_matrix(self, features):
        res = self.distances(features)
        if res.status_code == 200:
            data = res.json()
            return data['durations']
        else:
            raise Exception(res.text)
