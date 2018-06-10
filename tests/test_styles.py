from os import remove

from mapbox.errors import (
    InvalidFileFormatError,
    InvalidStartError
)

from mapbox.services.styles import Styles

from base64 import b64encode

from pytest import raises

from responses import (
    activate,
    add,
    DELETE,
    GET,
    PATCH,
    POST,
    PUT
)


USERNAME = b64encode(b"{\"u\":\"user\"}").decode("utf-8")
ACCESS_TOKEN = "pk.{}.test".format(USERNAME)
STYLE_ID = "mapbox://styles/mapbox/streets-v10"
ENCODED_STYLE_ID = "mapbox%3A%2F%2Fstyles%2Fmapbox%2Fstreets-v10"


# utility function

def create_test_style_object():
  with open("./style-object.json", "w") as file:
      file.write("{\"key\": \"value\"}")


# utility function

def create_test_style_object_with_invalid_keys():
  with open("./style-object.json", "w") as file:
      file.write("{\"key\": \"value\", \"created\": \"value\", \"modified\": \"value\"}")


# utility function

def create_test_icon():
  with open("./icon.svg", "w") as file:
      file.write("<svg></svg>")


def test_object_properties():
    styles = Styles()

    assert styles.api_name
    assert styles.api_version
    assert styles.valid_file_formats
    assert styles.base_uri


def test_validate_start():
    styles = Styles()

    # invalid value (value < 0)

    with raises(InvalidStartError):
        start = -1
        result = styles._validate_start(start)

    # invalid value (value > 65280)

    with raises(InvalidStartError):
        start = 65281
        result = styles._validate_start(start)

    # invalid value (value % 256 != 0)

    with raises(InvalidStartError):
        start = 257
        result = styles._validate_start(start)

    # valid value

    start = 0
    result = styles._validate_start(start)
    assert result == start

    # valid value

    start = 256
    result = styles._validate_start(start)
    assert result == start


def test_validate_retina():
    styles = Styles()

    # True

    retina = True
    result = styles._validate_retina(retina)
    assert result == "@2x"

    # False

    retina = False
    result = styles._validate_retina(retina)
    assert result == ""


def test_validate_file_format():
    styles = Styles()

    # invalid value

    with raises(InvalidFileFormatError) as exception:
        file_format = "invalid"
        result = styles._validate_file_format(file_format)
    
    # valid values

    file_formats = [
        "json",
        "png"
    ]

    for file_format in file_formats:
        result = styles._validate_file_format(file_format)
        assert result == file_format


@activate
def test_style():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.style(
        STYLE_ID
    )

    assert response.status_code == 200


@activate
def test_list_styles():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.list_styles()

    assert response.status_code == 200


@activate
def test_create_style():

    # style_object == dict

    add(
        method=POST,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.create_style(
        {
            "key": "value"
        }
    )

    assert response.status_code == 200

    # style_object == file

    create_test_style_object()

    add(
        method=POST,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.create_style(
        "style-object.json"
    )

    assert response.status_code == 200
    remove("style-object.json")


@activate
def test_update_style():

    # style_object == dict

    add(
        method=PATCH,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.update_style(
        {
            "key": "value",
            "created": "value",
            "modified": "value"
        }
    )

    assert response.status_code == 200

    # style_object == file

    create_test_style_object_with_invalid_keys()

    add(
        method=PATCH,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.update_style(
        "style-object.json"
    )

    assert response.status_code == 200
    remove("style-object.json")


@activate
def test_delete_style():
    add(
        method=DELETE,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        status=204
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.delete_style(
        STYLE_ID
    )

    assert response.status_code == 204


@activate
def test_font_glyphs():

    # one font

    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/fonts/v1" +
        "/user" +
        "/font" +
        "/256-511.pbf" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="256-511.pbf",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.font_glyphs(
        ["font"],
        256
    )

    assert response.status_code == 200

    # multiple fonts

    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/fonts/v1" +
        "/user" +
        "/first-font%2Csecond-font%2Cthird-font" +
        "/256-511.pbf" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="256-511.pbf",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.font_glyphs(
        ["first-font", "second-font", "third-font"],
        256
    )

    assert response.status_code == 200


@activate
def test_sprite():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.sprite(
        STYLE_ID,
        "sprite"
    )

    assert response.status_code == 200


@activate
def test_sprite_with_retina():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite@2x" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.sprite(
        STYLE_ID,
        "sprite",
        retina=True
    )

    assert response.status_code == 200


@activate
def test_sprite_with_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite.png" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="sprite.png",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.sprite(
        STYLE_ID,
        "sprite",
        file_format="png"
    )

    assert response.status_code == 200


@activate
def test_sprite_with_retina_and_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite@2x.png" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="sprite@2x.png",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.sprite(
        STYLE_ID,
        "sprite",
        retina=True,
        file_format="png"
    )

    assert response.status_code == 200


@activate
def test_add_image():
    create_test_icon()

    add(
        method=PUT,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite" +
        "/icon.svg" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.add_image(
        STYLE_ID,
        "sprite",
        "icon.svg"
    )

    assert response.status_code == 200
    remove("./icon.svg")


@activate
def test_delete_image():
    add(
        method=DELETE,
        url="https://api.mapbox.com" +
        "/styles/v1" +
        "/user" +
        "/{}".format(ENCODED_STYLE_ID) +
        "/sprite" +
        "/icon.svg" +
        "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    styles = Styles(access_token=ACCESS_TOKEN)

    response = styles.delete_image(
        STYLE_ID,
        "sprite",
        "icon.svg"
    )

    assert response.status_code == 200
