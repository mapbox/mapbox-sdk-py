import os.path

import boto3
from boto3.session import Session as boto3_session
from uritemplate import URITemplate

from mapbox.compat import text_types, urlparse
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
                404: "Token does not have upload scope",
                429: "Too many requests"})
        return resp

    def stage(self, fileobj_or_url, creds=None, callback=None,
              region_name=None):
        """Stages data in a Mapbox-owned S3 bucket

        If creds are not provided, temporary credentials will be
        generated using the Mapbox API.

        Note that when a s3:// URL is passed, identifying an object
        in a bucket owned by the caller, the caller must ensure that
        AWS credentials for access to that object are properly
        configured.

        Parameters
        ----------
        fileobj_or_url : file object or str
            A filename, s3:// URL, or a Python file object opened in
            binary mode.
        creds : dict
            AWS credentials allowing uploads to the destination bucket.
        callback : func
            A function that takes a number of bytes processed as its
            sole argument.

        Returns
        -------
        str
            The URL of the staged data
        """
        if (not isinstance(fileobj_or_url, text_types) and
                not hasattr(fileobj_or_url, 'read')):
            raise InvalidFileError(
                "a filename, URL, or file-like object is required")

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

        if isinstance(fileobj_or_url, text_types):
            # s3:// URLs are a special case. We copy these directly
            # between AWS buckets if we can. This requires s3:GetObject
            # to be granted to our federated user.
            if fileobj_or_url.startswith('s3://'):
                parse_results = urlparse(fileobj_or_url)
                assert parse_results.scheme == 's3'
                source_bucket = parse_results.netloc
                source_key = parse_results.path.lstrip('/')

                copy_source = {'Bucket': source_bucket, 'Key': source_key}

                # The source client credentials and region must be
                # configured by the caller.
                source_client = boto3.client('s3', region_name)
                bucket.copy(copy_source, key, SourceClient=source_client,
                            Callback=callback)

            else:
                bucket.upload_file(fileobj_or_url, key, Callback=callback)
        else:
            bucket.upload_fileobj(fileobj_or_url, key, Callback=callback)

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
        stage_url : str
            URL to resource on S3, typically provided in the response
            of this class's stage() method. Does not work on arbitrary
            URLs (TODO).
        tileset : str
            The id of the tileset set to be created. Username will be
            prefixed if not present. For example, 'my-tileset' becomes
            '{username}.my-tileset'.
        name : str
            A short name for the tileset that will appear in Mapbox
            studio.
        patch : bool
            Optional patch mode which requires a flag on the owner's
            account.

        Returns
        -------
        requests.Response
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
        """List uploads

        Returns a Response object, the json() method of which returns
        a list of uploads

        Returns
        -------
        requests.Response
        """
        uri = URITemplate(self.baseuri + '/{username}').expand(
            username=self.username)
        resp = self.session.get(uri)
        self.handle_http_error(resp)

        return resp

    def delete(self, upload):
        """Delete an upload

        Returns a Response object. A response status code of 200
        indicates success.

        Parameters
        ----------
        upload : str
            The id of the upload or a dict with key 'id'.

        Returns
        -------
        requests.Response
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
        """Status of an upload

        Returns a Response object, the json() method of which returns
        and updated upload dict.

        Parameters
        ----------
        upload : str
            The id of the upload or a dict with key 'id'.

        Returns
        -------
        requests.Response
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

    def upload(self, fileobj_or_url, tileset, name=None, patch=False,
               callback=None, region=None):
        """Upload data and create a Mapbox tileset

        Effectively replicates the Studio upload feature. Returns a
        Response object, the json() of which returns a dict with upload
        metadata.

        Note that when a s3:// URL is passed, identifying an object
        in a bucket owned by the caller, the caller must ensure that
        AWS credentials for access to that object are properly
        configured.

        Parameters
        ----------
        fileobj_or_url : file object or str
            A filename, s3:// URL, or a Python file object opened in
            binary mode.
        tileset : str
            A tileset identifier such as '{owner}.my-tileset'.
        name : str
            A short name for the tileset that will appear in Mapbox
            studio.
        patch : bool
            Optional patch mode which requires a flag on the owner's
            account.
        callback : func
            A function that takes a number of bytes processed as its
            sole argument.
        region : str
            Upload data is staged to a bucket in 'us-east-1'. If source
            data is in a different region it must be specified by name.

        Returns
        -------
        requests.Response
        """
        url = self.stage(fileobj_or_url, callback=callback)
        return self.create(url, tileset, name=name, patch=patch)
