import functools
from apflow.views.base_api import model_factory
from .models import Counterparty, CounterpartyNote, CounterpartyAccount


counterparty_factory = functools.partial(model_factory, model=Counterparty)
counterparty_note_factory = functools.partial(model_factory,
                                              model=CounterpartyNote)
counterparty_account_factory = functools.partial(model_factory,
                                                 model=CounterpartyAccount)
