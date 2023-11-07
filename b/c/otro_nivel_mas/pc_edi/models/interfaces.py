from typing import Union, List
from unittest.mock import Mock

from odoo.addons.pc_edi_account.models.edi_invoice_deserializer import EdiInvoiceDeserializer
from odoo.addons.pc_edi_account.models.edi_invoice_serializer import EdiInvoiceSerializer
from odoo.addons.pc_edi_account.models.edi_receiver_transport import EdiReceiverTransport
from odoo.addons.pc_edi_account.models.edi_sender_transport import EdiSenderTransport
from odoo.models import Model, AbstractModel

EdiDocument = str


class EdiDocumentInterface(AbstractModel):
    _name = 'edi.document.interface'
    _description = 'EDI Document Interface'

    def serialize(self, invoice_serializer: Union[EdiInvoiceSerializer, Mock]) -> EdiDocument:
        raise NotImplementedError()

    def deserialize(self, invoice_deserializer: Union[EdiInvoiceDeserializer, Mock]) -> Model:
        raise NotImplementedError()


class TransportInterface(AbstractModel):
    _name = 'edi.transport.interface'
    _description = 'EDI Transport Interface'

    def send(self, sender: EdiSenderTransport) -> None:
        raise NotImplementedError()

    def receive(self, receiver: EdiReceiverTransport) -> List[str]:
        raise NotImplementedError()
