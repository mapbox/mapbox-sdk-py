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


@click.command(short_help="Geocode an address or coordinates.")
@click.argument('query', default='-', required=False)
@click.option(
    '--forward/--reverse',
    default=True,
    help="Perform a forward or reverse geocode. [default: forward]")
@click.pass_context
def geocode(ctx, query, forward):
    """This command gets coordinates for an address (forward mode) or
    addresses for coordinates (reverse mode).

    In forward (the default) mode the query argument shall be an address
    such as '1600 pennsylvania ave nw'.

      $ mbx geocode '1600 pennsylvania ave nw'

    In reverse mode the query argument shall be a JSON encoded array
    of longitude and latitude (in that order) in decimal degrees.

      $ mbx geocode --reverse '[-77.4371, 37.5227]'

    """
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
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
