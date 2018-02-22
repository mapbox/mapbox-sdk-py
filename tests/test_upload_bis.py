import base64
import json
import re

from boto3.session import Session
from hypothesis import example, given, settings
from hypothesis.strategies import text, integers
import mock
import responses
import pytest

import mapbox
import mapbox.services.uploads


# Fake Mapbox users.
accounts = ['arthur', 'zaphod']
tokens = [
    'pk.' + base64.b64encode(json.dumps({'u': user, 'd': 'test'}).encode()).decode()
    for user in accounts]


def credentials_body(account):
    return """
       {{"key": "staging/{account}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "bucket.test",
         "url": "https://bucket.test.s3.amazonaws.com/staging/{account}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(account=account)


@responses.activate
@pytest.mark.parametrize("account, token", zip(accounts, tokens))
def test_get_credentials(account, token):
    """Getting credentials from account matching the token works"""

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            account, token),
        match_querystring=True,
        body=credentials_body(account), status=200,
        content_type='application/json')

    res = mapbox.Uploader(access_token=token)._get_credentials()

    assert res.status_code == 200
    creds = res.json()
    assert account in creds['url']
    for k in ['key', 'bucket', 'url', 'accessKeyId',
              'secretAccessKey', 'sessionToken']:
        assert k in creds.keys()


@responses.activate
@pytest.mark.parametrize("account, token", zip(accounts, reversed(tokens)))
def test_get_credentials_crossed(account, token):
    """Getting credentials from account not matching the token fails"""

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(
            account, token),
        match_querystring=True,
        body=json.dumps({"message": "Not Found"}), status=404,
        content_type='application/json')

    res = mapbox.Uploader(access_token=token)._get_credentials()

    assert res.status_code == 404
    assert res.json()['message'] == 'Not Found'
