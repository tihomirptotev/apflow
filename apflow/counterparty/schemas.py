from marshmallow import fields, ValidationError, validates
from marshmallow import Schema
from .models import Counterparty
from sqlalchemy.orm.exc import NoResultFound


class CounterpartySchema(Schema):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.request = None

    name = fields.String(required=True)
    eik_egn = fields.String(required=True)
    url = fields.Url(dump_only=True)
    dbsession = None

    @validates('eik_egn')
    def validates_eik_egn(self, value):
        if len(value) < 9:
            raise ValidationError('Length must be at least 9 characters.')
        if len(value) > 13:
            raise ValidationError('Length must be less than 14 characters.')

        try:
            obj = Counterparty.find_by_col_name(
                self.dbsession, 'eik_egn', value)
            if obj:
                raise ValidationError(
                    f'Counterparty with eik_egn: {value} already exsts.')
        except NoResultFound:
            pass
