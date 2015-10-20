import responses
import json

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
        'https://api.mapbox.com/uploads/v1/{}/credentials?access_token=pk.test'.format(username),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    creds = mapbox.Uploader(username, access_token='pk.test')._get_credentials()
    assert username in creds['url']
    for k in ['key', 'bucket', 'url', 'accessKeyId',
              'secretAccessKey', 'sessionToken']:
        assert k in creds.keys()


# This is not working, moto is not properly patching boto3?
#
# import boto3
# from moto import mock_s3
# @mock_s3
# def test_stage():
#     creds = {
#         "key": "_pending/{}/key.test".format(username),
#         "accessKeyId": "ak.test",
#         "bucket": "tilestream-tilesets-production",
#         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{}/key.test".format(username),
#         "secretAccessKey": "sak.test",
#         "sessionToken": "st.test"}
#     s3 = boto3.resource('s3', region_name='us-east-1')
#     s3.create_bucket(Bucket=creds['bucket'])
#     url = mapbox.Uploader(username, access_token='pk.test').stage('tests/test.csv', creds)
#     assert url == creds['url']
#     assert s3.Object(creds['bucket'], creds['key']).get()['Body'].read().decode("utf-8") == \
#         'testing123'


@responses.activate
def test_upload():
    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{}?access_token=pk.test'.format(username),
        match_querystring=True,
        body=upload_response_body, status=201,
        content_type='application/json')

    job = mapbox.Uploader(username, access_token='pk.test').upload(
        'http://example.com/test.json', 'test1')  # without username prefix
    assert job['tileset'] == "{}.{}".format(username, 'test1')

    job = mapbox.Uploader(username, access_token='pk.test').upload(
        'http://example.com/test.json', 'testuser.test1')  # also takes full tileset
    assert job['tileset'] == "{}.{}".format(username, 'test1')


@responses.activate
def test_list():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{}?access_token=pk.test'.format(username),
        match_querystring=True,
        body="[{}]".format(upload_response_body), status=200,
        content_type='application/json')

    uploads = mapbox.Uploader(username, access_token='pk.test').list()
    assert len(uploads) == 1
    assert json.loads(upload_response_body) in uploads


@responses.activate
def test_status():
    job = json.loads(upload_response_body)
    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{}/{}?access_token=pk.test'.format(username, job['id']),
        match_querystring=True,
        body=upload_response_body, status=200,
        content_type='application/json')

    status = mapbox.Uploader(username, access_token='pk.test').status(job)
    assert job == status


@responses.activate
def test_delete():
    job = json.loads(upload_response_body)
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/uploads/v1/{}/{}?access_token=pk.test'.format(username, job['id']),
        match_querystring=True,
        body=None, status=204,
        content_type='application/json')

    assert mapbox.Uploader(username, access_token='pk.test').delete(job)
