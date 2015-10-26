# mapbox
from uritemplate import URITemplate
from .base import Service
from boto3.session import Session


class Uploader(Service):
    """Mapbox Upload API

    Example usage:

        from mapbox import Uploader

        u = Uploader('username')
        url = u.stage('test.tif')
        job = u.extract(url, 'test1').json()

        assert job in u.list().json()

        # ... wait unti finished ...
        finished = u.status(job).json()['complete']

        u.delete(job)
        assert job not in u.list().json()
    """

    def __init__(self, username, access_token=None):
        self.username = username
        self.baseuri = 'https://api.mapbox.com/uploads/v1'
        self.session = self.get_session(access_token)

    def _get_credentials(self):
        """Gets temporary S3 credentials to stage user-uploaded files
        """
        uri = URITemplate('%s/{username}/credentials' % self.baseuri).expand(
            username=self.username)
        res = self.session.get(uri)
        res.raise_for_status()
        # TODO if there is a perms error,
        # massage exeption to alert user about upload:* scope tokens
        return res

    def stage(self, filepath, creds=None):
        """Stages the user's file on S3
        If creds are not provided, temporary credientials will be generated
        Returns the URL to the staged resource.
        """
        if not creds:
            res = self._get_credentials()
            creds = res.json()

        session = Session(aws_access_key_id=creds['accessKeyId'],
                          aws_secret_access_key=creds['secretAccessKey'],
                          aws_session_token=creds['sessionToken'],
                          region_name="us-east-1")

        s3 = session.resource('s3')
        with open(filepath, 'rb') as data:
            res = s3.Object(creds['bucket'], creds['key']).put(Body=data)

        return creds['url']

    def extract(self, stage_url, tileset, name=None):
        """Initiates the extraction process from the
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

        res = self.session.post(uri, json=msg)
        res.raise_for_status()
        return res

    def list(self):
        """List of all uploads

        Returns a response object where the json() contents are
        a list of uploads
        """
        uri = URITemplate('%s/{username}' % self.baseuri).expand(
            username=self.username)
        res = self.session.get(uri)
        res.raise_for_status()
        return res

    def delete(self, upload):
        """Delete the specified upload
        """
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload

        uri = URITemplate('%s/{username}/{upload_id}' % self.baseuri).expand(
            username=self.username, upload_id=upload_id)
        res = self.session.delete(uri)
        res.raise_for_status()
        return res

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
        res = self.session.get(uri)
        res.raise_for_status()
        return res

    def upload(self, filepath, tileset):
        """High level function to upload a local file to mapbox tileset
        Effectively replicates the upload functionality using the HTML form
        Returns a response object where the json() is a dict with upload metadata
        """
        url = self.stage(filepath)
        return self.extract(url, tileset)
