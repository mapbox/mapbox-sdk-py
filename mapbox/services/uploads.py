import os.path

from boto3.session import Session as boto3_session
from uritemplate import URITemplate

from mapbox.errors import InvalidFileError
from mapbox.services.base import Service


class Uploader(Service):
    """Access to the Upload API.

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

    @property
    def baseuri(self):
        return 'https://{0}/uploads/v1'.format(self.host)

    def _get_credentials(self):
        """Gets temporary S3 credentials to stage user-uploaded files
        """
        uri = URITemplate(self.baseuri + '/{username}/credentials').expand(
            username=self.username)
        resp = self.session.get(uri)
        self.handle_http_error(
            resp,
            custom_messages={
                401: "Token is not authorized",
                404: "Token does not have upload scope"})
        return resp

    def stage(self, fileobj, creds=None, callback=None):
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

        bucket = s3.Bucket(creds['bucket'])
        bucket.upload_fileobj(fileobj, creds['key'], Callback=callback)

        return creds['url']

    def create(self, stage_url, tileset, name=None, patch=False):
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

        if patch:
            msg['patch'] = patch

        if name is not None:
            msg['name'] = name

        uri = URITemplate(self.baseuri + '/{username}').expand(
            username=self.username)

        resp = self.session.post(uri, json=msg)
        self.handle_http_error(resp)
        return resp

    def list(self):
        """List of all uploads

        Returns a response object where the json() contents are
        a list of uploads
        """
        uri = URITemplate(self.baseuri + '/{username}').expand(
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

        uri = URITemplate(self.baseuri + '/{username}/{upload_id}').expand(
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

        uri = URITemplate(self.baseuri + '/{username}/{upload_id}').expand(
            username=self.username, upload_id=upload_id)
        resp = self.session.get(uri)
        self.handle_http_error(resp)
        return resp

    def upload(self, fileobj, tileset, name=None, patch=False, callback=None):
        """High level function to upload a file object to mapbox tileset
        Effectively replicates the upload functionality using the HTML form
        Returns a response object where the json() is a dict with upload metadata
        """
        url = self.stage(fileobj, callback=callback)
        return self.create(url, tileset, name=name, patch=patch)
