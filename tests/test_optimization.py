from mapbox.errors import (
    InvalidParameterError,
    InvalidProfileError,
    ValidationError
)

from mapbox.services.optimization import Optimization

from pytest import (
    mark,
    raises
)

from responses import (
    activate,
    add,
    GET
)


ACCESS_TOKEN = "pk.test"

FEATURES = [
    {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [
                0.0,
                0.0
            ]
        }
    }, 
    {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [
                1.0,
                1.0
            ]
        }
    }
]


COORDINATES = "0.0,0.0;1.0,1.0"


def test_object_properties():
    optimization = Optimization()

    assert optimization.api_name
    assert optimization.api_version
    assert optimization.valid_profiles
    assert optimization.valid_geometries
    assert optimization.valid_overviews
    assert optimization.valid_annotations
    assert optimization.valid_sources
    assert optimization.valid_destinations


def test_validate_profile_invalid():
    optimization = Optimization()

    with raises(InvalidProfileError) as exception:
        profile = "invalid"
        result = optimization._validate_profile(profile)


@mark.parametrize("profile", ["mapbox/cycling", "mapbox/driving", "mapbox/walking"])
def test_validate_profile_valid(profile):
    optimization = Optimization()
    result = optimization._validate_profile(profile)
    assert result == profile   


def test_validate_geometry_invalid():
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        geometry = "invalid"
        result = optimization._validate_geometry(geometry)


@mark.parametrize("geometry", ["geojson", "polyline", "polyline6"])
def test_validate_geometry_valid(geometry):
    optimization = Optimization()
    result = optimization._validate_geometry(geometry)
    assert result == geometry


def test_validate_overview_invalid():
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        overview = "invalid"
        result = optimization._validate_overview(overview)


@mark.parametrize("overview", ["full", "simplified", False])
def test_validate_overview_valid(overview):
    optimization = Optimization()
    result = optimization._validate_overview(overview)
    assert result == overview


def test_validate_source_invalid():
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        source = "invalid"
        result = optimization._validate_source(source)


@mark.parametrize("source", ["any", "first"])
def test_validate_source_valid(source):
    optimization = Optimization()
    result = optimization._validate_source(source)
    assert result == source


def test_validate_destination_invalid():
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        destination = "invalid"
        result = optimization._validate_destination(destination)


@mark.parametrize("destination", ["any", "last"])
def test_validate_destination_valid(destination):
    optimization = Optimization()
    result = optimization._validate_destination(destination)
    assert result == destination


# too many distribution pairs
# too few values in each pair
# too many values in each pair
# values are the same
# first value is not a valid index
# second value is not a valid index

@mark.parametrize(
    "distributions", 
    [
        [[0, 1], [0, 1], [0, 1]],
        [[0], [0]],
        [[0, 1, 0], [0, 1, 0]],
        [[0, 0], [0, 0]],
        [[100, 0], [0, 0]],
        [[0, 100], [0, 0]]
    ]
)
def test_validate_distributions_invalid(distributions):
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        result = optimization._validate_distributions(distributions, COORDINATES)


def test_validate_distributions_valid():
    optimization = Optimization()
    distributions = [[0, 1], [0, 1]]
    result = optimization._validate_distributions(distributions, COORDINATES)
    assert result == "0,1;0,1"


def test_validate_distributions_none():
    optimization = Optimization()
    distributions = None
    result = optimization._validate_distributions(distributions, COORDINATES)
    assert result == distributions


def test_validate_annotations_invalid():
    optimization = Optimization()

    with raises(InvalidParameterError) as exception:
        annotation = ["invalid"]
        result = optimization._validate_annotations(annotation)


@mark.parametrize(
    "annotations", 
    [
        ["distance"], 
        ["duration"], 
        ["speed"],
        ["distance", "duration"],
        ["distance", "speed"],
        ["duration", "speed"],
        ["distance", "duration", "speed"]
    ]
)
def test_validate_annotations_valid(annotations):
    optimization = Optimization()
    result = optimization._validate_annotations(annotations)
    assert result == ",".join(annotations)


