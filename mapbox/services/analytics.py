from mapbox.services.base import Service
import dateutil.parser
from dateutil.relativedelta import *
from uritemplate import URITemplate

class Analytics(Service):
    """Access to Analytics API"""

    valid_resource_types = ['tokens', 'styles', 'accounts', 'tilesets']

    @property
    def baseuri(self):
        return 'https://{0}/analytics/v1'.format(self.host)

    def _validate_resource_type(self, resource_type):
        if resource_type not in self.valid_resource_types:
            raise ValueError("{0} is not a valid profile".format(resource_type))
        return resource_type

    def _validate_period(self, period):
        try:
            start_date = dateutil.parser.parse(period[0])
            end_date = dateutil.parser.parse(period[1])
        except:
            raise ValueError("Dates are not in ISO formatted string")
        if start_date > end_date:
            raise ValueError("The first date must be earlier than the second")
        if relativedelta(end_date, start_date).years >= 1 and relativedelta(end_date, start_date).days >= 0:
            raise ValueError("The maximum period can be 1 year")
        return period



    def analytics(self, resource_type, username, id, period):
        resource_type = self._validate_resource_type(resource_type)
        period = self._validate_period(period)

        params = {}
        if resource_type is not None:
            params['resource_type'] = resource_type
        if period is not None:
            params['period'] = period
        if id is None:
            params['id'] = False


        uri = URITemplate(self.baseuri + '/{resourceType}/{username}/{id}?period={period}').expand(
            resourceType=resource_type, username=username, id=id, period=period)

        resp = self.session.get(uri)
        resp.geojson = resp.json()
        self.handle_http_error(resp)

        return resp
