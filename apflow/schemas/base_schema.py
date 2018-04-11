from marshmallow import fields, ValidationError, validates
from marshmallow import Schema


class BaseSchema(Schema):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.detail_route_name = kwargs.pop('detail_route_name', None)
        super().__init__(*args, **kwargs)
        # self.request = request
        # self.detail_route_name = detail_route_name

    url = fields.Method('self_url')

    def self_url(self, obj):
        return self.request.route_url(self.detail_route_name, id=obj.id)
        # return self.context['request'].route_url(
        #     self.context['detail_route_name'], id=obj.id)


class BaseAuditSchema(BaseSchema):

    created_by = fields.Integer(dump_only=True)
    updated_by = fields.Integer(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
