import arrow

from uritemplate import URITemplate

from mapbox.services.base import Service


class Tokens(Service):
    """Access to the Tokens API."""

    @property
    def baseuri(self):
        return 'https://{0}/tokens/v2'.format(self.host)

    def create(self, username, scopes=None, note=None, expires=0):
        if not scopes:
            raise ValueError("One or more token scopes are required")
        if not note:
            note = "SDK generated note"

        uri = URITemplate(self.baseuri + '/{username}').expand(username=username)

        payload = {'scopes': scopes, 'note': note}

        if expires > 0:
            payload['expires'] = arrow.now().replace(seconds=+expires).isoformat()

        res = self.session.post(uri, json=payload)
        self.handle_http_error(res)
        return res
