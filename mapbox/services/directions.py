import warnings
from numbers import Number

import polyline
from uritemplate import URITemplate

from mapbox.encoding import encode_waypoints as encode_coordinates
from mapbox.services.base import Service
from mapbox import errors


class Directions(Service):
    """Access to the Directions v5 API."""

    api_name = 'directions'
    api_version = 'v5'

    valid_profiles = [
        'mapbox/driving',
        'mapbox/driving-traffic',
        'mapbox/walking',
        'mapbox/cycling']
    valid_geom_encoding = ['geojson', 'polyline', 'polyline6']
    valid_geom_overview = ['full', 'simplified', False]
    valid_annotations = ['duration', 'distance', 'speed']

    @property
    def baseuri(self):
        return 'https://{0}/{1}/{2}'.format(
            self.host, self.api_name, self.api_version)

    def _validate_profile(self, profile):
        # Backwards compatible with v4 profiles
        v4_to_v5_profiles = {
            'mapbox.driving': 'mapbox/driving',
            'mapbox.cycling': 'mapbox/cycling',
            'mapbox.walking': 'mapbox/walking'}
        if profile in v4_to_v5_profiles:
            profile = v4_to_v5_profiles[profile]
            warnings.warn('Converting v4 profile to v5, use {} instead'.format(profile),
                          errors.MapboxDeprecationWarning)
        if profile not in self.valid_profiles:
            raise errors.InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    def _validate_annotations(self, annotations):
        results = []
        if annotations is None:
            return None
        for annotation in annotations:
            if annotation not in self.valid_annotations:
                raise errors.InvalidParameterError(
                    "{0} is not a valid annotation".format(annotation))
            else:
                results.append(annotation)
        return results

    def _validate_geom_encoding(self, geom_encoding):
        if geom_encoding is not None and \
           geom_encoding not in self.valid_geom_encoding:
            raise errors.InvalidParameterError(
                "{0} is not a valid geometry format".format(geom_encoding))
        return geom_encoding

    def _validate_geom_overview(self, overview):
        if overview is not None and overview not in self.valid_geom_overview:
            raise errors.InvalidParameterError(
                "{0} is not a valid geometry overview type".format(overview))
        return overview

    def _validate_snapping(self, snaps, features):
        bearings = []
        radii = []
        if snaps is None:
            return (None, None)
        if len(snaps) != len(features):
            raise errors.InvalidParameterError(
                'Must provide exactly one snapping element for each input feature')
        for snap in snaps:
            if snap is None:
                bearings.append(None)
                radii.append(None)
            else:
                try:
                    # radius-only
                    radius = self._validate_radius(snap)
                    bearing = None
                except errors.InvalidParameterError:
                    # (radius, angle, range) tuple
                    try:
                        radius, angle, rng = snap
                    except ValueError:
                        raise errors.InvalidParameterError(
                            'waypoint snapping should contain 3 elements: '
                            '(bearing, angle, range)')
                    self._validate_radius(radius)

                    try:
                        assert angle >= 0
                        assert angle <= 360
                        assert rng >= 0
                        assert rng <= 360
                    except (TypeError, AssertionError):
                        raise errors.InvalidParameterError(
                            'angle and range must be between 0 and 360')
                    bearing = (angle, rng)

                bearings.append(bearing)
                radii.append(radius)

        if all([b is None for b in bearings]):
            bearings = None

        return (bearings, radii)

    def _validate_radius(self, radius):
        if radius is None:
            return None

        if isinstance(radius, str):
            if radius != 'unlimited':
                raise errors.InvalidParameterError(
                    '{0} is not a valid radius'.format(radius))
        elif isinstance(radius, Number):
            if radius <= 0:
                raise errors.InvalidParameterError(
                    'radius must be greater than zero'.format(radius))
        else:
            raise errors.InvalidParameterError(
                '{0} is not a valid radius'.format(radius))

        return radius

    @staticmethod
    def _encode_bearing(b):
        if b is None:
            return ''
        else:
            return '{},{}'.format(*b)

    def directions(self, features, profile='mapbox/driving',
                   alternatives=None, geometries=None, overview=None, steps=None,
                   continue_straight=None, waypoint_snapping=None, annotations=None,
                   language=None, **kwargs):
        """Request directions for waypoints encoded as GeoJSON features.

        Parameters
        ----------
        features : iterable
            An collection of GeoJSON features
        profile : str
            Name of a Mapbox profile such as 'mapbox.driving'
        alternatives : bool
            Whether to try to return alternative routes, default: False
        geometries : string
            Type of geometry returned (geojson, polyline, polyline6)
        overview : string or False
            Type of returned overview geometry: 'full', 'simplified',
            or False
        steps : bool
            Whether to return steps and turn-by-turn instructions,
            default: False
        continue_straight : bool
            Direction of travel when departing intermediate waypoints
        radiuses : iterable of numbers or 'unlimited'
            Must be same length as features
        waypoint_snapping : list
            Controls snapping of waypoints

            The list is zipped with the features collection and must
            have the same length. Elements of the list must be one of:

            - A number (interpretted as a snapping radius)
            - The string 'unlimited' (unlimited snapping radius)
            - A 3-element tuple consisting of (radius, angle, range)
            - None (no snapping parameters specified for that waypoint)
        annotations : str
            Whether or not to return additional metadata along the route

            Possible values are: 'duration', 'distance', 'speed', and
            'congestion'. Several annotations can be used by joining
            them with ','.
        language : str
            Language of returned turn-by-turn text instructions,
            default: 'en'

        Returns
        -------
        requests.Response
            The response object has a geojson() method for access to
            the route(s) as a GeoJSON-like FeatureCollection
            dictionary.
        """
        # backwards compatible, deprecated
        if 'geometry' in kwargs and geometries is None:
            geometries = kwargs['geometry']
            warnings.warn('Use `geometries` instead of `geometry`',
                          errors.MapboxDeprecationWarning)

        annotations = self._validate_annotations(annotations)
        coordinates = encode_coordinates(
            features, precision=6, min_limit=2, max_limit=25)
        geometries = self._validate_geom_encoding(geometries)
        overview = self._validate_geom_overview(overview)
        profile = self._validate_profile(profile)

        bearings, radii = self._validate_snapping(waypoint_snapping, features)

        params = {}
        if alternatives is not None:
            params.update(
                {'alternatives': 'true' if alternatives is True else 'false'})
        if geometries is not None:
            params.update({'geometries': geometries})
        if overview is not None:
            params.update(
                {'overview': 'false' if overview is False else overview})
        if steps is not None:
            params.update(
                {'steps': 'true' if steps is True else 'false'})
        if continue_straight is not None:
            params.update(
                {'continue_straight': 'true' if steps is True else 'false'})
        if annotations is not None:
            params.update({'annotations': ','.join(annotations)})
        if language is not None:
            params.update({'language': language})
        if radii is not None:
            params.update(
                {'radiuses': ';'.join(str(r) for r in radii)})
        if bearings is not None:
            params.update(
                {'bearings': ';'.join(self._encode_bearing(b) for b in bearings)})

        profile_ns, profile_name = profile.split('/')

        uri = URITemplate(
            self.baseuri + '/{profile_ns}/{profile_name}/{coordinates}.json').expand(
                profile_ns=profile_ns, profile_name=profile_name, coordinates=coordinates)

        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        def geojson():
            return self._geojson(resp.json(), geom_format=geometries)
        resp.geojson = geojson
        return resp

    def _geojson(self, data, geom_format=None):
        fc = {
            'type': 'FeatureCollection',
            'features': []}

        for route in data['routes']:
            if geom_format == 'geojson':
                geom = route['geometry']
            else:
                # convert default polyline encoded geometry
                geom = {
                    'type': 'LineString',
                    'coodinates': polyline.decode(route['geometry'])}

            feature = {
                'type': 'Feature',
                'geometry': geom,
                'properties': {
                    # TODO include RouteLegs and other details
                    'distance': route['distance'],
                    'duration': route['duration']}}
            fc['features'].append(feature)
        return fc
