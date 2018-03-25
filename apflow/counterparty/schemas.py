from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from .models import Counterparty


class CounterpartySchema(ModelSchema):
    url = fields.Url()
    class Meta:
        model = Counterparty


