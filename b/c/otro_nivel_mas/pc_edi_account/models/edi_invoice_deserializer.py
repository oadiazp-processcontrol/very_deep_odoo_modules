from dataclasses import dataclass

from pydifact.segmentcollection import Interchange

from odoo.models import Model

EdiDocument = str


@dataclass
class EdiInvoiceDeserializer:
    edi_document: EdiDocument
    account_move_model: Model

    def deserialize(self) -> Model:
        interchange = Interchange.from_str(self.edi_document)
        created_model_dict = self._get_model_dict_from_interchange(interchange)
        return self.account_move_model.create(created_model_dict)

    def _get_model_dict_from_interchange(self, interchange: Interchange) -> dict:
        raise NotImplementedError()


        