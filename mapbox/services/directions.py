from uritemplate import URITemplate

from mapbox.encoding import encode_waypoints
from mapbox.services.base import Service
from mapbox import errors


class Directions(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/v4/directions'
        self.session = self.get_session(access_token)
        self.valid_profiles = ['mapbox.driving',
                               'mapbox.cycling',
                               'mapbox.walking']
        self.valid_instruction_formats = ['text', 'html']
        self.valid_geom_encoding = ['geojson', 'polyline', 'false']

    def _validate_profile(self, profile):
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
                "{0} is not a valid instruction format".format(instruction_format))
        return instruction_format

    def directions(
            self,
            features,
            profile='mapbox.driving',
            alternatives=None,
            instructions=None,
            geometry=None,
            steps=None):
        """Request directions for waypoints encoded as GeoJSON features."""
        profile = self._validate_profile(profile)
        instructions = self._validate_instruction_format(instructions)
        geometry = self._validate_geom_encoding(geometry)
        waypoints = encode_waypoints(features, precision=6,
                                     min_limit=2, max_limit=30)

        params = {}
        if alternatives is not None:
            params.update(
                {'alternatives': 'true' if alternatives is True else 'false'})
        if instructions is not None:
            params.update({'instructions': instructions})
        if geometry is not None:
            params.update({'geometry': 'false' if geometry is False else geometry})
        if steps is not None:
            params.update(
                {'steps': 'true' if steps is True else 'false'})

        uri = URITemplate('%s/{profile}/{waypoints}.json' % self.baseuri).expand(
            profile=profile, waypoints=waypoints)

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
