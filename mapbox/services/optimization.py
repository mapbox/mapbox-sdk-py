from mapbox.encoding import (
    encode_bearing,
    encode_waypoints,
    validate_radius,
    validate_snapping
)

from mapbox.errors import (
    InvalidParameterError,
    InvalidProfileError,
    ValidationError
)

from mapbox.services.base import Service

import polyline

from uritemplate import URITemplate


class Optimization(Service):
    """Access to Optimization API V1

    Attributes
    ----------
    api_name : str
        The API's name.

    api_version : str
        The API's version number.

    valid_profiles : list
        The possible values for profile.

    valid_geometries : list
        The possible values for geometries.

    valid_overviews : list
        The possible values for overview.

    valid_sources : list
        The possible valies for source.

    valid_destinations : list
        The possible values for destination.

    valid_annotations : list
        The possible values for annotations.

    base_uri : str
        The API's base URI, currently 
        https://api.mapbox.com/optimized-trips/v1.
    """

    api_name = "optimized-trips"

    api_version = "v1"

    valid_profiles = [
        "mapbox/cycling",
        "mapbox/driving",
        "mapbox/walking"
    ]

    valid_geometries = [
        "geojson",
        "polyline",
        "polyline6"
    ]

    valid_overviews = [
        "full",
        "simplified",
        False
    ]

    valid_sources = [
        "any",
        "first"
    ]

    valid_destinations = [
        "any",
        "last"
    ]

    valid_annotations = [
        "distance",
        "duration",
        "speed"
    ]

    @property
    def base_uri(self):
        """Forms base URI."""

        return "https://{}/{}/{}".format(
            self.host, 
            self.api_name, 
            self.api_version
        )

    def _validate_profile(self, profile):
        """Validates profile, raising error if invalid."""

        if profile not in self.valid_profiles:
            raise InvalidProfileError(
                "{} is not a valid profile".format(profile)
            )

        return profile

    def _validate_geometry(self, geometry):
        """Validates geometry, raising error if invalid."""

        if geometry is not None\
            and geometry not in self.valid_geometries:
                raise InvalidParameterError(
                    "{} is not a valid geometry format".format(geometry)
                )

        return geometry  

    def _validate_overview(self, overview):
        """Validates overview, raising error if invalid."""

        if overview is not None\
            and overview not in self.valid_overviews:
                raise InvalidParameterError(
                    "{} is not a valid geometry overview type".format(overview)
                )

        return overview

    def _validate_source(self, source):
        """Validates source, raising error if invalid."""

        if source is not None\
            and source not in self.valid_sources:
                raise InvalidParameterError(
                    "{} is not a valid source".format(source)
                )

        return source

    def _validate_destination(self, destination):
        """Validates destination, raising error if invalid."""

        if destination is not None\
            and destination not in self.valid_destinations:
                raise InvalidParameterError(
                    "{} is not a valid destination".format(destination)
                )

        return destination

    def _validate_distributions(self, distributions, coordinates):
        """Validates distribution pairs, raising error if invalid."""

        if distributions is None:
            return None

        results = []

        coordinates = coordinates.split(";")

        # The number of distribution pairs must be less
        # than or equal to the number of coordinate pairs.

        if len(distributions) > len(coordinates):
            raise InvalidParameterError(
                "{} are not valid distributions".format(str(distributions))
            )

        # There must be two values in each distribution pair,
        # a pick-up and a drop-off.
 
        for distribution in distributions:
          if len(distribution) != 2:
              raise InvalidParameterError(
                  "{} is not a valid distribution".format(str(distribution))
              )

        # The values for pick-up and drop-off must not be 
        # the same. 

          pick_up, drop_off = distribution
          
          if pick_up == drop_off:
              raise InvalidParameterError(
                  "{} is not a valid distribution".format(str(distribution))
              )

        # The values for pick-up and drop-off must correspond
        # to indices of the list of coordinate pairs.

          try:
              pick_up = int(pick_up)
              coordinates[pick_up]
          except IndexError as exception:
              raise InvalidParameterError(
                  "{} is not a valid distribution".format(str(distribution))
              )

          try:
              drop_off = int(drop_off)
              coordinates[drop_off]
          except IndexError as exception:
              raise InvalidParameterError(
                  "{} is not a valid distribution".format(str(distribution))
              )

          result = "{},{}".format(pick_up, drop_off)
          results.append(result)

        return ";".join(results)

    def _validate_annotations(self, annotations):
        """Validates annotations, raising error if invalid."""

        if annotations is None:
            return None

        for annotation in annotations:
            if annotation not in self.valid_annotations:
                raise InvalidParameterError(
                    "{} is not a valid annotation".format(annotation)
                )

        return ",".join(annotations)

    # Copied from directions.py and modified.

    def _geojson(self, data, geometry_format=None):
        """Converts JSON to GeoJSON in response object."""
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": []
        }

        for route in data["trips"]:
            if geometry_format == "geojson":
                geometry = route["geometry"]
 
            else:
                geometry = {
                    "type": "LineString",
                    "coordinates": polyline.decode(
                        route["geometry"]
                    )
                }

            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "distance": route["distance"],
                    "duration": route["duration"]
                }
            }

            feature_collection["features"].append(feature)

        return feature_collection
    
    def route(self, features, profile="mapbox/driving",
              geometries=None, overview=None, steps=None, 
              waypoint_snapping=None, roundtrip=None, source=None, 
              destination=None, distributions=None, annotations=None, 
              language=None):
        
        """The Optimization API returns a duration-optimized route
        between the input coordinates.

        Parameters
        ----------
        features : iterable
            The collection of GeoJSON features used 
            to define the returned route.

        profile : str
            The routing profile.

            The default value is mapbox/driving.

        geometries : str, optional
            The format of the returned geometries.

            If None, the default value is polyline.

        overview : str, optional
            The type of the returned overview geometry.

            If None, the default value is simplified.

        steps : bool, optional
             Whether to return steps and turn-by-turn 
             instructions.

             If None, the default value is False.

        waypoint_snapping : list, optional
            The bearings and radiuses of waypoints in the
            returned route.

        roundtrip : bool, optional
            Whether the returned route is roundtrip 
            (the trip ends at the first location).

            If None, the default value is True.

        source : str, optional
            The first location of the returned route.

            If None, the default value is any.

        destination : str, optional
            The last location of the returned route.

            If None, the default value is any.

        distributions : list, optional
            The pick-up and drop-off locations along the 
            returned route.

        annotations : list, optional
            The metadata provided with the returned route.

        language : str, optional
            The language of the returned step-by-step 
            instructions.

            If None, the default value is en.

        Returns
        -------
        request.Response
            The respone object with the optimization object.
        """

        # Check roundtrip, source, and destination.

        if roundtrip == False\
            and ((source is None) or (destination is None)):
                raise ValidationError(
                    "Source and destination are required if roundtrip is False"
                )

        # Create dict to assist in building URI resource path.

        path_values = dict()

        # Validate profile and update dict.

        profile = self._validate_profile(profile)
        name, mode = profile.split("/")
        path_values["name"] = name
        path_values["mode"] = mode

        # Obtain coordinates and update dict.

        coordinates = encode_waypoints(
            features, 
            precision=6, 
            min_limit=2, 
            max_limit=12
        )

        path_values["coordinates"] = coordinates

        # Build URI resource path.

        path_part = "/{name}/{mode}/{coordinates}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values) 

        # Build URI query parameters.

        query_parameters = dict()

        if geometries is not None:
            geometries = self._validate_geometry(geometries)
            query_parameters["geometries"] = geometries

        if overview is not None:
            overview = self._validate_overview(overview)
            query_parameters["overview"] = "false" if overview is False else overview

        if steps is not None:
            query_parameters["steps"] = "true" if steps is True else "false"

        if waypoint_snapping is not None:
            bearings, radiuses = validate_snapping(waypoint_snapping, features)
        else:
            bearings = None
            radiuses = None

        if bearings is not None:
            bearings = ";".join(encode_bearing(bearing) for bearing in bearings)
            query_parameters["bearings"] = bearings

        if radiuses is not None:
            radiuses = ";".join(str(radius) for radius in radiuses)
            query_parameters["radiuses"] = radiuses

        if roundtrip is not None:
            query_parameters["roundtrip"] = "true" if roundtrip is True else "false"
 
        if source is not None:
            source = self._validate_source(source)
            query_parameters["source"] = source

        if destination is not None:
            destination = self._validate_destination(destination)
            query_parameters["destination"] = destination

        if distributions is not None:
            distributions = self._validate_distributions(distributions, coordinates)
            query_parameters["distributions"] = distributions
  
        if annotations is not None:
            annotations = self._validate_annotations(annotations)
            query_parameters["annotations"] = annotations

        if language is not None:
            query_parameters["language"] = language
        
        # Send HTTP GET request.

        response = self.session.get(uri, params=query_parameters)
        self.handle_http_error(response)

        # Add geojson method to response object.

        def geojson():
            return self._geojson(
                response.json(),
                geometry_format=geometries
            )

        response.geojson = geojson
        
        return response
