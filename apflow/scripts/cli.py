import os
import sys
import transaction
import click

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models import MyModel


@click.group()
@click.argument('config-uri')
@click.pass_context
def main(ctx, config_uri):
    if ctx.obj is None:
        ctx.obj = dict()
    click.echo('This is the main script.')
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)
    ctx.obj['SESSION_FACTORY'] = session_factory


@main.group()
@click.pass_context
def db(ctx):
    pass


@db.command()
@click.pass_context
def init(ctx):
    '''Sample script'''

    with transaction.manager:
        dbsession = get_tm_session(
            ctx.obj['SESSION_FACTORY'], transaction.manager)

        model = MyModel(name='e', value=8)
        dbsession.add(model)
