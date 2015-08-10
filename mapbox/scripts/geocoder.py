import logging
import json
import re

import click

import mapbox
from mapbox.compat import map


class MapboxException(click.ClickException):
    pass


def iter_query(query):
    """Accept a filename, stream, or string.
    Returns an iterator over lines of the query."""
    try:
        itr = click.open_file(query).readlines()
    except IOError:
        itr = [query]
    return itr


def coords_from_query(query):
    """Transform a query line into a (lng, lat) pair of coordinates."""
    try:
        coords = json.loads(query)
    except ValueError:
        vals = re.split(r"\,*\s*", query.strip())
        coords = [float(v) for v in vals]
    return tuple(coords[:2])


@click.command(short_help="Geocode an address.")
@click.argument('query', default='-', required=False)
@click.option('--access-token', help="Your access token")
@click.option(
    '--forward/--reverse',
    default=True,
    help="Perform a forward (default) or reverse geocode")
@click.pass_context
def geocode(ctx, query, access_token, forward):
    """Geocode an address"""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')
    geocoder = mapbox.Geocoder(access_token=access_token)

    if forward:
        for q in iter_query(query):
            resp = geocoder.forward(q)
            if resp.status_code == 200:
                click.echo(resp.text)
            else:
                raise MapboxException(resp.text.strip())
    else:
        for coords in map(coords_from_query, iter_query(query)):
            resp = geocoder.reverse(*coords)
            if resp.status_code == 200:
                click.echo(resp.text)
            else:
                raise MapboxException(resp.text.strip())
