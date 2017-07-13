import warnings

from uritemplate import URITemplate

from mapbox.encoding import encode_waypoints
from mapbox.services.base import Service
from mapbox import errors


class Directions(Service):
    """Access to the Directions v5 API."""

    valid_profiles = [
        'mapbox/driving',
        'mapbox/driving-traffic',
        'mapbox/walking',
        'mapbox/cycling']
    valid_instruction_formats = ['text', 'html']
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

    def _validate_instruction_format(self, instruction_format):
        if instruction_format is not None and \
           instruction_format not in self.valid_instruction_formats:
            raise errors.InvalidParameterError(
                "{0} is not a valid instruction format".format(
                    instruction_format))
        return instruction_format

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
        overview: string or False
        radiuses: iterable of numbers or 'unlimited'
            Must be same length as features
        steps: boolean
        continue_straight: boolean
        bearings: ?
            final encoding needs to be 'bearing,range' delimited by ;
            Must be same length as features (sequential `;` skips)
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

        if bearings is not None:
            raise NotImplementedError(
                "Haven't decided on the best python data structure for bearings yet")

        profile = self._validate_profile(profile)
        geometries = self._validate_geom_encoding(geometries)
        overview = self._validate_geom_overview(overview)
        annotations = self._validate_annotations(annotations)
        radiuses = self._validate_radiuses(radiuses, features)
        waypoints = encode_waypoints(
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

        profile_ns, profile_name = profile.split('/')

        uri = URITemplate(
            self.baseuri + '/{profile_ns}/{profile_name}/{waypoints}.json').expand(
                profile_ns=profile_ns, profile_name=profile_name, waypoints=waypoints)

        resp = self.session.get(uri, params=params)
        self.handle_http_error(resp)

        def geojson():
            return self._geojson(resp.json())

        if geometries == 'geojson' and overview is not False:
            # TODO make this work for polyline encoded geometry
            resp.geojson = geojson

        return resp

    def _geojson(self, data):
        fc = {
            'type': 'FeatureCollection',
            'features': []}
        for route in data['routes']:
            feature = {
                'type': 'Feature',
                'properties': {
                    # TODO include RouteLegs and other details
                    'distance': route['distance'],
                    'duration': route['duration']}}
            feature['geometry'] = route['geometry']
            fc['features'].append(feature)

        return fc
