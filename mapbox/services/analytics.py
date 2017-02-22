from mapbox.services.base import Service

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
        if period[0] > period[1]:
            raise ValueError("The first date must be earlier than the second")

    # def analytics(self, resource_type, username, id, period):
    #     resource_type = self._validate_resource_type(resource_type)
    #     username = self._validate_username(username)
    #     id = self._validate_id(id)
    #     period = self._validate_period(period)
