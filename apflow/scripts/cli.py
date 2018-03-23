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
from ..models import Counterparty, CounterpartyNote


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
    ctx.obj['ENGINE'] = engine


@main.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@main.group()
@click.pass_context
def db(ctx):
    pass


@db.command()
@click.pass_context
def init(ctx):
    '''Initialize database'''
    Base.metadata.create_all(ctx.obj['ENGINE'])
    # with transaction.manager:
    #     dbsession = get_tm_session(
    #         ctx.obj['SESSION_FACTORY'], transaction.manager)

    #     counterparty = Counterparty(name='Доставчик 1',
    #                                 eik_egn='1234567809',
    #                                 created_by=1,
    #                                 updated_by=1,
    #                                 id=2)
    #     dbsession.add(counterparty)
    # pass


@db.command()
@click.pass_context
def drop_all(ctx):
    '''Drop all tables from database.'''
    Base.metadata.drop_all(ctx.obj['ENGINE'])
