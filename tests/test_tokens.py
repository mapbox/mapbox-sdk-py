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


@responses.activate
def test_temp_token_create():
    """Temporary token creation works"""
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token=sk.test',
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token='sk.test').create_temp_token('testuser', ["styles:read", "fonts:read"], 3600)
    assert response.status_code == 200


@responses.activate
def test_update_token():
    """Token updation works"""
    responses.add(
        responses.PATCH,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token=pk.test',
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token='pk.test').update_auth('testuser', 'auth_id', ["styles:read", "fonts:read"])
    assert response.status_code == 200


@responses.activate
def test_delete_auth():
    """Token authorization deletion works"""
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token=pk.test',
        match_querystring=True,
        status=204)

    response = Tokens(access_token='pk.test').delete_auth('testuser', 'auth_id')
    assert response.status_code == 204


@responses.activate
def test_check_validity():
    """Token checking validation works"""
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2?access_token=pk.test',
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token='pk.test').check_validity()
    assert response.status_code == 200
