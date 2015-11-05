import json

import boto3
from moto import mock_s3
import responses

import mapbox


username = 'testuser'
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
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token=pk.test'.format(username),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    res = mapbox.Uploader(username, access_token='pk.test')._get_credentials()
    assert res.status_code == 200
    creds = res.json()
    assert username in creds['url']
    for k in ['key', 'bucket', 'url', 'accessKeyId',
              'secretAccessKey', 'sessionToken']:
        assert k in creds.keys()


@mock_s3
def test_stage():
    creds = {
        "key": "_pending/{0}/key.test".format(username),
        "accessKeyId": "ak.test",
        "bucket": "tilestream-tilesets-production",
        "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{0}/key.test".format(username),
        "secretAccessKey": "sak.test",
        "sessionToken": "st.test"}
    s3 = boto3.resource('s3', region_name='us-east-1')
    s3.create_bucket(Bucket=creds['bucket'])
    url = mapbox.Uploader(username, access_token='pk.test').stage('tests/test.csv', creds)
    assert url == creds['url']
    assert s3.Object(creds['bucket'], creds['key']).get()['Body'].read() == 'testing123\n'


@responses.activate
def test_extract():
    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token=pk.test'.format(username),
        match_querystring=True,
        body=upload_response_body, status=201,
        content_type='application/json')

    res = mapbox.Uploader(username, access_token='pk.test').extract(
        'http://example.com/test.json', 'test1')  # without username prefix
    assert res.status_code == 201
    job = res.json()
    assert job['tileset'] == "{0}.test1".format(username)

    res2 = mapbox.Uploader(username, access_token='pk.test').extract(
        'http://example.com/test.json', 'testuser.test1')  # also takes full tileset
    assert res2.status_code == 201
    job = res2.json()
    assert job['tileset'] == "{0}.test1".format(username)


@responses.activate
def test_list():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}?access_token=pk.test'.format(username),
        match_querystring=True,
        body="[{0}]".format(upload_response_body), status=200,
        content_type='application/json')

    res = mapbox.Uploader(username, access_token='pk.test').list()
    assert res.status_code == 200
    uploads = res.json()
    assert len(uploads) == 1
    assert json.loads(upload_response_body) in uploads


@responses.activate
def test_status():
    job = json.loads(upload_response_body)
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/{1}?access_token=pk.test'.format(username, job['id']),
        match_querystring=True,
        body=upload_response_body, status=200,
        content_type='application/json')

    res = mapbox.Uploader(username, access_token='pk.test').status(job)
    assert res.status_code == 200
    status = res.json()
    assert job == status


@responses.activate
def test_delete():
    job = json.loads(upload_response_body)
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/uploads/v1/{0}/{1}?access_token=pk.test'.format(username, job['id']),
        match_querystring=True,
        body=None, status=204,
        content_type='application/json')

    res = mapbox.Uploader(username, access_token='pk.test').delete(job)
    assert res.status_code == 204
