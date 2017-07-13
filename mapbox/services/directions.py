import warnings

from uritemplate import URITemplate

from mapbox.encoding import encode_waypoints as encode_coordinates
from mapbox.services.base import Service
from mapbox import errors


class Directions(Service):
    """Access to the Directions v5 API."""

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
        return 'https://{0}/directions/v5'.format(self.host)

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

    def _validate_bearings(self, bearings, features):
        result = []
        if bearings is None:
            return None
        if len(bearings) != len(features):
            raise errors.InvalidParameterError(
                'Must provide exactly one bearing tuple for each input feature')
        for bearing in bearings:
            if bearing is None:
                result.append(None)
            else:
                try:
                    angle, rng = bearing
                except ValueError:
                    raise errors.InvalidParameterError(
                        'bearing tuple must contain two elements: (angle, range)')

                if angle <= 0 or angle >= 360 or rng <= 0 or rng >= 360:
                    raise errors.InvalidParameterError(
                        'angle and range must be between 0 and 360')
                result.append((angle, rng))
        return result

    def _validate_radiuses(self, radiuses, features):
        result = []
        if radiuses is None:
            return None
        if len(radiuses) != len(features):
            raise errors.InvalidParameterError(
                'Must provide exactly one radius for each input feature')
        for radius in radiuses:
            if radius == 'unlimited' or radius > 0:
                result.append(radius)
            else:
                raise errors.InvalidParameterError(
                    '{0} is not a valid radius'.format(radius))
        return result

    @staticmethod
    def _encode_bearing(b):
        if b is None:
            return ''
        else:
            return '{},{}'.format(*b)

    def directions(self, features, profile='mapbox/driving', alternatives=None,
                   geometries=None, overview=None, radiuses=None, steps=None,
                   continue_straight=None, bearings=None, annotations=None,
                   language=None, **kwargs):
        """Request directions for waypoints encoded as GeoJSON features.

        Parameters
        ----------
        features: iterable of GeoJSON-like Feature mappings
        profile: string
        alternatives: boolean
        geometries: string
            Type of geometry returned (geojson, polyline, polyline6)
        overview: string or False
            ('full', 'simplified', False)
        radiuses: iterable of numbers or 'unlimited'
            Must be same length as features
        steps: boolean
        continue_straight: boolean
        bearings: list of bearing 2-tuples
            where the bearing tuple consists of an angle and range
                [(215, 45), (315, 90)]
            Must be same length as features
        annotations: string
        language: string

        Returns
        -------
        requests.Response
            the json() method will return a Directions response dict
        """
        # backwards compatible, deprecated
        if 'geometry' in kwargs and geometries is None:
            geometries = kwargs['geometry']
            warnings.warn('Use `geometries` instead of `geometry`',
                          errors.MapboxDeprecationWarning)

        profile = self._validate_profile(profile)
        geometries = self._validate_geom_encoding(geometries)
        overview = self._validate_geom_overview(overview)
        annotations = self._validate_annotations(annotations)
        radiuses = self._validate_radiuses(radiuses, features)
        bearings = self._validate_bearings(bearings, features)
        coordinates = encode_coordinates(
            features, precision=6, min_limit=2, max_limit=25)

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
        if radiuses is not None:
            params.update(
                {'radiuses': ';'.join(str(r) for r in radiuses)})
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
            return self._geojson(resp.json())
        resp.geojson = geojson
        return resp

    def _geojson(self, data):
        fc = {
            'type': 'FeatureCollection',
            'features': []}

        # TODO make this work for polyline encoded geometry
        # Otherwise the geometry will be invalid GeoJSON
        for route in data['routes']:
            feature = {
                'type': 'Feature',
                'geometry': route['geometry'],
                'properties': {
                    # TODO include RouteLegs and other details
                    'distance': route['distance'],
                    'duration': route['duration']}}
            fc['features'].append(feature)
        return fc
