from marshmallow_sqlalchemy import ModelSchema
from .models import Counterparty


class CounterpartySchema(ModelSchema):
    class Meta:
        model = Counterparty


