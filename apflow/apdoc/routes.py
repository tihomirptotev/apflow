def includeme(config):
    config.add_route('apdoc', '/',
                     factory='.factories.apdoc_factory')

    config.add_route('apdoc_view',
                     '/{id}', factory='.factories.apdoc_factory')

    config.add_route('apdoc_cd_view',
                     '{id}/cd/{cd_id}', factory='.factories.apdoc_cd_factory')

    config.add_view('apflow.apdoc.api.ApDocApi',
                    route_name='apdoc',
                    request_method='GET',
                    permission='read',
                    attr='list_all')

    config.add_view('apflow.apdoc.api.ApDocApi',
                    route_name='apdoc_view',
                    request_method='GET',
                    permission='read',
                    attr='view')
