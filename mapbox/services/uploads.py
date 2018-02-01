"""Mapbox Uploads API
"""

import re
import warnings

from boto3.session import Session as boto3_session
from uritemplate import URITemplate

from mapbox.errors import ValidationError
from mapbox.services.base import Service


class Uploader(Service):
    """Access to the Upload API V1

    Example usage:

        from mapbox import Uploader

        u = Uploader()
        url = u.stage(open('test.tif', 'rb'))
        job = u.create(url, 'test1').json()

        assert job in u.list().json()

        # ... wait unti finished ...
        finished = u.status(job).json()['complete']

        u.delete(job)
        assert job not in u.list().json()
    """

    api_name = 'uploads'
    api_version = 'v1'

    def _get_credentials(self):
        """Gets temporary S3 credentials to stage user-uploaded files
        """
        uri = URITemplate(self.baseuri + '/{username}/credentials').expand(
            username=self.username)

        resp = self.session.post(uri)

        self.handle_http_error(
            resp,
            custom_messages={
                401: "Token is not authorized",
                404: "Token does not have upload scope",
                429: "Too many requests"})
        return resp

    def _validate_tileset(self, tileset):
        """Validate the tileset name and
        ensure that it includes the username
        """
        if '.' not in tileset:
            tileset = "{0}.{1}".format(self.username, tileset)

        pattern = '^[a-z0-9-_]{1,32}\.[a-z0-9-_]{1,32}$'
        if not re.match(pattern, tileset, flags=re.IGNORECASE):
            raise ValidationError(
                'tileset {0} is invalid, must match r"{1}"'.format(
                    tileset, pattern))

        return tileset

    # TODO: remove this method at 1.0.
    def _resolve_username(self, account, username):
        """Resolve username and handle deprecation of account kwarg"""
        if account is not None:
            warnings.warn(
                "Use keyword argument 'username' instead of 'account'",
                DeprecationWarning)
        return username or account or self.username

    def stage(self, fileobj, creds=None, callback=None):
        """Stages data in a Mapbox-owned S3 bucket

        If creds are not provided, temporary credentials will be
        generated using the Mapbox API.

        Parameters
        ----------
        fileobj: file object or filename
            A Python file object opened in binary mode or a filename.
        creds: dict
            AWS credentials allowing uploads to the destination bucket.
        callback: func
            A function that takes a number of bytes processed as its
            sole argument.

        Returns
        -------
        str
            The URL of the staged data
        """

        if not hasattr(fileobj, 'read'):
            fileobj = open(fileobj, 'rb')

        if not creds:
            res = self._get_credentials()
            creds = res.json()

        session = boto3_session(
            aws_access_key_id=creds['accessKeyId'],
            aws_secret_access_key=creds['secretAccessKey'],
            aws_session_token=creds['sessionToken'],
            region_name='us-east-1')

        s3 = session.resource('s3')
        bucket = s3.Bucket(creds['bucket'])
        key = creds['key']
        bucket.upload_fileobj(fileobj, key, Callback=callback)

        return creds['url']

    def create(self, stage_url, tileset, name=None, patch=False):
        """Create a tileset

        Note: this step is refered to as "upload" in the API docs;
        This class's upload() method is a high-level function
        which acts like the Studio upload form.

        Returns a response object where the json() contents are
        an upload dict. Completion of the tileset may take several
        seconds or minutes depending on size of the data. The status()
        method of this class may be used to poll the API endpoint for
        tileset creation status.

        Parameters
        ----------
        stage_url: str
            URL to resource on S3, typically provided in the response
            of this class's stage() method.
        tileset: str
            The id of the tileset set to be created. Username will be
            prefixed if not present. For example, 'my-tileset' becomes
            '{username}.my-tileset'.
        name: str
            A short name for the tileset that will appear in Mapbox
            studio.
        patch: bool
            Optional patch mode which requires a flag on the owner's
            account.

        Returns
        -------
        requests.Response
        """
        tileset = self._validate_tileset(tileset)
        username, _name = tileset.split(".")

        msg = {'tileset': tileset,
               'url': stage_url}

        if patch:
            msg['patch'] = patch

        msg['name'] = name if name else _name

        uri = URITemplate(self.baseuri + '/{username}').expand(
            username=username)

        resp = self.session.post(uri, json=msg)
        self.handle_http_error(resp)

        return resp

    def list(self, account=None, username=None):
        """List of all uploads

        Returns a Response object, the json() method of which returns
        a list of uploads

        Parameters
        ----------
        username : str
            Account username, defaults to the service's username.
        account : str, **deprecated**
            Alias for username. Will be removed in version 1.0.

        Returns
        -------
        requests.Response
        """
        username = self._resolve_username(account, username)
        uri = URITemplate(self.baseuri + '/{username}').expand(
            username=username)
        resp = self.session.get(uri)
        self.handle_http_error(resp)
        return resp

    def delete(self, upload, account=None, username=None):
        """Delete the specified upload

        Parameters
        ----------
        upload: str
            The id of the upload or a dict with key 'id'.
        username : str
            Account username, defaults to the service's username.
        account : str, **deprecated**
            Alias for username. Will be removed in version 1.0.

        Returns
        -------
        requests.Response
        """
        username = self._resolve_username(account, username)
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload
        uri = URITemplate(self.baseuri + '/{username}/{upload_id}').expand(
            username=username, upload_id=upload_id)
        resp = self.session.delete(uri)
        self.handle_http_error(resp)
        return resp

    def status(self, upload, account=None, username=None):
        """Check status of upload

        Parameters
        ----------
        upload: str
            The id of the upload or a dict with key 'id'.
        username : str
            Account username, defaults to the service's username.
        account : str, **deprecated**
            Alias for username. Will be removed in version 1.0.

        Returns
        -------
        requests.Response
        """
        username = self._resolve_username(account, username)
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload
        uri = URITemplate(self.baseuri + '/{username}/{upload_id}').expand(
            username=username, upload_id=upload_id)
        resp = self.session.get(uri)
        self.handle_http_error(resp)
        return resp

    def upload(self, fileobj, tileset, name=None, patch=False, callback=None):
        """Upload data and create a Mapbox tileset

        Effectively replicates the Studio upload feature. Returns a
        Response object, the json() of which returns a dict with upload
        metadata.

        Parameters
        ----------
        fileobj: file object or str
            A filename or a Python file object opened in binary mode.
        tileset: str
            A tileset identifier such as '{owner}.my-tileset'.
        name: str
            A short name for the tileset that will appear in Mapbox
            studio.
        patch: bool
            Optional patch mode which requires a flag on the owner's
            account.
        callback: func
            A function that takes a number of bytes processed as its
            sole argument. May be used with a progress bar.

        Returns
        -------
        requests.Response
        """
        tileset = self._validate_tileset(tileset)
        url = self.stage(fileobj, callback=callback)
        return self.create(url, tileset, name=name, patch=patch)
