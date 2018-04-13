import functools
from pyramid.httpexceptions import HTTPNotFound
from apflow.views.base_api import model_factory
from .models import ApDocument, ApDocCostDistribution


apdoc_factory = functools.partial(model_factory, model=ApDocument)


def apdoc_cd_factory(request):
    """ Creates route factory for the provided model. """
    apdoc_id = request.matchdict.get('id')
    cd_id = request.matchdict.get('cd_id')
    if cd_id is None:
        # Return the class
        return ApDocCostDistribution
    obj = request.dbsession.query(
        ApDocCostDistribution).filter_by(
            id=int(cd_id),
            apdoc_id=int(apdoc_id)).first()
    if not obj:
        raise HTTPNotFound()
    return obj
