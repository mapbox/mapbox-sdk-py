import logging
import json

import click

import mapbox
from mapbox.datasets import batch, iter_features


class MapboxCLIException(click.ClickException):
    pass


@click.command(short_help="Create an empty dataset")
@click.argument('owner')
@click.option('--name')
@click.option('--description')
@click.pass_context
def create_dataset(ctx, owner, name, description):
    """Create a new empty dataset."""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    datasets = mapbox.Datasets(owner, access_token=access_token)
    properties = {}
    if name:
        properties['name'] = name
    if description:
        properties['description'] = description
    resp = datasets.create(**properties)
    click.echo(resp.text)


@click.command(short_help="List datasets")
@click.argument('owner')
@click.pass_context
def ls_datasets(ctx, owner):
    """List datasets."""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    datasets = mapbox.Datasets(owner, access_token=access_token)
    resp = datasets.list()
    click.echo(resp.text)


@click.command(short_help="Get a dataset's features")
@click.argument('owner')
@click.argument('id')
@click.option('--output', '-o', default='-', help="Save output to a file.")
@click.pass_context
def retrieve_features(ctx, owner, id, output):
    """Return features as GeoJSON."""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    stdout = click.open_file(output, 'w')

    dataset = mapbox.Dataset(owner, id, access_token=access_token)
    resp = dataset.retrieve_features()
    click.echo(resp.text, file=stdout)


@click.command(short_help="Update a dataset's features")
@click.argument('owner')
@click.argument('id')
@click.option(
    '--sequence / --no-sequence', default=False,
    help="Specify whether the input stream is a LF-delimited sequence of GeoJSON "
         "features (the default) or a single GeoJSON feature collection.")
@click.pass_context
def update_features(ctx, owner, id, sequence):
    """Update a dataset's features from provided GeoJSON."""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    dataset = mapbox.Dataset(owner, id, access_token=access_token)

    stdin = click.get_text_stream('stdin')
    for update_batch in batch(iter_features(stdin, is_sequence=sequence)):
        payload = {'put': list(update_batch)}
        logger.debug("Payload: %r", payload)
        resp = dataset.update_features(**payload)
