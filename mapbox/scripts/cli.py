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
@cligj.verbose_opt
@cligj.quiet_opt
@click.version_option(version=mapbox.__version__, message='%(version)s')
@click.pass_context
def main_group(ctx, verbose, quiet):
    """Mapbox command line interface.
    """
    verbosity = verbose - quiet
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj['verbosity'] = verbosity

if __name__ == '__main__':
    main_group()