
def _geom_points(geom):
    """GeoJSON geometry to a sequence of point tuples
    """
    if geom['type'] == 'Point':
        yield tuple(geom['coordinates'])
    elif geom['type'] in ('MultiPoint', 'LineString'):
        for position in geom['coordinates']:
            yield tuple(position)
    else:
        raise ValueError(
            "Unsupported geometry type:{0}".format(geom['type']))


def read_points(features):
    """ Iterable of features to a sequence of point tuples
    Where "features" can be either GeoJSON mappings
    or objects implementing the geo_interface
    """
    for feature in features:

        if hasattr(feature, '__geo_interface__'):
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

        elif feature['type'] == 'Feature':
            # A GeoJSON-like mapping
            geom = feature['geometry']
            for pt in _geom_points(geom):
                yield pt

        else:
            raise ValueError("Unknown object: Not a GeoJSON feature or "
                             "an object with __geo_interface__:\n{0}".format(feature))


def encode_waypoints(features, min_limit=None, max_limit=None, precision=6):
    """Given an iterable of features
    return a string encoded in waypoint-style used by certain mapbox APIs
    ("lon,lat" pairs separated by ";")
    """
    coords = ['{lon:.{p}f},{lat:.{p}f}'.format(lon=lon, lat=lat, p=precision)
              for lon, lat in read_points(features)]

    if min_limit is not None and len(coords) < min_limit:
        raise ValueError("Not enough features to encode waypoints, "
                         "need at least {0}".format(min_limit))
    if max_limit is not None and len(coords) > max_limit:
        raise ValueError("Too many features to encode waypoints, "
                         "need at most {0}".format(max_limit))

    return ';'.join(coords)


# TODO
# def encode_polyline(features, zoom_level=18):
