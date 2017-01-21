import json

from uritemplate import URITemplate

from mapbox import errors
from mapbox.services.base import Service
from mapbox.utils import normalize_geojson_featurecollection


class Static(Service):
    """Access to the Static Map API."""

    @property
    def baseuri(self):
        return 'https://{0}/v4'.format(self.host)

    def _validate_lat(self, val):
        if val < -85.0511 or val > 85.0511:
            raise errors.InvalidCoordError(
                "Latitude must be between -85.0511 and 85.0511")
        return val

    def _validate_lon(self, val):
        if val < -180 or val > 180:
            raise errors.InvalidCoordError(
                "Longitude must be between -180 and 180")
        return val

    def _validate_image_size(self, val):
        if not (1 < val < 1280):
            raise errors.ImageSizeError(
                "Image height and width must be between 1 and 1280")
        return val

    def _validate_overlay(self, val):
        if len(val) > 4087:  # limit is 4096 minus the 'geojson()'
            raise errors.InputSizeError(
                "GeoJSON is too large for the static maps API, "
                "must be less than 4096 characters")
        return val

    def image(self, mapid, lon=None, lat=None, z=None, features=None,
              width=600, height=600, image_format='png256', sort_keys=False):

        if lon is not None and lat is not None and z is not None:
            auto = False
            lat = self._validate_lat(lat)
            lon = self._validate_lon(lon)
        else:
            auto = True

        width = self._validate_image_size(width)
        height = self._validate_image_size(height)

        values = dict(
            mapid=mapid,
            lon=str(lon),
            lat=str(lat),
            z=str(z),
            width=str(width),
            height=str(height),
            fmt=image_format)

        if features:
            collection = normalize_geojson_featurecollection(features)
            values['overlay'] = json.dumps(
                collection, separators=(',', ':'), sort_keys=sort_keys)

            self._validate_overlay(values['overlay'])

            if auto:
                pth = '/{mapid}/geojson({overlay})/auto/{width}x{height}.{fmt}'
            else:
                pth = ('/{mapid}/geojson({overlay})/{lon},{lat},{z}'
                       '/{width}x{height}.{fmt}')
        else:
            if auto:
                raise errors.InvalidCoordError(
                    "Must provide features if lat, lon, z are None")

            # No overlay
            pth = '/{mapid}/{lon},{lat},{z}/{width}x{height}.{fmt}'

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.get(uri)
        self.handle_http_error(res)
        return res
