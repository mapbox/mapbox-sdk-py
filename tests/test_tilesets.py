from mapbox.errors import (
    InvalidTilesetTypeError,
    InvalidVisibilityError,
    InvalidSortbyError,
    InvalidLimitError
)

from mapbox.services.tilesets import Tilesets

from base64 import b64encode

from pytest import (
    mark, 
    raises
)

from responses import (
    activate,
    add,
    GET
)


USERNAME = b64encode(b"{\"u\":\"user\"}").decode("utf-8")
ACCESS_TOKEN = "pk.{}.test".format(USERNAME)


def test_object_attributes():
    tilesets = Tilesets()

    assert tilesets.api_name
    assert tilesets.api_version
    assert tilesets.valid_tileset_types
    assert tilesets.valid_visibilities
    assert tilesets.valid_sortbys
    assert tilesets.base_uri


def test_validate_tileset_type_invalid():
    tilesets = Tilesets()

    with raises(InvalidTilesetTypeError) as exception:
        tileset_type = "invalid"
        result = tilesets._validate_tileset_type(tileset_type)


@mark.parametrize("tileset_type", ["raster", "vector"])
def test_validate_tileset_type_valid(tileset_type):
    tilesets = Tilesets()
    result = tilesets._validate_tileset_type(tileset_type)
    assert result == tileset_type


def test_validate_visibility_invalid():
    tilesets = Tilesets()

    with raises(InvalidVisibilityError) as exception:
        visibility = "invalid"
        result = tilesets._validate_visibility(visibility)


@mark.parametrize("visibility", ["private", "public"])
def test_validate_visibility_valid(visibility):
    tilesets = Tilesets()
    result = tilesets._validate_visibility(visibility)
    assert result == visibility


def test_validate_sortby_invalid():
    tilesets = Tilesets()

    with raises(InvalidSortbyError) as exception:
        sortby = "invalid"
        result = tilesets._validate_sortby(sortby)


@mark.parametrize("sortby", ["created", "modified"])
def test_validate_sortby_valid(sortby):
    tilesets = Tilesets()
    result = tilesets._validate_sortby(sortby)
    assert result == sortby


@mark.parametrize("limit", [0, 501])
def test_validate_limit_invalid(limit):
    tilesets = Tilesets()

    with raises(InvalidLimitError) as exception:
        result = tilesets._validate_limit(limit)


@mark.parametrize("limit", [1, 250, 500])
def test_validate_limit_valid(limit):
    tilesets = Tilesets()
    result = tilesets._validate_limit(limit)
    assert result == limit


@activate
def test_tilesets():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets()
    assert response.status_code == 200


@activate
@mark.parametrize("tileset_type", ["raster", "vector"])
def test_tilesets_with_tileset_type(tileset_type):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&type={}".format(tileset_type),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type=tileset_type)
    assert response.status_code == 200


@activate
@mark.parametrize("visibility", ["private", "public"])
def test_tilesets_with_visibility(visibility):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&visibility={}".format(visibility),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(visibility=visibility)
    assert response.status_code == 200


@activate
@mark.parametrize("sortby", ["created", "modified"])
def test_tilesets_with_sortby(sortby):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&sortby={}".format(sortby),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(sortby=sortby)
    assert response.status_code == 200


@activate
@mark.parametrize("limit", [1, 250, 500])
def test_tilesets_with_limit(limit):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&limit={}".format(limit),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(limit=limit)
    assert response.status_code == 200


@activate
def test_tilesets_with_tileset_type_and_visibility():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&type=vector" +
        "&visibility=public",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type="vector", visibility="public")
    assert response.status_code == 200


@activate
def test_tilesets_with_tileset_type_and_sortby():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&type=vector" +
        "&sortby=created",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type="vector", sortby="created")
    assert response.status_code == 200


@activate
def test_tilesets_with_tileset_type_and_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&type=vector" +
        "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type="vector", limit=500)
    assert response.status_code == 200


@activate
def test_tilesets_with_visibility_and_sortby():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&visibility=public" +
        "&sortby=created",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(visibility="public", sortby="created")
    assert response.status_code == 200


@activate
def test_tilesets_with_visibility_and_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN) +
        "&visibility=public" +
        "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(visibility="public", limit=500)
    assert response.status_code == 200


@activate
def test_tilesets_with_sortby_and_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/tilesets/v1" +
        "/user?access_token={}".format(ACCESS_TOKEN) +
        "&sortby=created" +
        "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(sortby="created", limit=500)
    assert response.status_code == 200
