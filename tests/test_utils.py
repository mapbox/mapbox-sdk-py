import pytest

from mapbox.utils import normalize_geojson_featurecollection


geom = {'type': 'Point', 'coordinates': (-122, 45)}
feat = {'type': 'Feature', 'geometry': geom, 'properties': {}}
coll = {'type': 'FeatureCollection', 'features': [feat]}
coll2 = {'type': 'FeatureCollection', 'features': [feat, feat]}


def test_geom():
    res = normalize_geojson_featurecollection(geom)
    assert res['type'] == 'FeatureCollection'
    assert res == coll


def test_feat():
    res = normalize_geojson_featurecollection(feat)
    assert res['type'] == 'FeatureCollection'
    assert res == coll


def test_coll():
    res = normalize_geojson_featurecollection(coll)
    assert res['type'] == 'FeatureCollection'
    assert res == coll


def test_mult_geom():
    geoms = (geom, geom)
    res = normalize_geojson_featurecollection(geoms)
    assert res['type'] == 'FeatureCollection'
    assert res == coll2


def test_mult_feat():
    feats = (feat, feat)
    res = normalize_geojson_featurecollection(feats)
    assert res['type'] == 'FeatureCollection'
    assert res == coll2


def test_mult_coll():
    colls = (coll, coll)
    res = normalize_geojson_featurecollection(colls)
    assert res['type'] == 'FeatureCollection'
    assert res == coll2


def test_mix():
    objs = (geom, feat, coll, coll2)
    res = normalize_geojson_featurecollection(objs)
    assert res['type'] == 'FeatureCollection'
    assert len(res['features']) == 5


def test_nonsense():
    with pytest.raises(ValueError):
        normalize_geojson_featurecollection(123)

    with pytest.raises(ValueError):
        normalize_geojson_featurecollection({'foo': 'bar'})

    with pytest.raises(ValueError):
        normalize_geojson_featurecollection({'type': 'not-geojson'})
