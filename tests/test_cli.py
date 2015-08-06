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
        ['geocode', '1600 pennsylvania ave nw', '--access-token', 'bogus'])
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
        ['geocodex', '1600 pennsylvania ave nw'],
        env={'MapboxAccessToken': 'bogus'},
        catch_exceptions=False)
    import pdb; pdb.set_trace()
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'


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
