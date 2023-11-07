from pydifact import Segment
from pydifact.segmentcollection import Interchange

from odoo.addons.pc_edi_account.models.edi_invoice_serializer import EdiInvoiceSerializer


class RawEdiInvoiceSerializer(EdiInvoiceSerializer):

    def _create_interchange(self) -> Interchange:
        return Interchange(
            'UNOC',
            '123456789',
            '123456789',
            '200102',
        )

    def _create_first_interchange_segments(self, interchange: Interchange) -> None:
        interchange.add_segment(Segment('UNH', ['INVOIC', 'D', '96A', 'UN', 'EAN008']))

        interchange.add_segment(Segment('BGM', ['380', self.model.name]))
        # interchange.add_segment(Segment('DTM', ['137', self.invoice_date]))
        interchange.add_segment(Segment('CUX', ['1', 'EUR']))
        interchange.add_segment(Segment('NAD', ['BY', self.model.partner_id.name]))
        interchange.add_segment(Segment('NAD', ['SE', self.model.env.company.name]))

    def _create_lines_segments(self, interchange: Interchange) -> None:
        for line in self.model.invoice_line_ids:
            interchange.add_segment(Segment('LIN', [line.product_id.name]))
            interchange.add_segment(Segment('QTY', [str(line.quantity)]))
            interchange.add_segment(Segment('PRI', [str(line.price_unit)]))

    def _create_last_interchange_segments(self, interchange: Interchange) -> None:
        interchange.add_segment(Segment('MOA', ['203', str(self.model.amount_total)]))
        interchange.add_segment(Segment('UNT', ['1', '1']))
        interchange.add_segment(Segment('UNZ', ['1', 'INVOICD96AUNEAN008']))
