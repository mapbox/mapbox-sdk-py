import json

from .errors import InvalidFeatureError
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
    coords = ['{lon},{lat}'.format(lon=round(lon, precision), lat=round(lat, precision))
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
    which has an array of [ Longitude, Latitidue ] pairs
    """
    coords = {
        'coordinates': list(read_points(features))}
    return json.dumps(coords)
