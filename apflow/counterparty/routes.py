def includeme(config):
    config.add_route('counterparty', '/',
                     factory='.factories.counterparty_factory')

    config.add_route('counterparty_view',
                     '/{id}', factory='.factories.counterparty_factory')

    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty',
                    request_method='GET',
                    permission='read',
                    attr='list_all')

    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty',
                    request_method='POST',
                    permission='crud',
                    attr='add')

    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='GET',
                    permission='read',
                    attr='view')

    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='PUT',
                    permission='crud',
                    attr='update')

    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='DELETE',
                    permission='crud',
                    attr='delete')

    config.add_route('counterparty_notes', '/{id}/notes',
                     factory='.factories.counterparty_factory')

    config.add_route('counterparty_note_view',
                     '/{id}/notes/{note_id}',
                     factory='.factories.counterparty_note_factory')

    config.add_view('apflow.counterparty.api.CounterpartyNoteApi',
                    route_name='counterparty_note_view',
                    request_method='GET',
                    permission='read',
                    attr='view')

    config.add_view('apflow.counterparty.api.CounterpartyNoteApi',
                    route_name='counterparty_note_view',
                    request_method='PUT',
                    permission='crud',
                    attr='update')

    config.add_view('apflow.counterparty.api.CounterpartyNoteApi',
                    route_name='counterparty_note_view',
                    request_method='DELETE',
                    permission='crud',
                    attr='delete')

# TODO: Add permissions