def test_validate_annotations_none():
    optimization = Optimization()
    annotations = None
    result = optimization._validate_annotations(annotations)
    assert result == annotations


def test_route_error_no_source():
    optimization = Optimization(access_token=ACCESS_TOKEN)

    with raises(ValidationError) as exception:
        response = optimization.route(
            FEATURES,
            roundtrip=False,
            destination="any"
        )


def test_route_error_no_destination():
    optimization = Optimization(access_token=ACCESS_TOKEN)

    with raises(ValidationError) as exception:
        response = optimization.route(
            FEATURES,
            roundtrip=False,
            source="any"
      )


def test_route_error_no_source_no_destination():
    optimization = Optimization(access_token=ACCESS_TOKEN)

    with raises(ValidationError) as exception:
        response = optimization.route(
            FEATURES,
            roundtrip=False
        )


@activate
def test_route():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)
    response = optimization.route(FEATURES)
    assert response.status_code == 200


@activate
def test_route_with_profile():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling"
    )

    assert response.status_code == 200


@activate
def test_route_with_geometries():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        geometries="geojson"
    )

    assert response.status_code == 200


@activate
def test_route_with_overview():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&overview=false",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        overview=False
    )

    assert response.status_code == 200


@activate
def test_route_with_steps():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&steps=false",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        steps=False
    )

    assert response.status_code == 200


@activate
def test_route_with_waypoint_snapping():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        waypoint_snapping=[
            (1, 1, 1), 
            (1, 1, 1)
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        annotations=[
            "distance", 
            "duration", 
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/driving" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_geometries():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_overview():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&overview=full",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        overview="full"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_steps():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&steps=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        steps=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_waypoint_snapping():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_overview():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_steps():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&steps=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        steps=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_waypoint_snapping():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_steps():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_waypoint_snapping():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ]
    )

    assert response.status_code == 200



@activate
def test_route_with_profile_geometries_overview_and_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_waypoint_snapping():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_roundtrip():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        roundtrip=True
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1)
        ],
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_and_source():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_and_destination():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        roundtrip=True,
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        source="any",
        destination="any"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_and_distributions():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" +
            "&distributions=0,1",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        distributions=[
            [0, 1]
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_distributions_and_annotations():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" +
            "&distributions=0,1" +
            "&annotations=distance,duration,speed",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        distributions=[
            [0, 1]
        ],
        annotations=[
            "distance",
            "duration",
            "speed"
        ]
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_distributions_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" + 
            "&distributions=0,1" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        distributions=[
            [0, 1]
        ],
        language="en"
    )

    assert response.status_code == 200


@activate
def test_route_with_profile_geometries_overview_steps_waypoint_snapping_roundtrip_source_destination_distributions_annotations_and_language():
    add(
        url="https://api.mapbox.com" +
            "/optimized-trips/v1" +
            "/mapbox/cycling" + 
            "/0.0%2C0.0%3B1.0%2C1.0" +
            "?access_token=pk.test" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1" +
            "&roundtrip=true" +
            "&source=any" +
            "&destination=any" +
            "&distributions=0,1" +
            "&annotations=distance,duration,speed" +
            "&language=en",
        method=GET,
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    optimization = Optimization(access_token=ACCESS_TOKEN)

    response = optimization.route(
        FEATURES,
        profile="mapbox/cycling",
        geometries="geojson",
        overview="full",
        steps=True,
        waypoint_snapping=[
            (1, 1, 1),
            (1, 1, 1) 
        ],
        roundtrip=True,
        source="any",
        destination="any",
        distributions=[
            [0, 1]
        ],
        annotations=[
            "distance",
            "duration",
            "speed"
        ],
        language="en"
    )

    assert response.status_code == 200
