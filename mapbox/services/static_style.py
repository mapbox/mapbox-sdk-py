import json

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


class StaticStyle(Service):
    """Access to the Static Map API."""

    @property
    def baseuri(self):
        """
        /styles/v1/{username}/{style_id}/static/{overlay}/{lon},{lat},{zoom},{bearing},{pitch}{auto}/{width}x{height}{@2x}
        """
        return 'https://{0}/styles/v1'.format(self.host)

    def image(self, username, style_id, lon=None, lat=None, zoom=None, features=None,
              pitch=0, bearing=0, width=600, height=600, twox=False, sort_keys=False):

        if lon is not None and lat is not None and zoom is not None:
            auto = False
            lat = validate_lat(lat)
            lon = validate_lon(lon)
        else:
            auto = True

        if pitch < 0 or pitch > 60:
            raise ValueError("bad pitch")  # TODO raise proper error here

        if bearing < 0 or bearing > 360:
            raise ValueError("bad bearing")  # TODO raise proper error here

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
            auto="auto" if auto else '',
            twox='@2x' if twox else '',
            width=str(width),
            height=str(height))

        if features:
            collection = normalize_geojson_featurecollection(features)
            values['overlay'] = json.dumps(
                collection, separators=(',', ':'), sort_keys=sort_keys)

            validate_overlay(values['overlay'])

            pth = '{username}/{style_id}/static/{overlay}/'
            if auto:
                pth += '{bearing},{pitch}{auto}/{width}x{height}{twox}'
            else:
                pth += '{lon},{lat},{zoom},{bearing},{pitch}/{width}x{height}{twox}'
        else:
            if auto:
                raise errors.InvalidCoordError(
                    "Must provide features or lat, lon, z")

            # No overlay
            pth = ('/{username}/{style_id}/static/'
                   '{lon},{lat},{zoom},{bearing},{pitch}/{width}x{height}{twox}')

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.get(uri)
        self.handle_http_error(res)
        return res
