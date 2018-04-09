import dateutil.parser
from dateutil.relativedelta import relativedelta
from uritemplate import URITemplate

from mapbox.services.base import Service
from mapbox import errors


class Analytics(Service):
    """Access to Analytics API V1
    
    Attributes
    ----------
    api_name : str
        The API's name.
    
    api_version : str
        The API's version number.
    
    valid_resource_types : list
        The possible values for the resource being requested.
    """

    api_name = 'analytics'
    api_version = 'v1'
    valid_resource_types = ['tokens', 'styles', 'accounts', 'tilesets']

    def _validate_resource_type(self, resource_type):
        if resource_type not in self.valid_resource_types:
            raise errors.InvalidResourceTypeError(
                "{0} is not a valid profile".format(resource_type))
        return resource_type

    def _validate_period(self, start, end):
        if start is None and end is None:
            return start, end
        try:
            start_date = dateutil.parser.parse(start)
            end_date = dateutil.parser.parse(end)
        except:
            raise errors.InvalidPeriodError("Dates are not in ISO formatted string")
        if start_date > end_date:
            raise errors.InvalidPeriodError("The first date must be earlier than the second")
        if relativedelta(end_date, start_date).years >= 1 and relativedelta(end_date, start_date).days >= 0:
            raise errors.InvalidPeriodError("The maximum period can be 1 year")
        return start, end

    def _validate_username(self, username):
        if username is None:
            raise errors.InvalidUsernameError("Username is required")
        return username

    def _validate_id(self, resource_type, id):
        if resource_type != 'accounts' and id is None:
            raise errors.InvalidId("Id is required")
        return id

    def analytics(self, resource_type, username, id=None, start=None, end=None):
        """Returns the request counts per day for a given resource and period.
        
        Parameters
        ----------
        resource_type : str
            The resource being requested.
            
            Possible values are "tokens", "styles", "tilesets", and "accounts".
        
        username : str
            The username for the account that owns the resource.
            
        id : str, optional
            The id for the resource.
            
            If resource_type is "tokens", then id is the complete token.
            If resource_type is "styles", then id is the style id.
            If resource_type is "tilesets", then id is a map id.
            If resource_type is "accounts", then id is not required.
        
        start, end : str, optional
            ISO-formatted start and end dates.
            
            If provided, the start date must be earlier than the end date, 
            and the maximum length of time between the start and end dates 
            is one year.
            
            If not provided, the length of time between the start and end 
            dates defaults to 90 days.
        
        Returns
        -------
        requests.Response
        """
        
        resource_type = self._validate_resource_type(resource_type)
        username = self._validate_username(username)
        start, end = self._validate_period(start, end)
        id = self._validate_id(resource_type, id)

        params = {}
        if id is not None:
            params.update({'id': id})

        if start is not None and end is not None:
            params.update({'period': start + ',' + end})

        uri = URITemplate(self.baseuri + '/{resourceType}/{username}').expand(
            resourceType=resource_type, username=username)

        resp = self.session.get(uri, params=params)
        resp.geojson = resp.json()
        self.handle_http_error(resp)

        return resp
