from re import (
    compile,
    match
)

from mapbox.errors import (
    ValidationError,
    InvalidZoomError,
    InvalidColumnError,
    InvalidRowError,
    InvalidFileFormatError,
    InvalidPeriodError,
    InvalidFeatureFormatError,
    InvalidMarkerNameError,
    InvalidLabelError,
    InvalidColorError
)

from mapbox.services.base import Service

from dateutil.parser import parse

from uritemplate import URITemplate

class Maps(Service):
    """Access to Maps API V4

    Attributes
    ----------
    api_name : str
        The API's name.

    api_version : str
        The API's version number.

    valid_file_formats : list
        The possible values for file_format.

    valid_feature_formats : list
        The possible values for feature_format.

    valid_marker_names : list
        The possible values for marker_name.

    base_uri : str
        The API's base URI, currently https://api.mapbox.com/v4.
    """

    api_name = "maps"

    api_version = "v4"

    valid_file_formats = [
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

    valid_feature_formats = [
        "json",
        "kml"
    ]

    valid_marker_names = [
        "pin-s",
        "pin-l"
    ]

    @property
    def base_uri(self):
        """Forms base URI."""

        return "https://{}/{}".format(self.host, self.api_version)

    def _validate_z(self, z):
        """Validates z (zoom), raising error if invalid."""

        if (z < 0) or (z > 20):
            raise InvalidZoomError(
                "{} is not a valid value for z (zoom)".format(z)
            )

        return z

    def _validate_x(self, x, z):
        """Validates x (column), raising error if invalid."""

        if (x < 0) or (x > ((2**z) - 1)):
            raise InvalidColumnError(
                "{} is not a valid value for x (column)".format(x)
            )

        return x

    def _validate_y(self, y, z):
        """Validates y (row), raising error if invalid."""

        if (y < 0) or (y > ((2**z) - 1)):
            raise InvalidRowError(
                "{} is not a valid value for y (row)".format(y)
            )

        return y

    def _validate_retina(self, retina):
        """Validates retina."""

        if retina:
            retina = "@2x"
        else:
            retina = ""

        return retina

    def _validate_file_format(self, file_format):
        """Validates file format, raising error if invalid."""

        if file_format not in self.valid_file_formats:
            raise InvalidFileFormatError(
                "{} is not a valid file format".format(file_format)
            )

        return file_format

    def _validate_timestamp(self, timestamp):
        """Validates timestamp, raising error if invalid."""

        try:
            parse(timestamp)
        except:
            raise InvalidPeriodError(
                "{} is not an ISO-formatted string".format(timestamp)
            )

        return timestamp

    def _validate_feature_format(self, feature_format):
        """Validates feature format, raising error if invalid."""

        if feature_format not in self.valid_feature_formats:
            raise InvalidFeatureFormatError(
                "{} is not a valid feature format".format(feature_format)
            )

        return feature_format

    def _validate_marker_name(self, marker_name):
        """Validates marker name, raising error if invalid."""

        if marker_name not in self.valid_marker_names:
            raise InvalidMarkerNameError(
                "{} is not a valid marker name".format(marker_name)
            )

        return marker_name

    def _validate_label(self, label):
        """Validates label, raising error if invalid."""

        letter_pattern = compile("^[a-z]{1}$")
        number_pattern = compile("^[0]{1}$|^[1-9]{1,2}$")
        icon_pattern = compile("^[a-zA-Z ]{1,}$")

        if not match(letter_pattern, label)\
            and not match(number_pattern, label)\
                and not match(icon_pattern, label):
                    raise InvalidLabelError(
                        "{} is not a valid label".format(label)
                    )

        return label

    def _validate_color(self, color):
        """Validates color, raising error if invalid."""

        three_digit_pattern = compile("^[a-f0-9]{3}$")
        six_digit_pattern = compile("^[a-f0-9]{6}$")

        if not match(three_digit_pattern, color)\
            and not match(six_digit_pattern, color):
                raise InvalidColorError(
                    "{} is not a valid color".format(color)
                )

        return color

    def tile(self, map_id, x, y, z, retina=False, 
             file_format="png", style_id=None, timestamp=None):

        """Returns an image tile, vector tile, or UTFGrid
        in the specified file format.

        Parameters
        ----------
        map_id : str
            The tile's unique identifier in the format username.id.

        x : int
            The tile's column, where 0 is the minimum value
            and ((2**z) - 1) is the maximum value.

        y : int
            The tile's row, where 0 is the minimum value
            and ((2**z) - 1) is the maximum value.

        z : int
            The tile's zoom level, where 0 is the minimum value
            and 20 is the maximum value.

        retina : bool, optional
            The tile's scale, where True indicates Retina scale
            (double scale) and False indicates regular scale.  

            The default value is false.
       
        file_format : str, optional
            The tile's file format.  

            The default value is png.

        style_id : str, optional
            The tile's style id.  

            style_id must be used together with timestamp.

        timestamp : str, optional
            The style id's ISO-formatted timestamp, found by 
            accessing the "modified" property of a style object.

            timestamp must be used together with style_id.

        Returns
        -------
        request.Response
            The response object with a tile in the specified format.
        """

        # Check x, y, and z.

        if x is None or y is None or z is None:
            raise ValidationError(
                "x, y, and z must be not be None"
            )

        # Validate x, y, z, retina, and file_format.

        x = self._validate_x(x, z)
        y = self._validate_y(y, z)
        z = self._validate_z(z)
        retina = self._validate_retina(retina)
        file_format = self._validate_file_format(file_format)

        # Create dict to assist in building URI resource path.

        path_values = dict(
            map_id=map_id,
            x=str(x),
            y=str(y),
            z=str(z)
        )

        # Start building URI resource path.

        path_part = "/{map_id}/{z}/{x}/{y}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Finish building URI resource path.
        # As in static.py, this two-part process avoids 
        # undesired escaping of "@" in "@2x."

        path_part = "{}.{}".format(retina, file_format)
        uri += path_part

        # Validate timestamp and build URI query parameters.
 
        query_parameters = dict()

        if style_id is not None and timestamp is not None:
            timestamp = self._validate_timestamp(timestamp)
            style = "{}@{}".format(style_id, timestamp)
            query_parameters["style"] = style

        # Send HTTP GET request.

        response = self.session.get(uri, params=query_parameters)
        self.handle_http_error(response)

        return response

    def features(self, map_id, feature_format="json"):
        """Returns vector features from Mapbox Editor projects
        as GeoJSON or KML.

        Parameters
        ----------
        map_id : str
            The map's unique identifier in the format username.id.

        feature_format : str, optional
            The vector's feature format.

            The default value is json.

        Returns
        -------
        request.Response
            The response object with vector features.
        """

        # Validate feature_format.

        feature_format = self._validate_feature_format(feature_format)
   
        # Create dict to assist in building URI resource path.

        path_values = dict(
            map_id=map_id,
            feature_format=feature_format
        )

        # Build URI resource path.

        path_part = "/{map_id}/features.{feature_format}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response

    def metadata(self, map_id, secure=False):
        """Returns TileJSON metadata for a tileset.

        Parameters
        ----------
        map_id : str
            The map's unique identifier in the format username.id.

        secure : bool, optional
            The representation of the requested resources, 
            where True indicates representation as HTTPS endpoints.

            The default value is False.

        Returns
        -------
        request.Response
            The response object with TileJSON metadata for the 
            specified tileset.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            map_id=map_id
        )

        # Build URI resource path.

        path_part = "/{map_id}.json"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Build URI query parameters.

        query_parameters = dict()

        if secure:
            query_parameters["secure"] = ""

        # Send HTTP GET request.

        response = self.session.get(uri, params=query_parameters)
        self.handle_http_error(response)

        return response

    def marker(self, marker_name=None, label=None, 
               color=None, retina=False):
        """Returns a single marker image without any
           background map.

        Parameters
        ----------
        marker_name : str
            The marker's shape and size.

        label : str, optional
            The marker's alphanumeric label.

            Options are a through z, 0 through 99, or the
            name of a valid Maki icon.

        color : str, optional
            The marker's color.

            Options are three- or six-digit hexadecimal
            color codes.

        retina : bool, optional
            The marker's scale, where True indicates Retina scale
            (double scale) and False indicates regular scale.  

            The default value is false.
 
        Returns
        -------
        request.Response
            The response object with the specified marker.
        """

        # Check for marker_name.

        if marker_name is None:
            raise ValidationError(
                "marker_name is a required argument"
            )

        # Validate marker_name and retina.

        marker_name = self._validate_marker_name(marker_name)
        retina = self._validate_retina(retina)

        # Create dict and start building URI resource path.

        path_values = dict(
            marker_name=marker_name
        )

        path_part = "/marker/{marker_name}"

        # Validate label, update dict,
        # and continue building URI resource path.

        if label is not None:
            label = self._validate_label(label)
            path_values["label"] = label
            path_part += "-{label}"

        # Validate color, update dict,
        # and continue building URI resource path.

        if color is not None:
            color = self._validate_color(color)
            path_values["color"] = color
            path_part += "+{color}"

        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Finish building URI resource path.

        path_part = "{}.png".format(retina)
        uri += path_part

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response
