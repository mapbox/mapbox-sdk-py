import json
from click.testing import CliRunner
import responses
from mapbox.scripts.cli import main_group
from mapbox.scripts.geocoder import coords_from_query, iter_query


def test_iter_query_string():
    assert iter_query("lolwut") == ["lolwut"]


def test_iter_query_file(tmpdir):
    filename = str(tmpdir.join('test.txt'))
    with open(filename, 'w') as f:
        f.write("lolwut")
    assert iter_query(filename) == ["lolwut"]


def test_coords_from_query_json():
    assert coords_from_query("[-100, 40]") == (-100, 40)


def test_coords_from_query_csv():
    assert coords_from_query("-100, 40") == (-100, 40)


def test_coords_from_query_ws():
    assert coords_from_query("-100 40") == (-100, 40)


@responses.activate
def test_cli_geocode_fwd():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
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
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
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
        'https://api.mapbox.com/v4/geocode/mapbox.places/%s.json?access_token=pk.test' % ','.join([str(x) for x in coords]),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse', '--access-token', 'pk.test'],
        input=','.join([str(x) for x in coords]))
    assert result.exit_code == 0
    assert result.output == '{"query": %s}\n' % json.dumps(coords)


@responses.activate
def test_cli_geocode_reverse_env_token():

    coords = [-77.4371, 37.5227]

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/%s.json?access_token=bogus' % ','.join([str(x) for x in coords]),
        match_querystring=True,
        body='{"query": %s}' % json.dumps(coords),
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse'],
        input=','.join([str(x) for x in coords]),
        env={'MapboxAccessToken': 'bogus'})
    assert result.exit_code == 0
    assert result.output == '{"query": %s}\n' % json.dumps(coords)


@responses.activate
def test_cli_geocode_unauthorized():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(main_group, ['geocode', '--forward', '1600 pennsylvania ave nw'])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'


@responses.activate
def test_cli_geocode_rev_unauthorized():
    coords = (-77.4371, 37.5227)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/geocode/mapbox.places/%s,%s.json' % coords,
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse'],
        input='%s,%s' % coords)
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'
