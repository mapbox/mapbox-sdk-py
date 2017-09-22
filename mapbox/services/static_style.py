import json
import warnings

from uritemplate import URITemplate

from mapbox import errors
from mapbox.services.base import Service
from mapbox.utils import normalize_geojson_featurecollection


def validate_lat(val):
    if val < -85.0511 or val > 85.0511:
        raise errors.InvalidCoordError(
            "Latitude must be between -85.0511 and 85.0511")
    return val


def validate_lon(val):
    if val < -180 or val > 180:
        raise errors.InvalidCoordError(
            "Longitude must be between -180 and 180")
    return val


def validate_image_size(val):
    if not 1 < val < 1280:
        raise errors.ImageSizeError(
            "Image height and width must be between 1 and 1280")
    return val


def validate_overlay(val):
    if len(val) > 2073:  # limit is 2083 minus the 'geojson()'
        raise errors.InputSizeError(
            "GeoJSON is too large for the static maps API, "
            "must be less than 2073 characters")
    return val


def validate_pitch(val):
    if val < 0 or val > 60:
        raise errors.InvalidCoordError("Pitch must be between 0 and 60")
    return val


def validate_bearing(val):
    if val < 0 or val > 365:
        raise errors.InvalidCoordError("Bearing must be between 0 and 365")
    return val


class StaticStyle(Service):
    """Access to the Static Map API V1"""

    api_name = 'styles'
    api_version = 'v1'

    def tile(self, username, style_id, z, x, y, tile_size=512, retina=False):
        "/styles/v1/{username}/{style_id}/tiles/{tileSize}/{z}/{x}/{y}{@2x}"
        if tile_size not in (256, 512):
            raise errors.ImageSizeError('tile_size must be 256 or 512 pixels')

        pth = '/{username}/{style_id}/tiles/{tile_size}/{z}/{x}/{y}'

        values = dict(username=username, style_id=style_id,
                      tile_size=tile_size, z=z, x=x, y=y)

        uri = URITemplate(self.baseuri + pth).expand(**values)
        if retina:
            uri += '@2x'
        res = self.session.get(uri)
        self.handle_http_error(res)
        return res

    def wmts(self, username, style_id):
        pth = '/{}/{}/wmts'.format(username, style_id)
        uri = URITemplate(self.baseuri + pth)
        res = self.session.get(uri)
        self.handle_http_error(res)
        return res

    def image(self, username, style_id, lon=None, lat=None, zoom=None, features=None,
              pitch=0, bearing=0, width=600, height=600, retina=None, sort_keys=False,
              attribution=None, logo=None, before_layer=None, twox=None):

        params = {}
        if attribution is not None:
            params['attribution'] = 'true' if attribution else 'false'
        if logo is not None:
            params['logo'] = 'true' if logo else 'false'
        if before_layer is not None:
            params['before_layer'] = before_layer

        # twox as a deprecated alias for retina
        if retina is None:
            if twox is not None:
                warnings.warn('twox is a deprecated alias for retina',
                              errors.MapboxDeprecationWarning)
                retina = twox
        else:
            if twox is not None:
                raise errors.ValidationError('Conflicting args; Remove twox and use retina')

        if lon is not None and lat is not None and zoom is not None:
            auto = False
            lat = validate_lat(lat)
            lon = validate_lon(lon)
        else:
            auto = True

        pitch = validate_pitch(pitch)
        bearing = validate_bearing(bearing)
        width = validate_image_size(width)
        height = validate_image_size(height)

        values = dict(
            username=username,
            style_id=style_id,
            pitch=str(pitch),
            bearing=str(bearing),
            lon=str(lon),
            lat=str(lat),
            zoom=str(zoom),
            auto=auto,
            width=str(width),
            height=str(height))

        if features:
            collection = normalize_geojson_featurecollection(features)
            values['overlay'] = json.dumps(
                collection, separators=(',', ':'), sort_keys=sort_keys)

            validate_overlay(values['overlay'])

            pth = '/{username}/{style_id}/static/geojson({overlay})/'
            if auto:
                # TODO what about {bearing} and {pitch}
                pth += 'auto/{width}x{height}'
            else:
                pth += '{lon},{lat},{zoom},{bearing},{pitch}/{width}x{height}'
        else:
            if auto:
                raise errors.InvalidCoordError(
                    "Must provide features or lat, lon, z")

            # No overlay
            pth = ('/{username}/{style_id}/static/'
                   '{lon},{lat},{zoom},{bearing},{pitch}/{width}x{height}')

        uri = URITemplate(self.baseuri + pth).expand(**values)

        # @2x handled separately to avoid HTML escaping the ampersand
        if retina:
            uri += '@2x'

        res = self.session.get(uri, params=params)
        self.handle_http_error(res)
        return res
