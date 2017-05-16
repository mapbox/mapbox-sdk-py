import base64
import json
import re

import mock
import responses
import pytest

import mapbox
import mapbox.services.uploads


username = 'testuser'
access_token = 'pk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))


upload_response_body = """
    {{"progress": 0,
    "modified": "date.test",
    "error": null,
    "tileset": "{username}.test1",
    "complete": false,
    "owner": "{username}",
    "created": "date.test",
    "id": "id.test",
    "name": null}}""".format(username=username)


@responses.activate
def test_get_credentials():
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    res = mapbox.Uploader(access_token=access_token)._get_credentials()

    assert res.status_code == 200
    creds = res.json()
    assert username in creds['url']
    for k in ['key', 'bucket', 'url', 'accessKeyId',
              'secretAccessKey', 'sessionToken']:
        assert k in creds.keys()


@responses.activate
def test_create():
    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=upload_response_body, status=201,
        content_type='application/json')

    res = mapbox.Uploader(access_token=access_token).create(
        'http://example.com/test.json', 'test1')  # without username prefix
    assert res.status_code == 201
    job = res.json()
    assert job['tileset'] == "{0}.test1".format(username)

    res2 = mapbox.Uploader(access_token=access_token).create(
        'http://example.com/test.json', 'testuser.test1')  # also takes full tileset
    assert res2.status_code == 201
    job = res2.json()
    assert job['tileset'] == "{0}.test1".format(username)


@responses.activate
def test_create_name():
    upload_response_body = """
        {"progress": 0,
        "modified": "date.test",
        "error": null,
        "tileset": "testuser.test1",
        "complete": false,
        "owner": "testuser",
        "created": "date.test",
        "id": "id.test",
        "name": "testname"}"""

    def request_callback(request):
        payload = json.loads(request.body.decode())
        assert payload['name'] == "testname"
        return (201, {}, upload_response_body)

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        callback=request_callback)

    res = mapbox.Uploader(access_token=access_token).create(
        'http://example.com/test.json', 'testuser.test1', name="testname")
    assert res.status_code == 201
    job = res.json()
    assert job['name'] == "testname"


@responses.activate
def test_list():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body="[{0}]".format(upload_response_body), status=200,
        content_type='application/json')

    res = mapbox.Uploader(access_token=access_token).list()
    assert res.status_code == 200
    uploads = res.json()
    assert len(uploads) == 1
    assert json.loads(upload_response_body) in uploads


@responses.activate
def test_status():
    job = json.loads(upload_response_body)
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/{1}?access_token={2}'.format(username, job['id'], access_token),
        match_querystring=True,
        body=upload_response_body, status=200,
        content_type='application/json')

    res = mapbox.Uploader(access_token=access_token).status(job)
    assert res.status_code == 200
    res = mapbox.Uploader(access_token=access_token).status(job['id'])
    assert res.status_code == 200
    status = res.json()
    assert job == status


@responses.activate
def test_delete():
    job = json.loads(upload_response_body)
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/uploads/v1/{0}/{1}?access_token={2}'.format(username, job['id'], access_token),
        match_querystring=True,
        body=None, status=204,
        content_type='application/json')

    res = mapbox.Uploader(access_token=access_token).delete(job)
    assert res.status_code == 204

    res = mapbox.Uploader(access_token=access_token).delete(job['id'])
    assert res.status_code == 204


class MockSession(object):
    """Mocks a boto3 session."""

    def __init__(self, *args, **kwargs):
        self.bucket = None
        self.key = None
        pass

    def resource(self, name):
        self.resource_name = name
        return self

    def Object(self, bucket, key):
        assert self.resource_name == 's3'
        self.bucket = bucket
        self.key = key
        return self

    def put(self, Body):
        assert self.bucket
        assert self.key
        self.body = Body
        return True

    def Bucket(self, bucket):
        self.bucket = bucket
        return self

    def upload_file(self, filename, key, Callback=None):
        self.filename = filename
        self.key = key
        self.Callback = Callback

    def upload_fileobj(self, data, key, Callback=None):
        self.data = data
        self.key = key
        self.Callback = Callback

        bytes_read = data.read(8192)
        if bytes_read and self.Callback:
            self.Callback(len(bytes_read))
        while bytes_read:
            bytes_read = data.read(8192)
            if bytes_read and self.Callback:
                self.Callback(len(bytes_read))

    def copy(self, source, key, ExtraArgs=None, Callback=None,
             SourceClient=None, Config=None):
        self.source = source
        self.key = key
        self.Callback = Callback


@responses.activate
def test_stage(monkeypatch):

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)
    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    with open('tests/moors.json', 'rb') as src:
        stage_url = mapbox.Uploader(access_token=access_token).stage(src)
    assert stage_url.startswith("https://tilestream-tilesets-production.s3.amazonaws.com/_pending")


@responses.activate
def test_stage_filename(monkeypatch):
    """A filename works too"""

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)
    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    stage_url = mapbox.Uploader(access_token=access_token).stage('tests/moors.json')
    assert stage_url.startswith("https://tilestream-tilesets-production.s3.amazonaws.com/_pending")


@responses.activate
def test_big_stage(tmpdir, monkeypatch):
    """Files larger than 1M are multipart uploaded."""

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    # Make a temp file larger than 1MB.
    bigfile = tmpdir.join('big.txt')
    bigfile.write(','.join(('num' for num in range(1000000))))
    assert bigfile.size() > 1000000

    with bigfile.open(mode='rb') as src:
        stage_url = mapbox.Uploader(access_token=access_token).stage(src)
    assert stage_url.startswith("https://tilestream-tilesets-production.s3.amazonaws.com/_pending")


@responses.activate
def test_upload(monkeypatch):
    """Upload a file and create a tileset"""

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=upload_response_body, status=201,
        content_type='application/json')

    def print_cb(num_bytes):
        print("{0} bytes uploaded".format(num_bytes))

    with open('tests/moors.json', 'rb') as src:
        res = mapbox.Uploader(access_token=access_token).upload(src, 'test1', callback=print_cb)

    assert res.status_code == 201
    job = res.json()
    assert job['tileset'] == "{0}.test1".format(username)


@responses.activate
def test_upload_error(monkeypatch):
    """Upload a file and create a tileset, fails with 409"""

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body="", status=409,
        content_type='application/json')

    with open('tests/moors.json', 'rb') as src:
        res = mapbox.Uploader(access_token=access_token).upload(src, 'test1')

    assert res.status_code == 409


@responses.activate
def test_upload_patch(monkeypatch):
    """Upload a file and create a tileset in patch mode"""

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    def ensure_patch(request):
        payload = json.loads(request.body.decode())
        assert payload['patch']
        headers = {}
        return (201, headers, upload_response_body)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    responses.add_callback(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        callback=ensure_patch,
        match_querystring=True,
        content_type='application/json')

    with open('tests/moors.json', 'rb') as src:
        res = mapbox.Uploader(access_token=access_token).upload(
            src, 'testuser.test1', name='test1', patch=True)

    assert res.status_code == 201
    job = res.json()
    assert job['tileset'] == "{0}.test1".format(username)
