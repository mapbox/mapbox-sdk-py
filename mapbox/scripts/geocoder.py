import logging

import click

import mapbox


class MapboxException(click.ClickException):
    pass


@click.command(short_help="Geocode an address.")
@click.argument('ADDRESS')
@click.option('--access-token', help="Your access token")
@click.pass_context
def geocode(ctx, address, access_token):
    """Geocode an address"""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')
    geocoder = mapbox.Geocoder(access_token=access_token)
    resp = geocoder.fwd(address)
    if resp.status_code == 200:
        click.echo(resp.text)
    else:
        raise MapboxException(resp.text.strip())

if __name__ == '__main__':
    geocode()