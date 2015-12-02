import json

from uritemplate import URITemplate

from mapbox.services.base import Service


class Static(Service):

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/v4'
        self.session = self.get_session(access_token)

    def image(self, mapid, lon=None, lat=None, z=None, features=None,
              width=600, height=600, image_format='png256'):

        if lon and lat and z:
            auto = False
        else:
            auto = True

        values = dict(
            mapid=mapid,
            lon=str(lon),
            lat=str(lat),
            z=str(z),
            width=str(width),
            height=str(height),
            format=image_format)

        if features:
            values['overlay'] = json.dumps({'type': 'FeatureCollection',
                                            'features': features})

            if len(values['overlay']) > 4087:  # limit is 4096 minus the 'geojson()'
                raise ValueError("geojson is too large for the static maps API, "
                                 "must be less than 4096 characters")

            if auto:
                uri = URITemplate(
                    '%s/{mapid}/geojson({overlay})/auto/{width}x{height}.{format}' %
                    self.baseuri).expand(**values)
            else:
                uri = URITemplate(
                    '%s/{mapid}/geojson({overlay})/{lon},{lat},{z}/{width}x{height}.{format}' %
                    self.baseuri).expand(**values)
        else:
            if auto:
                raise ValueError("Must provide features if lat, lon, z are None")

            # No overlay
            uri = URITemplate(
                '%s/{mapid}/{lon},{lat},{z}/{width}x{height}.{format}' %
                self.baseuri).expand(**values)

        res = self.session.get(uri)
        self.handle_http_error(res)
        return res
