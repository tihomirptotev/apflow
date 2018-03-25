class ModelService:
    model = None
    schema = None
    route_view_name = None

    def __init__(self, request):
        self.request = request
        self.user_id = 1

    def list_all(self):
        session = self.request.dbsession
        return session.query(self.model)

    def get_by_id(self, id):
        session = self.request.dbsession
        return session.query(self.model).filter_by(id=id).one()

    def create(self, json_data=None, **data):
        if json_data:
            obj = self.deserialize_single(json_data)
        else:
            obj = self.model(**data)
        obj.created_by = self.user_id
        obj.updated_by = self.user_id
        self.request.dbsession.add(obj)
        self.request.dbsession.flush()
        return obj

    def update(self, id, **data):
        pass

    def delete(self, id):
        pass

    def url_for_id(self, id):
        return self.request.route_url(self.route_view_name, id=id)

    def serialize_single(self, obj):
        res = self.schema.dump(obj).data
        res['url'] = self.url_for_id(obj.id)
        return res

    def deserialize_single(self, json_data):
        res = self.schema.load(json_data, session=self.request.dbsession)
        return res.data


    def serialize_multiple(self, obj_list):
        return [self.serialize_single(obj) for obj in obj_list]

