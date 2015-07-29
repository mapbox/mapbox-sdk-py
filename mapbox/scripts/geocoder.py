import logging

import click

import mapbox


@click.command(short_help="Geocode an address.")
@click.argument('ADDRESS')
@click.option('--access-token', help="Your access token")
@click.pass_context
def geocode(ctx, address, access_token):
    """Geocode an address"""
    geocoder = mapbox.Geocoder(access_token=access_token)
    resp = geocoder.fwd(address)
    if resp.status_code == 200:
        click.echo(resp.text)
    else:
        ctx.fail(resp.reason)
