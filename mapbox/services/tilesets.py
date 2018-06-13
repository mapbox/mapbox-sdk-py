from mapbox.errors import (
    InvalidTilesetTypeError,
    InvalidVisibilityError,
    InvalidSortbyError,
    InvalidLimitError
)

from mapbox.services.base import Service

from uritemplate import URITemplate

class Tilesets(Service):
    """Access to Tilesets API V1

    Attributes
    ----------
    api_name : str
        The API's name.

    api_version : str
        The API's version number.

    valid_tileset_types : list
        The possible values for tileset_type.

    valid_visibilities : list
        The possible values for visibility.

    valid_sortbys : list
        The possible values for sortby.

    base_uri : str
         The API's base URI, currently https://api.mapbox.com/tilesets/v1
    """

    api_name = "tilesets"

    api_version = "v1"

    valid_tileset_types = [
        "raster",
        "vector"
    ]

    valid_visibilities = [
        "private",
        "public"
    ]

    valid_sortbys = [
        "created",
        "modified"
    ]

    @property
    def base_uri(self):
        """Forms base URI."""

        return "https://{}/{}/{}".format(
            self.host,
            self.api_name,
            self.api_version
        ) 

    def _validate_tileset_type(self, tileset_type):
        """Validates tileset type, raising error if invalid."""

        if tileset_type not in self.valid_tileset_types:
            raise InvalidTilesetTypeError(
                "{} is not a valid tileset type".format(tileset_type)
            )

        return tileset_type

    def _validate_visibility(self, visibility):
        """Validates visibility, raising error if invalid."""

        if visibility not in self.valid_visibilities:
            raise InvalidVisibilityError(
                "{} is not a valid value for visibility".format(visibility)
            )

        return visibility

    def _validate_sortby(self, sortby):
        """Validates sortby, raising error if invalid."""

        if sortby not in self.valid_sortbys:
            raise InvalidSortbyError(
                "{} is not a valid value for sortby".format(sortby)
            )

        return sortby

    def _validate_limit(self, limit):
        """Validates limit, raising error if invalid."""

        if (limit < 1) or (limit > 500):
            raise InvalidLimitError(
                "{} is not a valid value for limit".format(limit)
            )

        return limit

    def tilesets(self, tileset_type=None, visibility=None, 
                 sortby=None, limit=None):
        """Lists all tilesets for an account.

        tileset_type : str, optional
            Filter results by tileset type.

            Valid values are raster or vector.

        visibility : str, optional
            Filter results by visibility.

            Valid values are private or public.

            Private tilesets require an access token
            belonging to the owner, while public
            tilesets may be requested with an access
            token belonging to any user.

        sortby : str, optional
            Sort results by timestamp.

            Valid values are created or modified

        limit : int, optional
            The maximum number of objects to return
            (pagination), where 1 is the minimum value
            and 500 is the maxium value.

            The default value is 100.

        Returns
        -------
        request.Response
            The response object with a tileset object.
        """

        # Build URI resource path.

        path_part = "/{username}"
        path_values = dict(username=self.username)
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Validate tileset_type, visibility, sortby, and limit
        # and build URI query parameters.

        query_parameters = dict()

        if tileset_type:
            tileset_type = self._validate_tileset_type(tileset_type)
            query_parameters["type"] = tileset_type

        if visibility:
            visibility = self._validate_visibility(visibility)
            query_parameters["visibility"] = visibility

        if sortby:
            sortby = self._validate_sortby(sortby)
            query_parameters["sortby"] = sortby

        if limit:
            limit = self._validate_limit(limit)
            query_parameters["limit"] = str(limit)

        # Send HTTP GET request.

        response = self.session.get(uri, params=query_parameters)

        return response
