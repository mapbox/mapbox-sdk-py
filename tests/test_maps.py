from mapbox.errors import (
    InvalidZoomError,
    InvalidColumnError,
    InvalidRowError,
    InvalidFileFormatError,
    InvalidPeriodError,
    InvalidFeatureFormatError,
    InvalidMarkerNameError,
    InvalidLabelError,
    InvalidColorError,
    ValidationError
)

from mapbox.services.maps import Maps

from pytest import raises

from responses import (
    activate,
    add,
    GET
)

def test_object_properties():
    maps = Maps()

    assert maps.api_name
    assert maps.api_version
    assert maps.valid_file_formats
    assert maps.valid_feature_formats
    assert maps.valid_marker_names
    assert maps.base_uri

def test_validate_z():
    maps = Maps()

    # invalid value

    with raises(InvalidZoomError) as exception:
        z = -1
        result = maps._validate_z(z)

    # invalid value

    with raises(InvalidZoomError) as exception:
        z = 21
        result = maps._validate_z(z)

    # valid value

    z = 10
    result = maps._validate_z(z)
    assert result == z

def test_validate_x():
    maps = Maps()

    # invalid value

    with raises(InvalidColumnError) as exception:
        x = -1
        z = 10
        result = maps._validate_x(x, z)

    # invalid value

    with raises(InvalidColumnError) as exception:
        x = 1024
        z = 10
        result = maps._validate_x(x, z)

    # valid value

    x = 512
    z = 10
    result = maps._validate_x(x, z)
    assert result == x

def test_validate_y():
    maps = Maps()

    # invalid value

    with raises(InvalidRowError) as exception:
        y = -1
        z = 10
        result = maps._validate_y(y, z)

    # invalid value

    with raises(InvalidRowError) as exception:
        y = 1024
        z = 10
        result = maps._validate_y(y, z)

    # valid value

    y = 512
    z = 10
    result = maps._validate_y(y, z)
    assert result == y

def test_validate_retina():
    maps = Maps()

    # True

    retina = True
    result = maps._validate_retina(retina)
    assert result == "@2x"

    # False

    retina = False
    result = maps._validate_retina(retina)
    assert result == ""

def test_validate_file_format():
    maps = Maps()

    # invalid value

    with raises(InvalidFileFormatError) as exception:
        file_format = "invalid"
        result = maps._validate_file_format(file_format)
    
    # valid values

    file_formats = [
        "grid.json",
        "mvt",
        "png",
        "png32",
        "png64",
        "png128",
        "png256",
        "jpg70",
        "jpg80",
        "jpg90"
    ]

    for file_format in file_formats:
        result = maps._validate_file_format(file_format)
        assert result == file_format

def test_validate_timestamp():
   maps = Maps()

   # invalid value

   with raises(InvalidPeriodError) as exception:
       timestamp = "invalid"
       result = maps._validate_timestamp(timestamp)

   # valid value

   timestamp = "2018-01-01T00:00:00.000Z"
   result = maps._validate_timestamp(timestamp)
   assert result == timestamp

def test_validate_feature_format():
    maps = Maps()

    # invalid value

    with raises(InvalidFeatureFormatError) as exception:
        feature_format = "invalid"
        result = maps._validate_feature_format(feature_format)
    
    # valid values

    feature_formats = [
        "json",
        "kml"
    ]

    for feature_format in feature_formats:
        result = maps._validate_feature_format(feature_format)
        assert result == feature_format

def test_validate_marker_name():
    maps = Maps()

    # invalid value

    with raises(InvalidMarkerNameError) as exception:
        marker_name = "invalid"
        result = maps._validate_marker_name(marker_name)

    # valid values

    marker_names = [
        "pin-s",
        "pin-l"
    ]

    for marker_name in marker_names:
        result = maps._validate_marker_name(marker_name)
        assert result == marker_name

def test_validate_label():
    maps = Maps()

    # invalid value

    with raises(InvalidLabelError) as exception:
        label = "00"
        result = maps._validate_label(label)

    # invalid value

    with raises(InvalidLabelError) as exception:
        label = "invalid_"
        result = maps._validate_label(label)

    # valid value

    label = "a"
    result = maps._validate_label(label)
    assert result == label

    # valid value

    label = "0"
    result = maps._validate_label(label)
    assert result == label

    # valid value

    label = "99"
    result = maps._validate_label(label)
    assert result == label

    # valid value

    label = "valid"
    result = maps._validate_label(label)
    assert result == label

    # valid value

    label = "valid "
    result = maps._validate_label(label)
    assert result == label

def test_validate_color():
    maps = Maps()

    # invalid value

    with raises(InvalidColorError) as exception:
        color = "invalid"
        result = maps._validate_color(color)

    # valid value

    color = "00f"
    result = maps._validate_color(color)
    assert result == color

    # valid value

    color = "0000ff"
    result = maps._validate_color(color)
    assert result == color

