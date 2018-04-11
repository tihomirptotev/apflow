from marshmallow import fields, ValidationError, validates
from marshmallow import Schema, post_load
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm.exc import NoResultFound
from apflow.schemas.base_schema import BaseAuditSchema, BaseSchema
from .models import Counterparty, CounterpartyNote


class CounterpartyNoteSchema(ModelSchema, BaseAuditSchema):

    class Meta:
        model = CounterpartyNote
        fields = ('id', 'note', 'url')


def counterparty_schema_factory(request):

    class CounterpartySchema(ModelSchema, BaseAuditSchema):
        notes = fields.Nested(CounterpartyNoteSchema(
            request=request, detail_route_name='counterparty_note_view'),
            many=True)

        class Meta:
            model = Counterparty

        # name = fields.String(required=True)
        # eik_egn = fields.String(required=True)

        @validates('eik_egn')
        def validates_eik_egn(self, value):
            if not (9 <= len(value) <= 13):
                raise ValidationError('Length must be between 9 and 13 characters.')

            try:
                obj = Counterparty.find_by_col_name(
                    self.request.dbsession, 'eik_egn', value)
                if obj:
                    raise ValidationError(
                        f'Counterparty with eik_egn: {value} already exsts.')
            except NoResultFound:
                pass

    return CounterpartySchema(request=request,
                              detail_route_name='counterparty_view')


# class CounterpartyNoteSchema(Schema):
#     note = fields.String(required=True)
#     created_by = fields.Integer()
#     updated_by = fields.Integer()
#     created_on = fields.DateTime()
#     updated_on = fields.DateTime()




# class CounterpartySchema(BaseAuditSchema):

#     name = fields.String(required=True)
#     eik_egn = fields.String(required=True)
#     notes = fields.Nested(CounterpartyNoteSchema())

#     @validates('eik_egn')
#     def validates_eik_egn(self, value):
#         if not (9 <= len(value) <= 13):
#             raise ValidationError('Length must be between 9 and 13 characters.')

#         try:
#             obj = Counterparty.find_by_col_name(
#                 self.context['request'].dbsession, 'eik_egn', value)
#             if obj:
#                 raise ValidationError(
#                     f'Counterparty with eik_egn: {value} already exsts.')
#         except NoResultFound:
#             pass
