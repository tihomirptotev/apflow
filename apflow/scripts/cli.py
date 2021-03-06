import os
import sys
import transaction
import click
import openpyxl

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
from ..models import (
    Counterparty,
    CounterpartyNote,
    User,
    Role,
    Employee,
    CompanyUnit,
    ApDocument,
    ApDocCostDistribution,
    CostAccount,
)


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
    with transaction.manager:
        dbsession = get_tm_session(
            ctx.obj['SESSION_FACTORY'], transaction.manager)
        user = User(username='admin', email='admin@local.host',
                    password='password')
        role = Role(name='admins', description='admins description')
        user.roles.append(role)
        dbsession.add(user)
        # dbsession.flush()

@db.command()
@click.pass_context
def init_sample_data(ctx):
    '''Initialize database with samlpe data'''
    Base.metadata.create_all(ctx.obj['ENGINE'])
    wb = openpyxl.load_workbook('apflow/tests/data/test_data.xlsx')

    with transaction.manager:
        dbsession = get_tm_session(
            ctx.obj['SESSION_FACTORY'], transaction.manager)
        user = User(username='admin', email='admin@local.host',
                    password='password')
        role = Role(name='admins', description='admins description')
        user.roles.append(role)
        dbsession.add(user)
        dbsession.flush()

        models_list = [Role, User, CompanyUnit, Employee, Counterparty,
                       CounterpartyNote, CostAccount, ApDocument,
                       ApDocCostDistribution]
        for model_name in models_list:
            sheetname = model_name.__tablename__
            ws = wb[sheetname]
            data = [tuple(cell.value for cell in row) for row in ws.rows]
            columns = data[0]
            data_as_dict = [dict(zip(columns, row)) for row in data[1:]]
            for item in data_as_dict:
                obj = model_name(**item)
                if model_name == User:
                    obj.password = 'password'
                dbsession.add(obj)
            dbsession.flush()

        ws = wb['roles_users']
        data = [tuple(cell.value for cell in row) for row in ws.rows][1:]
        for row in data:
            user = User.get_by_id(dbsession, row[0])
            role = Role.get_by_id(dbsession, row[1])
            user.roles.append(role)
            # import ipdb; ipdb.set_trace()
            dbsession.add(user)
        dbsession.flush()




@db.command()
@click.pass_context
def drop_all(ctx):
    '''Drop all tables from database.'''
    Base.metadata.drop_all(ctx.obj['ENGINE'])
