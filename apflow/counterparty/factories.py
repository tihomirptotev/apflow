import functools
from pyramid.httpexceptions import HTTPNotFound
from apflow.views.base_api import model_factory
from .models import Counterparty, CounterpartyNote, CounterpartyAccount


counterparty_factory = functools.partial(model_factory, model=Counterparty)
# counterparty_note_factory = functools.partial(model_factory,
#                                               model=CounterpartyNote)
counterparty_account_factory = functools.partial(model_factory,
                                                 model=CounterpartyAccount)


def counterparty_note_factory(request):
    """ Creates route factory for the provided model. """
    counterparty_id = request.matchdict.get('id')
    note_id = request.matchdict.get('note_id')
    if note_id is None:
        # Return the class
        return CounterpartyNote
    obj = request.dbsession.query(
        CounterpartyNote).filter_by(
            id=int(note_id),
            counterparty_id=int(counterparty_id),
            deleted=False).first()
    if not obj:
        raise HTTPNotFound()
    return obj
