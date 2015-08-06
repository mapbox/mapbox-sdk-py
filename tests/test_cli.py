import json
from click.testing import CliRunner
import responses
from mapbox.scripts.cli import main_group


@responses.activate
def test_cli_geocode_fwd():

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--forward', '1600 pennsylvania ave nw', '--access-token', 'bogus'])
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'


@responses.activate
def test_cli_geocode_fwd_env_token():

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--forward', '1600 pennsylvania ave nw'],
        env={'MapboxAccessToken': 'bogus'})
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'

@responses.activate
def test_cli_geocode_reverse():

    coords = [-77.4371, 37.5227]

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/%s.json?access_token=pk.test' % ','.join(map(lambda x: str(x), coords)),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse', ','.join([str(x) for x in coords]), '--access-token', 'bogus'])
    assert result.exit_code == 0
    assert result.output == '{"query": %s}\n' % json.dumps(coords)

@responses.activate
def test_cli_geocode_reverse_env_token():

    coords = [-77.4371, 37.5227]

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse', ','.join([str(x) for x in coords])],
        env={'MapboxAccessToken': 'bogus'})
    assert result.exit_code == 0
    assert result.output == '{"query": %s}\n' % json.dumps(coords)


@responses.activate
def test_cli_geocode_unauthorized():

    responses.add(
        responses.GET,
        'http://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(main_group, ['geocode', '1600 pennsylvania ave nw'])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'
