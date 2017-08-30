from uritemplate import URITemplate

from mapbox.encoding import encode_coordinates_json
from mapbox.errors import InvalidProfileError
from mapbox.services.base import Service


class Distance(Service):
    """Access to the Distance API V1"""

    api_name = 'distances'
    api_version = 'v1'

    valid_profiles = ['driving', 'cycling', 'walking']

    @property
    def baseuri(self):
        return 'https://{0}/{1}/{2}/mapbox'.format(
            self.host, self.api_name, self.api_version)

    def _validate_profile(self, profile):
        if profile not in self.valid_profiles:
            raise InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    def distances(self, features, profile='driving'):
        profile = self._validate_profile(profile)
        coords = encode_coordinates_json(features)
        uri = URITemplate(self.baseuri + '/{profile}').expand(profile=profile)
        res = self.session.post(uri, data=coords,
                                headers={'Content-Type': 'application/json'})
        self.handle_http_error(res)
        return res
