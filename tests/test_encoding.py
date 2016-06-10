import pytest
import copy
import json
from mapbox.encoding import (read_points,
                             encode_waypoints,
                             encode_polyline,
                             encode_coordinates_json)


gj_point_features = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -87.33787536621092,
            36.539156961321574]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [
            -88.2476806640625,
            36.92217534275667]}}]


gj_multipoint_features = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "MultiPoint",
        "coordinates": [
            [-87.33787536621092,
             36.539156961321574],
            [-88.2476806640625,
             36.92217534275667]]}}]


gj_line_features = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [-87.33787536621092,
             36.539156961321574],
            [-88.2476806640625,
             36.92217534275667]]}}]


class GeoThing(object):
    __geo_interface__ = None

    def __init__(self, thing):
        self.__geo_interface__ = thing


def test_read_geojson_features():
    expected = [(-87.33787536621092, 36.539156961321574),
                (-88.2476806640625, 36.92217534275667)]

    assert expected == list(read_points(gj_point_features))
    assert expected == list(read_points(gj_multipoint_features))
    assert expected == list(read_points(gj_line_features))


def test_geo_interface():
    expected = [(-87.33787536621092, 36.539156961321574),
                (-88.2476806640625, 36.92217534275667)]

    features = [GeoThing(gj_point_features[0]),
                GeoThing(gj_point_features[1])]
    assert expected == list(read_points(features))

    geoms = [GeoThing(gj_point_features[0]['geometry']),
             GeoThing(gj_point_features[1]['geometry'])]
    assert expected == list(read_points(geoms))


def test_encode_waypoints():
    expected = "-87.337875,36.539157;-88.247681,36.922175"

    assert expected == encode_waypoints(gj_point_features)
    assert expected == encode_waypoints(gj_multipoint_features)
    assert expected == encode_waypoints(gj_line_features)


def test_encode_limits():
    expected = "-87.337875,36.539157;-88.247681,36.922175"
    assert expected == encode_waypoints(gj_point_features)
    with pytest.raises(ValueError) as exc:
        encode_waypoints(gj_point_features, min_limit=3)
    assert 'at least' in str(exc.value)

    with pytest.raises(ValueError) as exc:
        encode_waypoints(gj_point_features, max_limit=1)
    assert 'at most' in str(exc.value)


def test_unsupported_geometry():
    unsupported = copy.deepcopy(gj_point_features)
    unsupported[0]['geometry']['type'] = "MultiPolygonnnnnn"
    with pytest.raises(ValueError) as exc:
        list(read_points(unsupported))
    assert 'Unsupported geometry' in str(exc.value)


def test_unknown_object():
    unknown = ["foo", "bar"]
    with pytest.raises(ValueError) as exc:
        list(read_points(unknown))
    assert 'Unknown object' in str(exc.value)


def test_encode_polyline():
    expected = "wp_~EvdatO{xiAfupD"
    assert expected == encode_polyline(gj_point_features)
    assert expected == encode_polyline(gj_multipoint_features)
    assert expected == encode_polyline(gj_line_features)


def test_encode_coordinates_json():
    expected = {
        'coordinates': [
            [-87.33787536621092, 36.539156961321574],
            [-88.2476806640625, 36.92217534275667]]}

    assert expected == json.loads(encode_coordinates_json(gj_point_features))
    assert expected == json.loads(encode_coordinates_json(gj_multipoint_features))
    assert expected == json.loads(encode_coordinates_json(gj_line_features))
