import logging
from typing import Union, List
from unittest.mock import Mock

from odoo.addons.pc_edi_account.models.edi_invoice_deserializer import EdiInvoiceDeserializer
from odoo.addons.pc_edi_account.models.edi_invoice_serializer import EdiInvoiceSerializer
from odoo.addons.pc_edi_account.models.edi_receiver_transport import EdiReceiverTransport
from odoo.addons.pc_edi_account.models.edi_sender_transport import EdiSenderTransport
from odoo.addons.pc_edi_account.models.edi_settings_finder import EdiSettingsFinder
from odoo.addons.pc_edi_account.models.sftp_edi_files_finder import SftpEdiFilesFinder
from odoo.models import Model

EdiDocument = str

logger = logging.getLogger(__name__)

INVOICE_MODEL = 'account.move'


class AccountMove(Model):
    _name = INVOICE_MODEL
    _inherit = [INVOICE_MODEL, 'edi.document.interface', 'edi.transport.interface']

    def serialize(self, invoice_serializer: Union[EdiInvoiceSerializer, Mock]) -> EdiDocument:
        return invoice_serializer.serialize()

    def deserialize(self, invoice_deserializer: Union[EdiInvoiceDeserializer, Mock]) -> Model:
        return invoice_deserializer.deserialize()

    def send(self, sender: Union[EdiSenderTransport, Mock]) -> None:
        sender.send()

    def receive(self, receiver: Union[EdiReceiverTransport, Mock]) -> List[EdiDocument]:
        return receiver.receive()

    def send_edi_invoice_by_ftp(self):
        settings = EdiSettingsFinder(
            partner_id=self.partner_id,
            env=self.env
        ).find()

        parameters = settings.parameters

        self.send(
            sender=settings.sender_transport_class(
                edi_document=self.serialize(
                    invoice_serializer=settings.serializer_class(
                        model=self
                    )
                ),
                settings=parameters
            )
        )

    def receive_edi_invoices_by_ftp(self):
        settings = EdiSettingsFinder(
            partner_id=self.partner_id,
            env=self.env
        ).find()

        parameters = settings.parameters
        logger.info('Settings parameters: %s', parameters)

        edi_documents = self.receive(
            receiver=settings.receiver_transport_class(
                settings=parameters,
                files=SftpEdiFilesFinder(
                    settings=parameters
                ).find()
            )
        )

        logger.info('Received EDI documents: %s', edi_documents)

        for document in edi_documents:
            self.deserialize(
                invoice_deserializer=settings.deserializer_class(
                    edi_document=EdiDocument(document),
                    account_move_model=self.env[INVOICE_MODEL]
                )
            )
