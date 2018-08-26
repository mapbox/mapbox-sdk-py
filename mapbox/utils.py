from collections import Mapping, Sequence


def normalize_geojson_featurecollection(obj):
    """Takes a geojson-like mapping representing
    geometry, Feature or FeatureCollection (or a sequence of such objects)
    and returns a FeatureCollection-like dict
    """
    if not isinstance(obj, Sequence):
        obj = [obj]

    features = []
    for x in obj:
        if not isinstance(x, Mapping) or 'type' not in x:
            raise ValueError(
                "Expecting a geojson-like mapping or sequence of them")

        if 'features' in x:
            features.extend(x['features'])
        elif 'geometry' in x:
            features.append(x)
        elif 'coordinates' in x:
            feat = {'type': 'Feature',
                    'properties': {},
                    'geometry': x}
            features.append(feat)
        else:
            raise ValueError(
                "Expecting a geojson-like mapping or sequence of them")

    return {'type': 'FeatureCollection', 'features': features}
