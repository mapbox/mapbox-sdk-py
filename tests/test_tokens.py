import responses

from mapbox.services.tokens import Tokens


@responses.activate
def test_token_create():
    """Token creation works"""
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token=pk.test',
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token='pk.test').create('testuser', ["styles:read", "fonts:read"])
    assert response.status_code == 200


@responses.activate
def test_token_list():
    """Token listing works"""
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2/testuser?access_token=pk.test',
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token='pk.test').list_tokens('testuser')
    assert response.status_code == 200
