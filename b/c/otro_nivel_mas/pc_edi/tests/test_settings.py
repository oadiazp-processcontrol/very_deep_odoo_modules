from odoo.addons.pc_edi_account.models.raw_edi_invoice_deserializer import RawEdiInvoiceDeserializer
from odoo.addons.pc_edi_account.models.raw_edi_invoice_serializer import RawEdiInvoiceSerializer
from odoo.addons.pc_edi_account.models.sftp_edi_receiver_transport import SftpEdiReceiverTransport
from odoo.addons.pc_edi_account.models.sftp_edi_sender_transport import SftpEdiSenderTransport
from odoo.exceptions import UserError
from odoo.tests import TransactionCase

SETTINGS_MODEL = 'edi.settings'


class TestSettings(TransactionCase):
    def test_default_should_be_unique(self):
        self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'webservice',
            'parameters': '{}',
            'default': True,
        })
        with self.assertRaises(UserError):
            self.env[SETTINGS_MODEL].create({
                'format': 'raw',
                'transport': 'webservice',
                'parameters': '{}',
                'default': True,
            })

    def test_invalid_json(self):
        with self.assertRaises(UserError):
            self.env[SETTINGS_MODEL].create({
                'format': 'json',
                'transport': 'webservice',
                'parameters': 'this is not a json',
                'default': True,
            })

    def test_partner_id_should_be_unique(self):
        partner = self.env['res.partner'].create({
            'name': 'Partner Name'
        })

        self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'webservice',
            'parameters': '{}',
            'default': False,
            'partner_id': partner.id,
        })
        with self.assertRaises(UserError):
            self.env[SETTINGS_MODEL].create({
                'format': 'raw',
                'transport': 'webservice',
                'parameters': '{}',
                'default': False,
                'partner_id': partner.id,
            })

    def test_cant_be_default_and_partner(self):
        partner = self.env['res.partner'].create({
            'name': 'Partner Name'
        })

        with self.assertRaises(UserError):
            self.env[SETTINGS_MODEL].create({
                'format': 'raw',
                'transport': 'webservice',
                'parameters': '{}',
                'default': True,
                'partner_id': partner.id,
            })

    def test_should_be_at_least_partner_or_default(self):
        with self.assertRaises(UserError):
            self.env[SETTINGS_MODEL].create({
                'format': 'raw',
                'transport': 'webservice',
                'parameters': '{}',
                'default': False,
                'partner_id': False,
            })

    def test_sender_transport_class_depends_on_the_transport_attr(self):
        setting = self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'sftp',
            'parameters': '{}',
            'default': True,
            'partner_id': False,
        })

        self.assertEqual(setting.sender_transport_class, SftpEdiSenderTransport)

        setting.transport = 'webservice'
        self.assertIsNone(setting.sender_transport_class)

    def test_receiver_transport_class_depends_on_the_transport_attr(self):
        setting = self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'sftp',
            'parameters': '{}',
            'default': True,
            'partner_id': False,
        })

        self.assertEqual(setting.receiver_transport_class, SftpEdiReceiverTransport)

        setting.transport = 'webservice'
        self.assertIsNone(setting.receiver_transport_class)

    def test_edi_serializer_class_depends_on_the_format_attr(self):
        setting = self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'sftp',
            'parameters': '{}',
            'default': True,
            'partner_id': False,
        })
        self.assertEqual(setting.serializer_class, RawEdiInvoiceSerializer)

        setting.format = 'json'
        self.assertIsNone(setting.serializer_class)

    def test_edi_deserializer_class_depends_on_the_format_attr(self):
        setting = self.env[SETTINGS_MODEL].create({
            'format': 'raw',
            'transport': 'sftp',
            'parameters': '{}',
            'default': True,
            'partner_id': False,
        })
        self.assertEqual(setting.deserializer_class, RawEdiInvoiceDeserializer)

        setting.format = 'json'
        self.assertIsNone(setting.deserializer_class)
