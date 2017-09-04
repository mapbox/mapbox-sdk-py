from datetime import datetime, timedelta

from uritemplate import URITemplate

from mapbox.errors import ValidationError
from mapbox.services.base import Service


class Tokens(Service):
    """Access to the Tokens API."""

    @property
    def baseuri(self):
        return 'https://{0}/tokens/v2'.format(self.host)

    def create(self, scopes, note=None, username=None):
        """Create a permanent token

        Parameters
        ----------
        scopes: list
        note: string
        username: string, defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username
        if not note:
            note = "SDK generated note"

        uri = URITemplate(
            self.baseuri + '/{username}').expand(username=username)

        payload = {'scopes': scopes, 'note': note}

        res = self.session.post(uri, json=payload)
        self.handle_http_error(res)
        return res

    def list_tokens(self, limit=None, username=None):
        """List all permanent tokens

        Parameters
        ----------
        limit: int
        username: string, defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username

        uri = URITemplate(
                self.baseuri + '/{username}').expand(username=username)

        params = {}
        if limit:
            params['limit'] = int(limit)

        res = self.session.get(uri, params=params)
        self.handle_http_error(res)
        return res

    def create_temp_token(self, scopes, expires=3600, username=None):
        """Create a temporary token

        Parameters
        ----------
        scopes: list
            List of valid mapbox token scope strings
        expires: int
            seconds, defaults to 3600 (1 hr)
        username: string
            defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username

        uri = URITemplate(
            self.baseuri + '/{username}').expand(username=username)

        payload = {'scopes': scopes}

        if expires <= 0 or expires > 3600:
            raise ValidationError("Expiry should be within 1 hour from now")
        payload['expires'] = (datetime.utcnow() + timedelta(seconds=expires)).isoformat()

        res = self.session.post(uri, json=payload)
        self.handle_http_error(res)
        return res

    def update(self, authorization_id, scopes=None, note=None, username=None):
        """Update a token's scopes or note

        Parameters
        ----------
        authorization_id: string
            id of the token to update (not the token itself)
        scopes: list
            List of valid mapbox token scope strings
        note: string
        username: string
            defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username
        if not scopes and not note:
            raise ValidationError("Provide either scopes or a note to update token")

        uri = URITemplate(
            self.baseuri + '/{username}/{authorization_id}').expand(
                username=username, authorization_id=authorization_id)

        payload = {}
        if scopes:
            payload['scopes'] = scopes
        if note:
            payload['note'] = note

        res = self.session.patch(uri, json=payload)
        self.handle_http_error(res)
        return res

    def delete(self, authorization_id, username=None):
        """Delete a token

        Parameters
        ----------
        authorization_id: string
            id of the token to update (not the token itself)
        username: string
            defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username

        uri = URITemplate(
            self.baseuri + '/{username}/{authorization_id}').expand(
                username=username, authorization_id=authorization_id)

        res = self.session.delete(uri)
        self.handle_http_error(res)
        return res

    def check_validity(self):
        """Check validity of the token

        Returns
        -------
        requests.Response
        """
        uri = URITemplate(self.baseuri)

        res = self.session.get(uri)
        self.handle_http_error(res)
        return res

    def list_scopes(self, username=None):
        """Delete a token

        Parameters
        ----------
        username: string
            defaults to username in access token

        Returns
        -------
        requests.Response
        """
        if username is None:
            username = self.username

        uri = URITemplate(
            'https://{host}/scopes/v1/{username}').expand(
                host=self.host, username=username)

        res = self.session.get(uri)
        self.handle_http_error(res)
        return res
