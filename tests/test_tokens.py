import responses
import base64

import pytest

from mapbox.services.tokens import Tokens
from mapbox.errors import ValidationError


token = 'sk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))


@responses.activate
def test_token_create():
    """Token creation works"""
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).create(
        ["styles:read", "fonts:read"], note="new token")
    assert response.status_code == 200


@responses.activate
def test_token_create_username():
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).create(
        ["styles:read", "fonts:read"], username='testuser')
    assert response.status_code == 200


@responses.activate
def test_token_list():
    """Token listing works"""
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).list_tokens()
    assert response.status_code == 200


@responses.activate
def test_token_list_username():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).list_tokens(username='testuser')
    assert response.status_code == 200


@responses.activate
def test_token_list_limit():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}&limit=5'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).list_tokens(limit=5)
    assert response.status_code == 200


@responses.activate
def test_temp_token_create():
    """Temporary token creation works"""
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).create_temp_token(
        ["styles:read", "fonts:read"])
    assert response.status_code == 200


@responses.activate
def test_temp_token_create_username():
    """Temporary token creation works"""
    responses.add(
        responses.POST,
        'https://api.mapbox.com/tokens/v2/testuser?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).create_temp_token(
        ["styles:read", "fonts:read"], username='testuser')
    assert response.status_code == 200


def test_temp_token_expire():
    with pytest.raises(ValidationError):
        response = Tokens(access_token=token).create_temp_token(
            ["styles:read"], expires=3601)


@responses.activate
def test_update_token():
    """Token updation works"""
    responses.add(
        responses.PATCH,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).update(
         'auth_id', note="updated token")
    assert response.status_code == 200


@responses.activate
def test_update_token_username():
    """Token updation works"""
    responses.add(
        responses.PATCH,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token={0}'.format(token),
        match_querystring=True,
        body='{"scopes": ["styles:read", "fonts:read"]}',
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).update(
         'auth_id', ["styles:read", "fonts:read"],
         username='testuser')
    assert response.status_code == 200


def test_temp_token_update_error():
    """update requires scope or notes"""
    with pytest.raises(ValidationError):
        Tokens(access_token=token).update('auth_id')


@responses.activate
def test_delete():
    """Token authorization deletion works"""
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token={0}'.format(token),
        match_querystring=True,
        status=204)

    response = Tokens(access_token=token).delete('auth_id')
    assert response.status_code == 204


@responses.activate
def test_delete_username():
    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/tokens/v2/testuser/auth_id?access_token={0}'.format(token),
        match_querystring=True,
        status=204)

    response = Tokens(access_token=token).delete(
        'auth_id', username='testuser')
    assert response.status_code == 204


@responses.activate
def test_check_validity():
    """Token checking validation works"""
    responses.add(
        responses.GET,
        'https://api.mapbox.com/tokens/v2?access_token={0}'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).check_validity()
    assert response.status_code == 200


@responses.activate
def test_list_scopes():
    """Listing of scopes for a token works"""
    responses.add(
        responses.GET,
        'https://api.mapbox.com/scopes/v1/testuser?access_token={0}'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).list_scopes()
    assert response.status_code == 200


@responses.activate
def test_list_scopes_username():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/scopes/v1/testuser?access_token={0}'.format(token),
        match_querystring=True,
        status=200,
        content_type='application/json')

    response = Tokens(access_token=token).list_scopes(username='testuser')
    assert response.status_code == 200
