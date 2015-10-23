import responses
import mapbox


points = [{
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [-112.084004, 36.05322]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [-112.083914, 36.053573]}}, {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [-112.083965, 36.053845]}}]


@responses.activate
def test_surface():
    body = """{"results":[{"id":0,"latlng":{"lat":36.05322,"lng":-112.084004},"ele":2186.361304424316},{"id":1,"latlng":{"lat":36.053573,"lng":-112.083914},"ele":2187.6233827411997},{"id":2,"latlng":{"lat":36.053845,"lng":-112.083965},"ele":2163.921475128245}],"attribution":"&lt;a href='https://www.mapbox.com/about/maps/' target='_blank'&gt;&amp;copy; Mapbox&lt;/a&gt;"}"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/surface/mapbox.mapbox-terrain-v1.json?access_token=pk.test&points=-112.084004%2C36.053220%3B-112.083914%2C36.053573%3B-112.083965%2C36.053845&geojson=false&fields=ele&layer=contour',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    res = mapbox.Surface(access_token='pk.test').surface(points)
    assert res.status_code == 200


@responses.activate
def test_surface_geojson():
    body = """{"results":{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-112.084004,36.05322]},"properties":{"id":0,"ele":2186.361304424316}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-112.083914,36.053573]},"properties":{"id":1,"ele":2187.6233827411997}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-112.083965,36.053845]},"properties":{"id":2,"ele":2163.921475128245}}]},"attribution":"<a href='https://www.mapbox.com/about/maps/' target='_blank'>&copy; Mapbox</a>"}"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/surface/mapbox.mapbox-terrain-v1.json?access_token=pk.test&fields=ele&layer=contour&geojson=true&points=-112.084004%2C36.053220%3B-112.083914%2C36.053573%3B-112.083965%2C36.053845',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    fc = mapbox.Surface(access_token='pk.test').surface_geojson(points)
    assert fc['type'] == 'FeatureCollection'
    assert len(fc['features']) == 3
