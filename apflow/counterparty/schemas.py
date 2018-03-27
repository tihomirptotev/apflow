from marshmallow import fields, ValidationError, validates
from marshmallow import Schema
from .models import Counterparty


class CounterpartySchema(Schema):
    name = fields.String(required=True)
    eik_egn = fields.String(required=True)
    url = fields.Url(dump_only=True)

    @validates('eik_egn')
    def validates_eik_egn(self, value):
        if len(value) < 9:
            raise ValidationError('Length must be at least 9 characters.')
        if len(value) > 13:
            raise ValidationError('Length must be less than 14 characters.')


