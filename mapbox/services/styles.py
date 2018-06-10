from json import loads

from mapbox.errors import (
    InvalidFileFormatError,
    InvalidStartError
)

from mapbox.services.base import Service

from uritemplate import URITemplate


class Styles(Service):
    """Access to Styles API V1

    Attributes
    ----------
    api_name : str
        The API's name.

    api_version : str
        The API's version number

    valid_file_formats : list
        The possible values for file_format.

    base_uri : str
        The API's base URI, currently 
        https://api.mapbox.com/styles/v1.
    """

    api_name = "styles"

    api_version = "v1"

    valid_file_formats = [
        "json",
        "png"
    ]

    @property
    def base_uri(self):
        """Forms base URI."""

        return "https://{}/{}/{}".format(
            self.host, 
            self.api_name, 
            self.api_version
        )

    def _validate_start(self, start):
        """Validates start of font glyph range, raising error if invalid."""

        # 0 is a valid value.
        # Return 0 to avoid ZeroDivisionError.

        if start == 0:
            return start

        # Start must be a multiple of 256 between 0 and 65280.

        if (start < 0)\
            or (start > 65280)\
                or (start % 256 != 0):
                    raise InvalidStartError(
                        "{} is not a valid value for start".format(start)
                    )

        return start

    def _validate_retina(self, retina):
        """Validates retina."""

        if retina:
            retina = "@2x"
        else:
            retina = ""

        return retina

    def _validate_file_format(self, file_format):
        """Validates file format, raising error if invalid."""

        if file_format is not None\
            and file_format not in self.valid_file_formats:
                raise InvalidFileFormatError(
                    "{} is not a valid file format".format(file_format)
                )

        return file_format

    def style(self, style_id):
        """Returns a style as a JSON document.

        Parameters
        ----------
        style_id : str
            The style id.

        Returns
        -------
        request.Response
            The response object with the requested 
            style object.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            style_id=style_id
        )

        # Build URI resource path.

        path_part = "/{username}/{style_id}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response 

    def list_styles(self):
        """Returns a list of styles.  This method returns 
        style metadata rather than style objects.

        Returns
        -------
        request.Response
            The response object with the requested 
            style metadata.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username
        )

        # Build URI resource path.

        path_part = "/{username}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response 

    def create_style(self, style_object):
        """Creates a style.  

        style_object : dict or file
            The style object.

            The style object must be both valid JSON and 
            aligned to the Mapbox Style Specification.

            Validation occurs on the server.  Invalid styles 
            will produce a descriptive validation error.

        Returns
        -------
        request.Response
            The response object with the properties of
            the created style object.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username
        )

        # Build URI resource path.

        path_part = "/{username}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Set header.

        headers = {
            "Content-Type": "application/json"
        }

        # Get style object.

        if not isinstance(style_object, dict):
            with open(style_object, "r") as file:
                json = file.read()
                json = loads(json)
        else:
            json = style_object

        # Send HTTP POST request.

        response = self.session.post(uri, headers=headers, json=json)
        self.handle_http_error(response)

        return response

    def update_style(self, style_object):
        """Updates a style.  

        style_object : dict or file
            The style object.

            The style object must be both valid JSON and 
            aligned to the Mapbox Style Specification.

            Most validation occurs on the server.  Local
            validation is trivial, involving only the 
            removal of the "created" and "modified" keys 
            from the style object.

            Invalid styles will produce a descriptive 
            validation error.

        Returns
        -------
        request.Response
            The response object with the properties of
            the updated style object.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username
        )

        # Build URI resource path.

        path_part = "/{username}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Set header.

        headers = {
            "Content-Type": "application/json"
        }

        # Get style object.

        if not isinstance(style_object, dict):
            with open(style_object, "r") as file:
                json = file.read()
                json = loads(json)
        else:
            json = style_object

        # Remove invalid keys from style object.

        invalid_keys = [
            "created",
            "modified"
        ]

        for key in invalid_keys:
            if key in json:
                json.pop(key)

        # Send HTTP PATCH request.

        response = self.session.patch(uri, headers=headers, json=json)
        self.handle_http_error(response)

        return response

    def delete_style(self, style_id):
        """Deletes a style and any associated sprites.

        Parameters
        ----------
        style_id : str
            The style id.

        Returns
        -------
        HTTP status code
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            style_id=style_id
        )

        # Build URI resource path.

        path_part = "/{username}/{style_id}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP DELETE request.

        response = self.session.delete(uri)
        self.handle_http_error(response)

        return response

    def font_glyphs(self, fonts, start):
        """Returns a font glyph range as a protocol-buffer-encoded
           signed distance field.

        Parameters
        ----------
        fonts : list
            The fonts' names.

        start : int
             The range's start, where valid values are multiples
             of 256 between 0 and 65280.

        Returns
        -------
        request.Response
            The response object with the protocol-buffer-encoded
            font glyph range.
        """

        # Validate start.

        start = self._validate_start(int(start))

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            fonts=",".join(fonts),
            start=start,
            end=start + 255
        )

        # Build URI resource path.
        # The base URI for this method differs from that used 
        # by other methods of the Styles class.

        path_part = "/fonts/v1/{username}/{fonts}/{start}-{end}.pbf"
        uri = URITemplate("https://" + self.host + path_part).expand(**path_values)

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response  

    def sprite(self, style_id, sprite,
               retina=False, file_format=None):
        """Returns a sprite image or JSON document.

        Parameters
        ----------
        style_id : str
            The style id to which the sprite 
            belongs.

        sprite : str
            The name of the sprite.
 
        retina : bool, optional
            The image's scale, where True indicates 
            Retina scale (double scale) and False 
            indicates regular scale.  

            The default value is False.

        file_format : str, optional
            The sprite's file format.

            If None, the default value is json.

        Returns
        -------
        request.Response
            The request object with the requested sprite 
            image or JSON document. 
        """

        # Validate retina and file_format

        retina = self._validate_retina(retina)
        file_format = self._validate_file_format(file_format)

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            style_id=style_id,
            sprite=sprite
        )

        # Start building URI resource path.

        path_part = "/{username}/{style_id}/{sprite}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Continue building URI resource path.
        # As in static.py, this two-part process avoids
        # undesired escaping of "@" in "@2x."

        path_part = "{}".format(retina)
        uri += path_part

        # Finish building URI resource path.

        if file_format is not None:
            path_part = ".{}".format(file_format)
            uri += path_part

        # Send HTTP GET request.

        response = self.session.get(uri)
        self.handle_http_error(response)

        return response

    def add_image(self, style_id, sprite, icon_name):
        """Adds a new image to an existing sprite.

        Parameters
        ----------
        style_id : str
            The style id to which the sprite 
            belongs.

        sprite : str
            The name of the sprite.

        icon_name : str
            The name of the image to add.

            This should be a file with raw SVG data.
            
        Returns
        -------
        request.Response
            The request object with the propertes of
            the added image.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            style_id=style_id,
            sprite=sprite,
            icon_name=icon_name
        )

        # Build URI resource path.

        path_part = "/{username}/{style_id}/{sprite}/{icon_name}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP PUT request.

        with open(icon_name, "rb") as data:
            response = self.session.put(uri, data=data) 
            self.handle_http_error(response)

            return response

    def delete_image(self, style_id, sprite, icon_name):
        """Deletes an image from an existing sprite.

        Parameters
        ----------
        style_id : str
            The style id to which the sprite 
            belongs.

        sprite : str
            The name of the sprite.

        icon_name : str
            The name of the image to delete.
            
        Returns
        -------
        request.Response
            The request object with the propertes of
            the deleted image.
        """

        # Create dict to assist in building URI resource path.

        path_values = dict(
            username=self.username,
            style_id=style_id,
            sprite=sprite,
            icon_name=icon_name
        )

        # Build URI resource path.

        path_part = "/{username}/{style_id}/{sprite}/{icon_name}"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Send HTTP DELETE request.

        response = self.session.delete(uri) 
        self.handle_http_error(response)

        return response
