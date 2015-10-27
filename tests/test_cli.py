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
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus', 'geocode', '--forward', '1600 pennsylvania ave nw'])
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'


@responses.activate
def test_cli_geocode_fwd_env_token():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
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

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'pk.test', 'geocode', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 0
    assert result.output.strip() == body


@responses.activate
def test_cli_geocode_reverse_env_token():

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=bogus'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse'],
        input='{0},{1}'.format(lon, lat),
        env={'MapboxAccessToken': 'bogus'})
    assert result.exit_code == 0
    assert result.output.strip() == body


@responses.activate
def test_cli_geocode_unauthorized():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(main_group, ['geocode', '--forward',
                                        '1600 pennsylvania ave nw'])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'


@responses.activate
def test_cli_geocode_rev_unauthorized():

    lon, lat = -77.4371, 37.5227

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json'.format(lon, lat),
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'


@responses.activate
def test_cli_geocode_fwd_headers():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '-i', '--forward', '1600 pennsylvania ave nw'])
    assert result.exit_code == 0
    assert result.output.startswith('Content-Type')


@responses.activate
def test_cli_geocode_rev_headers():

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json'.format(lon, lat),
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocode', '-i', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 0
    assert result.output.startswith('Content-Type')
