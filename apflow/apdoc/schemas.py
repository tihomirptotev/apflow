from marshmallow import fields, ValidationError, validates
from marshmallow import Schema, post_load
from marshmallow_sqlalchemy import ModelSchema
# import simplejson as json
from sqlalchemy.orm.exc import NoResultFound
from apflow.schemas.base_schema import BaseAuditSchema, BaseSchema
from .models import ApDocument, ApDocCostDistribution, CostAccount
from apflow.company.models import CompanyUnit


class ApDocCostDistributionSchema(ModelSchema, BaseAuditSchema):

    url = fields.Method('self_url', dump_omly=True)
    account = fields.Method('self_account', dump_only=True)
    unit = fields.Method('self_unit', dump_only=True)

    def self_url(self, obj):
        return self.request.route_url(
            self.detail_route_name,
            id=obj.id)

    def self_account(self, obj):
        return self.request.dbsesion(CostAccount).get(obj.cost_account_id).name

    def self_unit(self, obj):
        return self.request.dbsesion(CompanyUnit).get(obj.company_unit_id).name

    class Meta:
        model = ApDocCostDistribution
        fields = ('id', 'apdoc_id', 'account', 'unit', 'amount', 'url')


def apdoc_schema_factory(request):

    class ApDocSchema(ModelSchema, BaseAuditSchema):
        cd_entries = fields.Nested(ApDocCostDistributionSchema(
            request=request, detail_route_name='apdoc_cd_view'),
            many=True)
        doc_sum = fields.Float()

        class Meta:
            model = ApDocument
            fields = ('counterparty_id', 'doc_number', 'doc_date', 'doc_sum',
                      'doc_info', 'doc_info_additional', 'doc_type', 'level',
                      'status', 'cd_entries', 'url')

        # TODO: add validation
        # @validates('eik_egn')
        # def validates_eik_egn(self, value):
        #     if not (9 <= len(value) <= 13):
        #         raise ValidationError(
        #             'Length must be between 9 and 13 characters.')

        #     try:
        #         obj = Counterparty.find_by_col_name(
        #             self.request.dbsession, 'eik_egn', value)
        #         if obj:
        #             raise ValidationError(
        #                 f'Counterparty with eik_egn: {value} already exsts.')
        #     except NoResultFound:
        #         pass

    return ApDocSchema(request=request,
                              detail_route_name='apdoc_view')
