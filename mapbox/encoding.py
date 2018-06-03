import json

from numbers import Number

from .compat import string_type

from .errors import (
    InvalidFeatureError,
    InvalidParameterError
)

import polyline


def _geom_points(geom):
    """GeoJSON geometry to a sequence of point tuples
    """
    if geom['type'] == 'Point':
        yield tuple(geom['coordinates'])
    elif geom['type'] in ('MultiPoint', 'LineString'):
        for position in geom['coordinates']:
            yield tuple(position)
    else:
        raise InvalidFeatureError(
            "Unsupported geometry type:{0}".format(geom['type']))


def read_points(features):
    """ Iterable of features to a sequence of point tuples
    Where "features" can be either GeoJSON mappings
    or objects implementing the geo_interface
    """
    for feature in features:

        if isinstance(feature, (tuple, list)) and len(feature) == 2:
            yield feature

        elif hasattr(feature, '__geo_interface__'):
            # An object implementing the geo_interface
            try:
                # Could be a Feature...
                geom = feature.__geo_interface__['geometry']
                for pt in _geom_points(geom):
                    yield pt
            except KeyError:
                # ... or a geometry directly
                for pt in _geom_points(feature.__geo_interface__):
                    yield pt

        elif 'type' in feature and feature['type'] == 'Feature':
            # A GeoJSON-like mapping
            geom = feature['geometry']
            for pt in _geom_points(geom):
                yield pt

        elif 'coordinates' in feature:
            geom = feature
            for pt in _geom_points(geom):
                yield pt

        else:
            raise InvalidFeatureError(
                "Unknown object: Not a GeoJSON Point feature or "
                "an object with __geo_interface__:\n{0}".format(feature))


def encode_waypoints(features, min_limit=None, max_limit=None, precision=6):
    """Given an iterable of features
    return a string encoded in waypoint-style used by certain mapbox APIs
    ("lon,lat" pairs separated by ";")
    """
    coords = ['{lon},{lat}'.format(
                  lon=float(round(lon, precision)),
                  lat=float(round(lat, precision)))
              for lon, lat in read_points(features)]

    if min_limit is not None and len(coords) < min_limit:
        raise InvalidFeatureError(
            "Not enough features to encode coordinates, "
            "need at least {0}".format(min_limit))
    if max_limit is not None and len(coords) > max_limit:
        raise InvalidFeatureError(
            "Too many features to encode coordinates, "
            "need at most {0}".format(max_limit))

    return ';'.join(coords)


def encode_polyline(features):
    """Encode and iterable of features as a polyline
    """
    points = list(read_points(features))
    latlon_points = [(x[1], x[0]) for x in points]
    return polyline.encode(latlon_points)


def encode_coordinates_json(features):
    """Given an iterable of features
    return a JSON string to be used as the request body for the distance API:
    a JSON object, with a key coordinates,
    which has an array of [ Longitude, Lattitude ] pairs
    """
    coords = {
        'coordinates': list(read_points(features))}
    return json.dumps(coords)


def validate_snapping(snaps, features):
    bearings = []
    radii = []
    if snaps is None:
        return (None, None)
    if len(snaps) != len(features):
        raise InvalidParameterError(
            'Must provide exactly one snapping element for each input feature')
    for snap in snaps:
        if snap is None:
            bearings.append(None)
            radii.append(None)
        else:
            try:
                # radius-only
                radius = validate_radius(snap)
                bearing = None
            except InvalidParameterError:
                # (radius, angle, range) tuple
                try:
                    radius, angle, rng = snap
                except ValueError:
                    raise InvalidParameterError(
                        'waypoint snapping should contain 3 elements: '
                        '(bearing, angle, range)')
                validate_radius(radius)

                try:
                    assert angle >= 0
                    assert angle <= 360
                    assert rng >= 0
                    assert rng <= 360
                except (TypeError, AssertionError):
                    raise InvalidParameterError(
                        'angle and range must be between 0 and 360')
                bearing = (angle, rng)

            bearings.append(bearing)
            radii.append(radius)

    if all([b is None for b in bearings]):
        bearings = None

    return (bearings, radii)


def validate_radius(radius):
    if radius is None:
        return None

    if isinstance(radius, string_type):
        if radius != 'unlimited':
            raise InvalidParameterError(
                '{0} is not a valid radius'.format(radius))
    elif isinstance(radius, Number):
        if radius <= 0:
            raise InvalidParameterError(
                'radius must be greater than zero'.format(radius))
    else:
        raise InvalidParameterError(
            '{0} is not a valid radius'.format(radius))

    return radius


def encode_bearing(b):
    if b is None:
        return ''
    else:
        return '{},{}'.format(*b)
