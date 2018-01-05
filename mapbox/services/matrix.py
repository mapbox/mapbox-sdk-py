"""Matrix API V1"""

import re

from mapbox.encoding import encode_waypoints
from mapbox.errors import InvalidProfileError
from mapbox.services.base import Service


class DirectionsMatrix(Service):
    """Access to the Matrix API V1"""

    api_name = 'directions-matrix'
    api_version = 'v1'

    valid_profiles = [
        'mapbox/driving', 'mapbox/cycling', 'mapbox/walking',
        'mapbox/driving-traffic']

    @property
    def baseuri(self):
        return 'https://{0}/{1}/{2}'.format(
            self.host, self.api_name, self.api_version)

    def _validate_profile(self, profile):
        parts = re.split(r'[\/\.]', profile)
        if len(parts) == 1:
            parts = ['mapbox'] + parts
        profile = '/'.join(parts)
        if profile not in self.valid_profiles:
            raise InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    def matrix(self, features, profile='mapbox/driving'):
        profile = self._validate_profile(profile)
        coords = encode_waypoints(features)
        uri = '{0}/{1}/{2}'.format(self.baseuri, profile, coords)
        res = self.session.get(uri)
        self.handle_http_error(res)
        return res
