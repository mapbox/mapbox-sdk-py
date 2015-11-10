from uritemplate import URITemplate

from mapbox.services.base import Service
from mapbox.encoding import encode_waypoints


class Directions(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/v4/directions'
        self.session = self.get_session(access_token)

    def _validate_profile(self, profile):
        valid_profiles = ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking']
        if profile not in valid_profiles:
            raise ValueError("{} is not a valid profile".format(profile))
        return profile

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
