# Skeleton of a CLI

import click

import riomucho


@click.command('riomucho')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(riomucho.has_legs)
