from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class ModelService:

    class Meta:
        model = None
        schema = None
        route_view_name = None

    def __init__(self, request):
        self.request = request
        self.model = getattr(self.Meta, 'model')
        self.schema = getattr(self.Meta, 'schema')
        self.route_view_name = getattr(self.Meta, 'route_view_name')
        self.user_id = 1

    def list_all(self):
        session = self.request.dbsession
        return session.query(self.model)

    def get_by_id(self, id):
        session = self.request.dbsession
        try:
            return session.query(self.model).filter_by(id=id).one()
        except NoResultFound:
            return dict(
                result='error',
                message=f'Object with id: {id} does not exist.')

    def find_by_col_name(self, col_name, value):
        session = self.request.dbsession
        col = getattr(self.model, col_name)
        return session.query(self.model).filter(col==value)

    def create(self, **data):
        obj = self.model(**data)
        obj.created_by = self.user_id
        obj.updated_by = self.user_id
        try:
            self.request.dbsession.add(obj)
            self.request.dbsession.flush()
            return obj
        except IntegrityError as e:
            return dict(
                result='error',
                message='Object not created. Data does not meet the constrains.')

    def create_many(self, data_list):
        for data in data_list:
            obj = self.model(**data)
            obj.created_by = self.user_id
            obj.updated_by = self.user_id
            self.request.dbsession.add(obj)
        self.request.dbsession.flush()
        return

    def update(self, id, data_dict):
        obj = self.get_by_id(id)
        if isinstance(obj, self.model):
            for k, v in data_dict.items():
                setattr(obj, k, v)
            self.request.dbsession.add(obj)
            self.request.dbsession.flush()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if isinstance(obj, self.model):
            self.request.dbsession.delete(obj)
            self.request.dbsession.flush()
            return self.serialize_single(obj)
        return obj

    def url_for_id(self, id):
        return self.request.route_url(self.route_view_name, id=id)

    def serialize_single(self, obj):
        res = self.schema.dump(obj).data
        res['url'] = self.url_for_id(obj.id)
        return res

    def deserialize_single(self, json_data):
        res = self.schema.load(json_data)
        return res


    def serialize_multiple(self, obj_list):
        return [self.serialize_single(obj) for obj in obj_list]

