from uritemplate import URITemplate
from mapbox.encoding import encode_waypoints
from .base import Service


class Directions(Service):

    def __init__(self, profile='mapbox.driving', access_token=None):
        self.profile = self._validate_profile(profile)
        self.baseuri = 'https://api.mapbox.com/v4/directions'
        self.session = self.get_session(access_token)

    def _validate_profile(self, profile):
        valid_profiles = ['mapbox.driving', 'mapbox.cycling', 'mapbox.walking']
        if profile not in valid_profiles:
            raise ValueError("{} is not a valid profile".format(profile))
        return profile

    def route(self,
              features,
              alternatives=None,
              instructions=None,
              geometry=None,
              steps=None):

        waypoints = encode_waypoints(features, precision=6,
                                     min_limit=2, max_limit=30)

        # TODO add optional args as url params
        uri = URITemplate('%s/{profile}/{waypoints}.json' % self.baseuri).expand(
            profile=self.profile, waypoints=waypoints)

        resp = self.session.get(uri)
        resp.raise_for_status()

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
