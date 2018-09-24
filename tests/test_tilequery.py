from mapbox.errors import (
    InvalidCoordError,
    InvalidParameterError
)

from mapbox.services.tilequery import Tilequery

from pytest import (
    mark,
    raises
)

from responses import (
    activate,
    add,
    GET
)


def test_object_properties():
    tilequery = Tilequery()

    assert tilequery.api_name
    assert tilequery.api_version
    assert tilequery.valid_geometries
    assert tilequery.base_uri


@mark.parametrize("lon", [-181, 181])
def test_validate_lon_invalid(lon):
    tilequery = Tilequery()

    with raises(InvalidCoordError) as exception:
        tilequery._validate_lon(lon)


@mark.parametrize("lon", [-180, 0, 180])
def test_validate_lon_valid(lon):
    tilequery = Tilequery()
    result = tilequery._validate_lon(lon)
    assert result == lon


@mark.parametrize("lat", [-86, 86])
def test_validate_lat_invalid(lat):
    tilequery = Tilequery()

    with raises(InvalidCoordError) as exception:
        tilequery._validate_lat(lat)


@mark.parametrize("lat", [-85.0511, 0, 85.0511])
def test_validate_lat_valid(lat):
    tilequery = Tilequery()
    result = tilequery._validate_lat(lat)
    assert result == lat


def test_validate_radius_invalid():
    tilequery = Tilequery()

    with raises(InvalidParameterError) as exception:
        tilequery._validate_radius(-1)


@mark.parametrize("radius", [0, 1000000])
def test_validate_radius_valid(radius):
    tilequery = Tilequery()
    result = tilequery._validate_radius(radius)
    assert result == radius


@mark.parametrize("limit", [0, 51])
def test_validate_limit_invalid(limit):
    tilequery = Tilequery()

    with raises(InvalidParameterError) as exception:
        tilequery._validate_limit(limit)


@mark.parametrize("limit", [1, 25, 50])
def test_validate_limit_valid(limit):
    tilequery = Tilequery()
    result = tilequery._validate_limit(limit)
    assert result == limit


def test_validate_geometry_invalid():
    tilequery = Tilequery()

    with raises(InvalidParameterError) as exception:
        tilequery._validate_geometry("invalid")


@mark.parametrize("geometry", ["linestring", "point", "polygon"])
def test_validate_radius_geometry(geometry):
    tilequery = Tilequery()
    result = tilequery._validate_geometry(geometry)
    assert result == geometry


@activate
def test_tilequery_one_mapid():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1
    )

    assert response.status_code == 200

    
@activate
def test_tilequery_two_mapids():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v9%2Cmapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        ["mapbox.mapbox-streets-v9", "mapbox.mapbox-streets-v10"],
        0.0,
        1.1
    )

    assert response.status_code == 200
    
    
@activate
def test_tilequery_with_radius():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&limit=25",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        limit=25
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        dedupe=True
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        geometry="linestring"
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        layers=[
            "layer0",
            "layer1",
            "layer2"
        ]
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_and_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_and_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        dedupe=True
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        geometry="linestring"
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        layers=[
            "layer0",
            "layer1",
            "layer2"
        ]
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_and_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        dedupe=True
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        geometry="linestring"
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        layers=[
            "layer0",
            "layer1",
            "layer2"
        ]
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_dedupe_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        dedupe=True,
        geometry="linestring"
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_dedupe_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        dedupe=True,
        layers=[
            "layer0",
            "layer1",
            "layer2"
        ]
    )

    assert response.status_code == 200


@activate
def test_tilequery_with_radius_limit_dedupe_geometry_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1,
        radius=25,
        limit=25,
        dedupe=True,
        geometry="linestring",
        layers=[
            "layer0",
            "layer1",
            "layer2"
        ]
    )

    assert response.status_code == 200
    
    
@activate
def test_tilequery_geojson_method():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilequery = Tilequery(access_token="pk.test")

    response = tilequery.tilequery(
        "mapbox.mapbox-streets-v10",
        0.0,
        1.1
    )

    assert response.status_code == 200
    assert response.geojson() == response.json()