def test_tile_error():
    maps = Maps(access_token="pk.test")

    # invalid number of *args

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets",
        )

    # invalid number of *args

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets",
            0
        )

    # invalid number of *args

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets",
            0,
            0
        )


    # x = None

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets", 
            None, 
            0, 
            0
        )

    # y = None

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets", 
            0, 
            None, 
            0
        )

    # z = None

    with raises(ValidationError) as exception:
        response = maps.tile(
            "mapbox.streets", 
            0, 
            0, 
            None
        )

@activate
def test_tile():
    # tuple

    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0.png?access_token=pk.test",
        match_querystring=True,
        body="0.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        *(0,0,0)
    )

    assert response.status_code == 200

    # individual x, y, and z

    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0.png?access_token=pk.test",
        match_querystring=True,
        body="0.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0
    )

    assert response.status_code == 200

@activate
def test_tile_with_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0@2x.png?access_token=pk.test",
        match_querystring=True,
        body="0@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0, 
        retina=True
    )

    assert response.status_code == 200

@activate
def test_tile_with_different_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0.grid.json?access_token=pk.test",
        match_querystring=True,
        body="0.grid.json",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0, 
        file_format="grid.json"
    )

    assert response.status_code == 200

@activate
def test_tile_with_retina_and_different_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0@2x.grid.json?access_token=pk.test",
        match_querystring=True,
        body="0@2x.grid.json",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0,
        retina=True, 
        file_format="grid.json"
    )

    assert response.status_code == 200

@activate
def test_tile_with_style():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0.png?access_token=pk.test&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body="0.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0,
        style_id="mapbox://styles/mapbox/streets-v10", 
        timestamp="2018-01-01T00:00:00.000Z"
    )

    assert response.status_code == 200

@activate
def test_tile_with_style_and_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0@2x.png?access_token=pk.test&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body="0@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0,
        retina=True,
        style_id="mapbox://styles/mapbox/streets-v10", 
        timestamp="2018-01-01T00:00:00.000Z"
    )

    assert response.status_code == 200

@activate
def test_tile_with_style_and_different_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0.grid.json?access_token=pk.test&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body="0.grid.json",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0,
        file_format="grid.json",
        style_id="mapbox://styles/mapbox/streets-v10", 
        timestamp="2018-01-01T00:00:00.000Z"
    )

    assert response.status_code == 200

@activate
def test_tile_with_style_and_retina_and_different_file_format():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/0/0/0@2x.grid.json?access_token=pk.test&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body="0@2x.grid.json",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.tile(
        "mapbox.streets", 
        0, 
        0, 
        0,
        retina=True,
        file_format="grid.json",
        style_id="mapbox://styles/mapbox/streets-v10", 
        timestamp="2018-01-01T00:00:00.000Z"
    )

    assert response.status_code == 200

@activate
def test_features():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/features.json?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.features(
        "mapbox.streets",
    )

    assert response.status_code == 200

@activate
def test_features_with_different_format():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets/features.kml?access_token=pk.test",
        match_querystring=True,
        body="<xml></xml>",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.features(
        "mapbox.streets",
        feature_format="kml"
    )

    assert response.status_code == 200

@activate
def test_metadata():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets.json?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.metadata(
        "mapbox.streets"
    )

    assert response.status_code == 200

@activate
def test_metadata_with_secure():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/mapbox.streets.json?access_token=pk.test&secure",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.metadata(
        "mapbox.streets",
        secure=True
    )

    assert response.status_code == 200

def test_standalone_marker_error():
    maps = Maps(access_token="pk.test")

    with raises(ValidationError) as exception:
        response = maps.standalone_marker()

@activate
def test_standalone_marker():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s"
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_label():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s-label.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s-label.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        label="label"
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_color():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s+00f.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s-00f.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        color="00f"
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s@2x.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        retina=True
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_label_and_color():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s-label+00f.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s-label+00f.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        label="label",
        color="00f"
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_color_and_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s+00f@2x.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s+00f@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        color="00f",
        retina=True
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_label_and_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s-label@2x.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s-label@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        label="label",
        retina=True
    )

    assert response.status_code == 200

@activate
def test_standalone_marker_with_label_and_color_and_retina():
    add(
        method=GET,
        url="https://api.mapbox.com/v4/marker/pin-s-label+00f@2x.png?access_token=pk.test",
        match_querystring=True,
        body="pin-s-label+00f@2x.png",
        status=200
    )

    maps = Maps(access_token="pk.test")

    response = maps.standalone_marker(
        marker_name="pin-s",
        label="label",
        color="00f",
        retina=True
    )

    assert response.status_code == 200
