"""Matrix API V1"""

import re
import warnings

from mapbox.encoding import encode_waypoints
from mapbox.errors import InvalidProfileError, MapboxDeprecationWarning
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
        # Support for Distance v1 and Directions v4 profiles
        profiles_map = {
            'mapbox.driving': 'mapbox/driving',
            'mapbox.cycling': 'mapbox/cycling',
            'mapbox.walking': 'mapbox/walking',
            'driving': 'mapbox/driving',
            'cycling': 'mapbox/cycling',
            'walking': 'mapbox/walking'}
        if profile in profiles_map:
            profile = profiles_map[profile]
            warnings.warn("Converting deprecated profile, use {} instead".format(profile),
                          MapboxDeprecationWarning)
        if profile not in self.valid_profiles:
            raise InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    def _make_query(self, srcindexes, dstindexes):
        params = {}
        if srcindexes is not None and isinstance(srcindexes, list):
            params['sources'] = ';'.join([str(idx) for idx in srcindexes])
        if dstindexes is not None and isinstance(dstindexes, list):
            params['destinations'] = ';'.join([str(idx) for idx in dstindexes])
        return params

    def matrix(self, coordinates, profile='mapbox/driving',
               sources=None, destinations=None):
        """Request a directions matrix for trips between coordinates

        In the default case, the matrix returns a symmetric matrix,
        using all input coordinates as sources and destinations. You may
        also generate an asymmetric matrix, with only some coordinates
        as sources or destinations:

        Parameters
        ----------
        coordinates : sequence
            A sequence of coordinates, which may be represented as
            GeoJSON features, GeoJSON geometries, or (longitude,
            latitude) pairs.
        profile : str
            The trip travel mode. Valid modes are listed in the class's
            valid_profiles attribute.
        sources : list
            Indices of source coordinates to include in the matrix.
            Default is all coordinates.
        destinations : list
            Indices of destination coordinates to include in the
            matrix. Default is all coordinates.

        Returns
        -------
        requests.Response

        Note: the directions matrix itself is obtained by calling the
        response's json() method. The resulting mapping has 4 items.

        code : str
            Status of the response
        durations : list
            An array of arrays representing the matrix in row-major
            order.  durations[i][j] gives the travel time from the i-th
            source to the j-th destination. All values are in seconds.
            The duration between the same coordinate is always 0. If
            a duration can not be found, the result is null.
        destinations : list
            Results of snapping selected coordinates to the nearest
            addresses.
        destinations : list
            Results of snapping selected coordinates to the nearest
            addresses.
        """
        profile = self._validate_profile(profile)
        coords = encode_waypoints(coordinates)
        query = self._make_query(sources, destinations)
        uri = '{0}/{1}/{2}'.format(self.baseuri, profile, coords)
        res = self.session.get(uri, params=query)
        self.handle_http_error(res)
        return res
