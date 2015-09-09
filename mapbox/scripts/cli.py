"""
Main click group for CLI
"""


import logging
from pkg_resources import iter_entry_points
import sys

import click
from click_plugins import with_plugins
import cligj

import mapbox


def configure_logging(verbosity):
    log_level = max(10, 30 - 10*verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


@with_plugins(ep for ep in list(iter_entry_points('mapbox.mapbox_commands')))
@click.group()
@click.option('--access-token', help="Your Mapbox access token.")
@cligj.verbose_opt
@click.version_option(version=mapbox.__version__, message='%(version)s')
@cligj.quiet_opt
@click.pass_context
def main_group(ctx, verbose, quiet, access_token):
    """This is the command line interface to Mapbox web services.

    Mapbox web services require an access token. Your token is shown
    on the https://www.mapbox.com/developers/api/ page when you are
    logged in. The token can be provided on the command line

      $ mbx --access-token MY_TOKEN ...

    or as an environment variable named MAPBOX_ACCESS_TOKEN or 
    MapboxAccessToken.

    \b
      $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
      $ mbx ...

    """
    verbosity = verbose - quiet
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj['verbosity'] = verbosity
    ctx.obj['access_token'] = access_token
