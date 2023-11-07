import json

from odoo.addons.pc_edi_account.models.raw_edi_invoice_deserializer import RawEdiInvoiceDeserializer
from odoo.addons.pc_edi_account.models.raw_edi_invoice_serializer import RawEdiInvoiceSerializer
from odoo.addons.pc_edi_account.models.sftp_edi_receiver_transport import SftpEdiReceiverTransport
from odoo.addons.pc_edi_account.models.sftp_edi_sender_transport import SftpEdiSenderTransport
from odoo.api import constrains
from odoo.exceptions import UserError
from odoo.fields import Selection, Many2one, Boolean, Text
from odoo.models import Model

TRANSPORT_SENDER_FACTORY_DICT = {
    'sftp': SftpEdiSenderTransport,
    'webservice': None
}

TRANSPORT_RECEIVER_FACTORY_DICT = {
    'sftp': SftpEdiReceiverTransport,
    'webservice': None
}

FORMAT_SERIALIZER_FACTORY_DICT = {
    'raw': RawEdiInvoiceSerializer,
    'json': None,
}

FORMAT_DESERIALIZER_FACTORY_DICT = {
    'raw': RawEdiInvoiceDeserializer,
    'json': None,
}


class Settings(Model):
    _name = 'edi.settings'
    _description = 'EDI Settings'

    format = Selection(selection=[
        ('raw', 'Raw'),
        ('json', 'Json'),
    ])
    transport = Selection(
        selection=[
            ('webservice', 'Webservice'),
            ('sftp', 'SFTP'),
        ]
    )
    parameters = Text()
    default = Boolean()
    partner_id = Many2one('res.partner')

    @constrains('default')
    def _check_default(self):
        default_settings_amount = self.search_count([('default', '=', True), ('id', '!=', self.id)])

        if self.default and default_settings_amount > 0:
            raise UserError('Only one default settings is allowed')

    @constrains('parameters')
    def _check_parameters_should_be_a_valid_json(self):
        try:
            json.loads(self.parameters)
        except json.decoder.JSONDecodeError:
            raise UserError('Invalid json format')

    @constrains('partner_id')
    def _check_should_be_just_a_setting_by_partner(self):
        partner_settings_amount = self.search_count([('partner_id', '=', self.partner_id.id), ('id', '!=', self.id)])

        if self.partner_id and partner_settings_amount > 0:
            raise UserError('Only one settings per partner is allowed')

    @constrains('default', 'partner_id')
    def _check_cant_be_default_and_partner(self):
        if self.default and self.partner_id:
            raise UserError('A default setting can not be a partner setting')

    @constrains('default', 'partner_id')
    def _check_should_be_default_or_partner(self):
        if not self.default and not self.partner_id:
            raise UserError('A setting should be default or partner')

    @property
    def sender_transport_class(self):
        return TRANSPORT_SENDER_FACTORY_DICT[self.transport]

    @property
    def receiver_transport_class(self):
        return TRANSPORT_RECEIVER_FACTORY_DICT[self.transport]

    @property
    def serializer_class(self):
        return FORMAT_SERIALIZER_FACTORY_DICT[self.format]

    @property
    def deserializer_class(self):
        return FORMAT_DESERIALIZER_FACTORY_DICT[self.format]


