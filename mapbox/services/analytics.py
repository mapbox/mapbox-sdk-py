import dateutil.parser
from dateutil.relativedelta import relativedelta
from uritemplate import URITemplate

from mapbox.services.base import Service
from mapbox import errors

class Analytics(Service):
    """Access to Analytics API"""

    valid_resource_types = ['tokens', 'styles', 'accounts', 'tilesets']

    @property
    def baseuri(self):
        return 'https://{0}/analytics/v1'.format(self.host)

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
