from marshmallow import fields, ValidationError, validates
from marshmallow import Schema


class BaseSchema(Schema):

    url = fields.Method('self_url')

    def self_url(self, obj):
        return self.context['request'].route_url(
            self.context['detail_route_name'], id=obj.id)


class BaseAuditSchema(BaseSchema):

    created_by = fields.Integer()
    updated_by = fields.Integer()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
