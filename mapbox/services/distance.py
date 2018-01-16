"""Distance API V1 **DEPRECATED**"""

import warnings

from mapbox.errors import MapboxDeprecationWarning
from mapbox.services.matrix import DirectionsMatrix


class Distance(object):
    """Access to the Distance API V1 ***DEPRECATED**"""

    api_name = 'distance-deprecated'
    api_version = 'v1-deprecated'
    valid_profiles = DirectionsMatrix.valid_profiles + [
        'driving', 'cycling', 'walking']

    def __init__(self, access_token=None, host=None, cache=None):
        warnings.warn(
            "The distance module will be removed in the next version. "
            "Use the matrix module instead.", MapboxDeprecationWarning)
        self.access_token = access_token
        self.host = host
        self.cache = cache

    def distances(self, features, profile='driving'):
        service = DirectionsMatrix(
            access_token=self.access_token, host=self.host, cache=self.cache)
        return service.matrix(features, profile=profile)
