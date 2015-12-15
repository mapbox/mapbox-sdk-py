# mapbox
from boto3.session import Session as boto3_session
from uritemplate import URITemplate

from .base import Service
from mapbox.errors import InvalidFileError


class Uploader(Service):
    """Mapbox Upload API

    Example usage:

        from mapbox import Uploader

        u = Uploader()
        url = u.stage(open('test.tif'))
        job = u.create(url, 'test1').json()

        assert job in u.list().json()

        # ... wait unti finished ...
        finished = u.status(job).json()['complete']

        u.delete(job)
        assert job not in u.list().json()
    """

    def __init__(self, access_token=None):
        self.baseuri = 'https://api.mapbox.com/uploads/v1'
        self.session = self.get_session(access_token)

    def _get_credentials(self):
        """Gets temporary S3 credentials to stage user-uploaded files
        """
        uri = URITemplate('%s/{username}/credentials' % self.baseuri).expand(
            username=self.username)
        resp = self.session.get(uri)
        self.handle_http_error(
            resp,
            custom_messages={
                401: "Token is not authorized",
                404: "Token does not have upload scope"})
        return resp

    def stage(self, fileobj, creds=None):
        """Stages the user's file on S3
        If creds are not provided, temporary credientials will be generated
        Returns the URL to the staged resource.
        """
        if not hasattr(fileobj, 'read'):
            raise InvalidFileError(
                "Object `{0}` has no .read method, "
                "a file-like object is required".format(fileobj))

        if not creds:
            res = self._get_credentials()
            creds = res.json()

        session = boto3_session(
            aws_access_key_id=creds['accessKeyId'],
            aws_secret_access_key=creds['secretAccessKey'],
            aws_session_token=creds['sessionToken'],
            region_name="us-east-1")

        s3 = session.resource('s3')
        res = s3.Object(creds['bucket'], creds['key']).put(Body=fileobj)

        return creds['url']

    def create(self, stage_url, tileset, name=None):
        """Initiates the creation process from the
        staging S3 bucket into the user's tileset.

        Note: this step is refered to as "upload" in the API docs;
        This classes upload() method is a high-level function
        which acts like the web-based upload form

        Parameters
        stage_url: URL to resource on S3, does not work on arbitrary URLs (TODO)
        tileset: the map/tileset name to create. Username will be prefixed if not
                 done already (e.g. 'test1' becomes 'username.test1')

        Returns a response object where the json() contents are
        an upload dict
        """
        if not tileset.startswith(self.username + "."):
            tileset = "{0}.{1}".format(self.username, tileset)

        msg = {'tileset': tileset,
               'url': stage_url}

        if name is not None:
            msg['name'] = name

        uri = URITemplate('%s/{username}' % self.baseuri).expand(
            username=self.username)

        resp = self.session.post(uri, json=msg)
        self.handle_http_error(resp)
        return resp

    def list(self):
        """List of all uploads

        Returns a response object where the json() contents are
        a list of uploads
        """
        uri = URITemplate('%s/{username}' % self.baseuri).expand(
            username=self.username)
        resp = self.session.get(uri)
        self.handle_http_error(resp)
        return resp

    def delete(self, upload):
        """Delete the specified upload
        """
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload

        uri = URITemplate('%s/{username}/{upload_id}' % self.baseuri).expand(
            username=self.username, upload_id=upload_id)
        resp = self.session.delete(uri)
        self.handle_http_error(resp)
        return resp

    def status(self, upload):
        """Check status of upload

        Returns a response object where the json() contents are
        another (updated) upload dict
        """
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload

        uri = URITemplate('%s/{username}/{upload_id}' % self.baseuri).expand(
            username=self.username, upload_id=upload_id)
        resp = self.session.get(uri)
        self.handle_http_error(resp)
        return resp

    def upload(self, fileobj, tileset, name=None):
        """High level function to upload a file object to mapbox tileset
        Effectively replicates the upload functionality using the HTML form
        Returns a response object where the json() is a dict with upload metadata
        """
        url = self.stage(fileobj)
        return self.create(url, tileset, name=name)
