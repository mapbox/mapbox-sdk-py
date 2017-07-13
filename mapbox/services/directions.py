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
    valid_geom_encoding = ['geojson', 'polyline', 'false']

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

    def _validate_geom_encoding(self, geom_encoding):
        if geom_encoding is not None and \
           geom_encoding not in self.valid_geom_encoding:
            raise errors.InvalidParameterError(
                "{0} is not a valid geometry encoding".format(geom_encoding))
        return geom_encoding

    def _validate_instruction_format(self, instruction_format):
        if instruction_format is not None and \
           instruction_format not in self.valid_instruction_formats:
            raise errors.InvalidParameterError(
                "{0} is not a valid instruction format".format(
                    instruction_format))
        return instruction_format

    def directions(self, features, profile='mapbox/driving', alternatives=None,
                   instructions=None, geometries=None, steps=None, **kwargs):
        """Request directions for waypoints encoded as GeoJSON features.

        :param features: sequence of GeoJSON features.
        :param profile: name of a profile.
        """
        # backwards compatible, deprecated
        if 'geometry' in kwargs and geometries is None:
            geometries = kwargs['geometry']
            warnings.warn('Use `geometries` instead of `geometry`',
                          errors.MapboxDeprecationWarning)

        profile = self._validate_profile(profile)
        instructions = self._validate_instruction_format(instructions)
        geometries = self._validate_geom_encoding(geometries)
        waypoints = encode_waypoints(
            features, precision=6, min_limit=2, max_limit=30)

        params = {}
        if alternatives is not None:
            params.update(
                {'alternatives': 'true' if alternatives is True else 'false'})
        if instructions is not None:
            params.update({'instructions': instructions})
        if geometries is not None:
            params.update(
                {'geometries': 'false' if geometries is False else geometries})
        if steps is not None:
            params.update(
                {'steps': 'true' if steps is True else 'false'})

        profile_ns, profile_name = profile.split('/')

        uri = URITemplate(
            self.baseuri + '/{profile_ns}/{profile_name}/{waypoints}.json').expand(
                profile_ns=profile_ns, profile_name=profile_name, waypoints=waypoints)

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

        for route in data['routes']:

            feature = {
                'type': 'Feature',
                'properties': {
                    # TODO handle these nested structures
                    # Flatten or ???
                    # 'destination': data['destination'],
                    # 'origin': data['origin'],
                    # 'waypoints': data['waypoints'],
                    # 'steps': route['steps']
                    'distance': route['distance'],
                    'duration': route['duration'],
                    'summary': route['summary']}}

            feature['geometry'] = route['geometry']
            fc['features'].append(feature)

        return fc
