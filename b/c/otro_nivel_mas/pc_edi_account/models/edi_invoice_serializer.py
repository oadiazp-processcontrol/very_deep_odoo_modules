from dataclasses import dataclass

from pydifact.segmentcollection import Interchange

from odoo.models import Model

EdiDocument = str


@dataclass
class EdiInvoiceSerializer:
    model: Model

    def serialize(self) -> EdiDocument:
        interchange = self._create_interchange()
        self._create_first_interchange_segments(interchange)
        self._create_lines_segments(interchange)
        self._create_last_interchange_segments(interchange)
        return EdiDocument(interchange.serialize())

    def _create_interchange(self) -> Interchange:
        raise NotImplementedError

    def _create_first_interchange_segments(self, interchange: Interchange) -> None:
        raise NotImplementedError

    def _create_lines_segments(self, interchange: Interchange) -> None:
        raise NotImplementedError

    def _create_last_interchange_segments(self, interchange: Interchange) -> None:
        raise NotImplementedError
