"""The Tilequery class provides access to Mapbox's Tilequery API."""

from mapbox.errors import (InvalidCoordError, InvalidParameterError)

from mapbox.services.base import Service

from uritemplate import URITemplate


class Tilequery(Service):
    """Access to Tilequery API V4

    Attributes
    ----------
    api_name : str
        The API's name.

    api_version : str
        The API's version number.

    valid_geometries : list
        The possible values for geometry.

    base_uri : str
        The API's base URI, currently https://api.mapbox.com/v4.
    """

    api_name = "tilequery"

    api_version = "v4"

    valid_geometries = ["linestring", "point", "polygon"]

    @property
    def base_uri(self):
        """Forms base URI."""

        return "https://{}/{}".format(self.host, self.api_version)

    def _validate_lon(self, lon):
        """Validates longitude, raising error if invalid."""

        if (lon < -180) or (lon > 180):
            raise InvalidCoordError("Longitude must be between -180 and 180")

        return lon

    def _validate_lat(self, lat):
        """Validates latitude, raising error if invalid."""

        if (lat < -85.0511) or (lat > 85.0511):
            raise InvalidCoordError("Latitude must be between -85.0511 and 85.0511")

        return lat

    def _validate_radius(self, radius):
        """Validates radius, raising error if invalid."""

        if radius is not None and radius < 0:
            raise InvalidParameterError("Radius must be greater than or equal to 0")

        return radius

    def _validate_limit(self, limit):
        """Validates limit, raising error if invalid."""

        if limit is not None and ((limit < 1) or (limit > 50)):
            raise InvalidParameterError("Limit must be between 1 and 50")

        return limit

    def _validate_geometry(self, geometry):
        """Validates geometry, raising error if invalid."""

        if geometry is not None and geometry not in self.valid_geometries:
            raise InvalidParameterError("{} is not a valid geometry".format(geometry))

        return geometry

    def tilequery(
        self,
        map_id,
        lon=None,
        lat=None,
        radius=None,
        limit=None,
        dedupe=None,
        geometry=None,
        layers=None,
    ):

        """Returns data about specific features
        from a vector tileset.

        Parameters
        ----------
        map_id : str or list
            The tileset's unique identifier in the
            format username.id.

            map_id may be either a str with one value
            or a list with multiple values.

        lon : float
            The longitude to query, where -180
            is the minimum value and 180 is the
            maximum value.

        lat : float
            The latitude to query, where -85.0511
            is the minimum value and 85.0511 is the
            maximum value.

        radius : int, optional
            The approximate distance in meters to
            query, where 0 is the minimum value.
            (There is no maximum value.)

            If None, the default value is 0.

        limit : int, optional
            The number of features to return, where
            1 is the minimum value and 50 is the
            maximum value.

            If None, the default value is 5.

        dedupe : bool, optional
            Whether to remove duplicate results.

            If None, the default value is True.

        geometry : str, optional
            The geometry type to query.

        layers : list, optional
            The list of layers to query.

            If a specified layer does not exist,
            then the Tilequery API will skip it.
            If no layers exist, then the API will
            return an empty GeoJSON FeatureCollection.

        Returns
        -------
        request.Response
            The response object with a GeoJSON
            FeatureCollection of features at or near
            the specified longitude and latitude.
        """

        # If map_id is a list, then convert it to a str
        # of comma-separated values.

        if isinstance(map_id, list):
            map_id = ",".join(map_id)

        # Validate lon and lat.

        lon = self._validate_lon(lon)
        lat = self._validate_lat(lat)

        # Create dict to assist in building URI resource path.

        path_values = dict(
            api_name=self.api_name, lon=lon, lat=lat
        )

        # Build URI resource path.

        path_part = "/" + map_id + "/{api_name}/{lon},{lat}.json"
        uri = URITemplate(self.base_uri + path_part).expand(**path_values)

        # Build URI query_parameters.

        query_parameters = dict()

        if radius is not None:
            radius = self._validate_radius(radius)
            query_parameters["radius"] = radius

        if limit is not None:
            limit = self._validate_limit(limit)
            query_parameters["limit"] = limit

        if dedupe is not None:
            query_parameters["dedupe"] = "true" if True else "false"

        if geometry is not None:
            geometry = self._validate_geometry(geometry)
            query_parameters["geometry"] = geometry

        if layers is not None:
            query_parameters["layers"] = ",".join(layers)

        # Send HTTP GET request.

        response = self.session.get(uri, params=query_parameters)
        self.handle_http_error(response)

        # To be consistent with other services,
        # add geojson method to response object.

        def geojson():
            return response.json()

        response.geojson = geojson

        return response
