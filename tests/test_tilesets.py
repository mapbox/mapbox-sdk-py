from mapbox.errors import (
    InvalidTilesetTypeError,
    InvalidVisibilityError,
    InvalidSortbyError,
    InvalidLimitError
)

from mapbox.services.tilesets import Tilesets

from base64 import b64encode

from pytest import raises

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

def test_validate_tileset_type():
    tilesets = Tilesets()

    # invalid value

    with raises(InvalidTilesetTypeError) as exception:
        tileset_type = "invalid"
        result = tilesets._validate_tileset_type(tileset_type)

    # valid values

    tileset_types = [
        "raster",
        "vector"
    ]

    for tileset_type in tileset_types:
        result = tilesets._validate_tileset_type(tileset_type)
        assert result == tileset_type

def test_validate_visibility():
    tilesets = Tilesets()

    # invalid value

    with raises(InvalidVisibilityError) as exception:
        visibility = "invalid"
        result = tilesets._validate_visibility(visibility)

    # valid values

    visibilities = [
        "private",
        "public"
    ]

    for visibility in visibilities:
        result = tilesets._validate_visibility(visibility)
        assert result == visibility

def test_validate_sortby():
    tilesets = Tilesets()

    # invalid value

    with raises(InvalidSortbyError) as exception:
        sortby = "invalid"
        result = tilesets._validate_sortby(sortby)

    # valid values

    sortbys = [
        "created",
        "modified"
    ]

    for sortby in sortbys:
        result = tilesets._validate_sortby(sortby)
        assert result == sortby

def test_validate_limit():
    tilesets = Tilesets()

    # invalid value

    with raises(InvalidLimitError) as exception:
        limit = 0
        result = tilesets._validate_limit(limit)

    # invalid value

    with raises(InvalidLimitError) as exception:
        limit = 501
        result = tilesets._validate_limit(limit)

    # valid value

    limit = 100
    result = tilesets._validate_limit(limit)
    assert result == limit

@activate
def test_tilesets():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets()
    assert response.status_code == 200

@activate
def test_tilesets_with_tileset_type():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&type=raster".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type="raster")
    assert response.status_code == 200

    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&type=vector".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(tileset_type="vector")
    assert response.status_code == 200

@activate
def test_tilesets_with_visibility():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&visibility=private".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(visibility="private")
    assert response.status_code == 200

    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&visibility=public".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(visibility="public")
    assert response.status_code == 200

@activate
def test_tilesets_with_sortby():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&sortby=created".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(sortby="created")
    assert response.status_code == 200

    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&sortby=modified".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(sortby="modified")
    assert response.status_code == 200

@activate
def test_tilesets_with_limit():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&limit=500".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(limit=500)
    assert response.status_code == 200

@activate
def test_tilesets_with_tileset_type_and_visibility():
    add(
        method=GET,
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&type=vector&visibility=public".format(ACCESS_TOKEN),
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
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&type=vector&sortby=created".format(ACCESS_TOKEN),
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
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&type=vector&limit=500".format(ACCESS_TOKEN),
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
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&visibility=public&sortby=created".format(ACCESS_TOKEN),
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
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&visibility=public&limit=500".format(ACCESS_TOKEN),
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
        url="https://api.mapbox.com/tilesets/v1/user?access_token={}&sortby=created&limit=500".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    tilesets = Tilesets(access_token=ACCESS_TOKEN)
    response = tilesets.tilesets(sortby="created", limit=500)
    assert response.status_code == 200
