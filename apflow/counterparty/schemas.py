from marshmallow import fields, ValidationError, validates
from marshmallow import Schema, post_load
from sqlalchemy.orm.exc import NoResultFound
from apflow.schemas.base_schema import BaseAuditSchema, BaseSchema
from .models import Counterparty


class CounterpartySchema(BaseAuditSchema):

    name = fields.String(required=True)
    eik_egn = fields.String(required=True)

    @validates('eik_egn')
    def validates_eik_egn(self, value):
        if not (9 <= len(value) <= 13):
            raise ValidationError('Length must be between 9 and 13 characters.')

        try:
            obj = Counterparty.find_by_col_name(
                self.context['request'].dbsession, 'eik_egn', value)
            if obj:
                raise ValidationError(
                    f'Counterparty with eik_egn: {value} already exsts.')
        except NoResultFound:
            pass
