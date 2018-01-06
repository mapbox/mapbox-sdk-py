"""Distance API V1 **DEPRECATED**"""

import warnings

from mapbox.services.matrix import DirectionsMatrix


class Distance(object):
    """Access to the Distance API V1 ***DEPRECATED**"""

    def __init__(self, access_token=None, host=None, cache=None):
        warnings.warn(
            "The distance module will be removed in the next version. "
            "Use the matrix module instead.", DeprecationWarning)
        self.access_token = access_token
        self.host = host
        self.cache = cache

    def distances(self, features, profile='driving'):
        service = DirectionsMatrix(
            access_token=self.access_token, host=self.host, cache=self.cache)
        return service.matrix(features, profile=profile)
