import logging

import click

import mapbox


class MapboxException(click.ClickException):
    pass

def _is_numeric(x):
    try:
        float(x)
    except:
        return False
    return True

@click.command(short_help="Geocode an address.")
@click.argument('LOCATION')
@click.option('--access-token', help="Your access token")
@click.option('--reverse', is_flag=True, flag_value=True, help="Perform a reverse geocode")
@click.pass_context
def geocode(ctx, location, access_token, reverse):
    """Geocode an address"""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')
    geocoder = mapbox.Geocoder(access_token=access_token)

    if not reverse:
        resp = geocoder.forward(location)
    else:
        location_parts = location.split(',')
        if len(location_parts) != 2:
            raise MapboxException('Reverse geocoding requires a LOCATION in format longitude,latitude')
        coords = filter(lambda x: _is_numeric(x), location_parts):
        if len(coords) != 2:
            raise MapboxException('Reverse geocoding LOCATION components must be decimal longitude/latitude')
        rep = geocoder.reverse(coords[0], coord[1])

    if resp.status_code == 200:
        click.echo(resp.text)
    else:
        raise MapboxException(resp.text.strip())

if __name__ == '__main__':
    geocode()