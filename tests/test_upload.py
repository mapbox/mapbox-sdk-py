import json
import base64

import responses

import mapbox


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
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
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
        payload = json.loads(request.body)
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
    """ Mocks a boto3 session,
    specifically for the purposes of an s3 key put
    """
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


@responses.activate
def test_stage():
    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    stage_url = mapbox.Uploader(access_token=access_token).stage(
        'tests/moors.json',
        session_class=MockSession)

    assert stage_url.startswith("https://tilestream-tilesets-production.s3.amazonaws.com/_pending")
