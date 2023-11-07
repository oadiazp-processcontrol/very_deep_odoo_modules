import logging
import os.path
from pathlib import Path
from unittest.mock import Mock

from odoo.addons.pc_edi_account.models.raw_edi_invoice_deserializer import RawEdiInvoiceDeserializer
from odoo.tests import TransactionCase

logger = logging.getLogger(__name__)

INVOICE_MODEL = 'account.move'
EdiDocument = str


class TestAccountMove(TransactionCase):

    def setUp(self):
        super().setUp()
        self.account = self.env['account.account'].create({
            'name': 'Account Name',
            'code': 'ACCOUNT',
            'company_id': self.env.company.id,
        })
        self.journal = self.env['account.journal'].create({
            'name': 'Journal Name',
            'type': 'sale',
            'code': 'SALE',
            'company_id': self.env.company.id,
        })

    def test_basic_serialize(self):
        partner = self.env['res.partner'].search([([
            'name', '!=', None
        ])], limit=1)
        products = self.env['product.product'].search([([
            'name', '!=', None
        ])], limit=3)

        invoice = self.env[INVOICE_MODEL].create({
            'partner_id': partner.id,
            'journal_id': self.journal.id,
            'invoice_date': '2020-1-1',
            'invoice_line_ids': [
                (0, 0, {
                    'name': products[0].name,
                    'quantity': 1,
                    'price_unit': products[0].lst_price,
                    'account_id': self.account.id,
                    'product_id': products[0].id
                }),
                (0, 0, {
                    'name': products[1].name,
                    'quantity': 2,
                    'price_unit': products[1].lst_price,
                    'account_id': self.account.id,
                    'product_id': products[1].id
                }),
                (0, 0, {
                    'name': products[2].name,
                    'quantity': 2,
                    'price_unit': products[2].lst_price,
                    'account_id': self.account.id,
                    'product_id': products[2].id
                }),
            ],
        })

        """
        This is a practical example of how to use the serialize method of the EdiInvoiceSerializer
        raw_edi_invoice_serializer = RawEdiInvoiceSerializer(invoice)        
        logger.info("EDI encoded invoice: %s", invoice.serialize(invoice_serializer=raw_edi_invoice_serializer))
        """

        invoice_serializer_mock = Mock()

        invoice.serialize(invoice_serializer=invoice_serializer_mock)
        invoice_serializer_mock.serialize.assert_called_once()

    def test_basic_deserialize(self):
        current_file_path = __file__
        parent_dir_path = Path(current_file_path).parent
        test_edi_file = os.path.join(parent_dir_path, 'edi_examples', 'basic_invoice.edi')

        with open(test_edi_file, 'r') as f:
            edi_document = f.read()
            deserialized_model = self.env[INVOICE_MODEL].deserialize(
                invoice_deserializer=RawEdiInvoiceDeserializer(
                    edi_document=edi_document,
                    account_move_model=self.env[INVOICE_MODEL]
                )
            )

            self.assertEqual(deserialized_model.name, '1060113800026')
            self.assertEqual(deserialized_model.partner_id.name, 'VAUXHALL MOTORS LTD')
            self.assertEqual(deserialized_model.amount_total, 1960.29)
            self.assertEqual(len(deserialized_model.invoice_line_ids), 1)
            self.assertEqual(deserialized_model.invoice_line_ids[0].name, '090346642')

    def test_upload_edi_document_to_sftp(self):
        """
        This is a practical example of how to use the send method of the EdiSenderTransport

        current_file_path = __file__
        parent_dir_path = Path(current_file_path).parent
        test_edi_file = os.path.join(parent_dir_path, 'edi_examples', 'basic_invoice.edi')

        with open(test_edi_file, 'r') as f:
            edi_document = f.read()
            self.env['account.move'].send(
                sender=SftpEdiSenderTransport(
                    edi_document=EdiDocument(edi_document),
                    settings={
                        'host': 'localhost',
                        'port': 2222,
                        'username': 'foo',
                        'password': 'pass',
                        'sent_invoices_path': 'upload/sent/invoices'
                    }
                )
            )
        """

        sftp_edi_sender_transport_mock = Mock()
        self.env[INVOICE_MODEL].send(sender=sftp_edi_sender_transport_mock)
        sftp_edi_sender_transport_mock.send.assert_called_once()

    def test_download_edi_document_from_sftp(self):
        """
        This is a practical example of how to use the receive method of the EdiReceiverTransport
        self.env['account.move'].receive(
            receiver=SftpEdiReceiverTransport(
                settings={
                    'host': 'localhost',
                    'port': 2222,
                    'username': 'foo',
                    'password': 'pass',
                    'received_invoices_path': 'upload/sent/invoices'
                },
                files=SftpEdiFilesFinder(
                    settings={
                        'host': 'localhost',
                        'port': 2222,
                        'username': 'foo',
                        'password': 'pass',
                        'received_invoices_path': 'upload/sent/invoices'
                    }
                ).find()
            )
        )
        """

        sftp_edi_receiver_transport_mock = Mock()
        self.env[INVOICE_MODEL].receive(receiver=sftp_edi_receiver_transport_mock)
        sftp_edi_receiver_transport_mock.receive.assert_called_once()
