# mapbox
from uritemplate import URITemplate
from .base import Service
from boto3.session import Session


class Uploader(Service):
    """Mapbox Upload API
    """

    def __init__(self, username, access_token=None):
        self.username = username
        self.baseuri = 'https://api.mapbox.com/uploads/v1'
        self.session = self.get_session(access_token)

    def _get_credentials(self):
        uri = URITemplate('%s/{username}/credentials' % self.baseuri).expand(
            username=self.username)
        res = self.session.get(uri)
        if res.status_code == 200:
            return res.json()
        else:
            # TODO raise appropriate exception and check for other types of errors
            raise Exception("Request for AWS credentials failed."
                            "Ensure your access token has scope 'uploads:write'")

    def stage(self, filepath, creds=None):
        if not creds:
            creds = self._get_credentials()
        session = Session(aws_access_key_id=creds['accessKeyId'],
                          aws_secret_access_key=creds['secretAccessKey'],
                          aws_session_token=creds['sessionToken'],
                          region_name="us-east-1")

        s3 = session.resource('s3')
        with open(filepath, 'rb') as data:
            s3.Object(creds['bucket'], creds['key']).put(Body=data)

        return creds['url']

    def upload(self, stage_url, tileset, name=None):

        if not tileset.startswith(self.username + "."):
            tileset = "{}.{}".format(self.username, tileset)

        msg = {'tileset': tileset,
               'url': stage_url}

        if name is not None:
            msg['name'] = name

        uri = URITemplate('%s/{username}' % self.baseuri).expand(
            username=self.username)

        res = self.session.post(uri, json=msg)
        if res.status_code == 201:
            return res.json()
        else:
            raise Exception("Upload failed")  # TODO

    def list(self):
        uri = URITemplate('%s/{username}' % self.baseuri).expand(
            username=self.username)
        res = self.session.get(uri)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception("GET list failed")  # TODO

    def delete(self, upload):
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload

        uri = URITemplate('%s/{username}/{upload_id}' % self.baseuri).expand(
            username=self.username, upload_id=upload_id)
        res = self.session.delete(uri)
        if res.status_code == 204:
            return True
        else:
            raise Exception("Delete failed")  # TODO

    def status(self, upload):
        if isinstance(upload, dict):
            upload_id = upload['id']
        else:
            upload_id = upload

        uri = URITemplate('%s/{username}/{upload_id}' % self.baseuri).expand(
            username=self.username, upload_id=upload_id)
        res = self.session.get(uri)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception("Status failed")  # TODO
