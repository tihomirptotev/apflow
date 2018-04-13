from marshmallow import fields, ValidationError, validates
from marshmallow import Schema, post_load
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm.exc import NoResultFound
from apflow.schemas.base_schema import BaseAuditSchema, BaseSchema
from .models import Counterparty, CounterpartyNote


class CounterpartyNoteSchema(ModelSchema, BaseAuditSchema):

    url = fields.Method('self_url', dump_omly=True)

    def self_url(self, obj):
        return self.request.route_url(
            self.detail_route_name,
            id=obj.counterparty_id,
            note_id=obj.id)

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
            fields = ('name', 'eik_egn', 'url', 'notes')

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
