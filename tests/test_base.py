import base64
import os

import pytest
import requests
import responses

import mapbox
from mapbox.errors import TokenError
from mapbox.services import base


def test_service_session():
    """Get a session using a token"""
    session = base.Session('pk.test')
    assert session.params.get('access_token') == 'pk.test'


def test_service_session_env():
    """Get a session using the env's token"""
    session = base.Session(
        env={'MapboxAccessToken': 'pk.test_env'})
    assert session.params.get('access_token') == 'pk.test_env'


def test_service_session_os_environ(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MapboxAccessToken', 'pk.test_os_environ')
    session = base.Session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


def test_service_session_os_environ_caps(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', 'pk.test_os_environ')
    session = base.Session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


def test_user_agent():
    session = base.Session()
    assert session.headers['User-Agent'].startswith('mapbox-sdk-py')
    assert 'python-requests' in session.headers['User-Agent']


@responses.activate
def test_custom_messages():
    fakeurl = 'https://example.com'
    responses.add(responses.GET, fakeurl, status=401)
    service = base.Service()
    response = service.session.get(fakeurl)

    assert service.handle_http_error(response) is None

    with pytest.raises(mapbox.errors.HTTPError) as exc:
        assert service.handle_http_error(response, custom_messages={401: "error"})
        assert exc.value.message == 'error'

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert service.handle_http_error(response, raise_for_status=True)
        assert "401" in exc.value.message


class MockService(base.Service):
    def __init__(self, access_token=None):
        # In order to get a username, a session must be created on init
        self.session = base.Session(access_token)


def test_username(monkeypatch):
    token = 'pk.{0}.test'.format(base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))
    service = MockService(access_token=token)
    assert service.username == 'testuser'


def test_username_failures(monkeypatch):
    if 'MAPBOX_ACCESS_TOKEN' in os.environ:
        monkeypatch.delenv('MAPBOX_ACCESS_TOKEN')
    service = MockService()
    with pytest.raises(ValueError) as exc:
        service.username
        assert 'access_token' in exc.value.message
        assert 'param' in exc.value.message

    token = "not.good"
    service = MockService(access_token=token)
    with pytest.raises(ValueError) as exc:
        service.username
        assert 'access_token' in exc.value.message
        assert 'username' in exc.value.message
