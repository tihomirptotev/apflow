def includeme(config):
    config.add_route('login', '/login', factory='.models.user_factory')
    config.add_route('signup', '/signup', factory='.models.user_factory')

    config.add_route('user', '/', factory='.models.user_factory')
    config.add_route('user_view', '/{id}', factory='.models.user_factory')
    config.add_view('apflow.user.api.UserApi',
                    route_name='user',
                    request_method='GET',
                    permission='read',
                    attr='list_all')
    config.add_view('apflow.user.api.UserApi',
                    route_name='user_view',
                    request_method='GET',
                    permission='read',
                    attr='view')
    # config.add_view('apflow.counterparty.api.CounterpartyApi',
    #                 route_name='counterparty',
    #                 request_method='POST',
    #                 permission='crud',
    #                 attr='add')
    # config.add_view('apflow.counterparty.api.CounterpartyApi',
    #                 route_name='counterparty_view',
    #                 request_method='GET',
    #                 permission='read',
    #                 attr='view')
    # config.add_view('apflow.counterparty.api.CounterpartyApi',
    #                 route_name='counterparty_view',
    #                 request_method='PUT',
    #                 permission='crud',
    #                 attr='update')
    # config.add_view('apflow.counterparty.api.CounterpartyApi',
    #                 route_name='counterparty_view',
    #                 request_method='DELETE',
    #                 permission='crud',
    #                 attr='delete')

# TODO: Add permissions
