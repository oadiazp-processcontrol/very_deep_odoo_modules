from typing import Optional

from pydifact import Segment
from pydifact.segmentcollection import Interchange

from odoo.addons.pc_edi_account.models.edi_invoice_deserializer import EdiInvoiceDeserializer
from odoo.addons.pc_edi_account.models.edi_invoice_serializer import EdiInvoiceSerializer


class RawEdiInvoiceDeserializer(EdiInvoiceDeserializer):
    def _get_model_dict_from_interchange(self, interchange: Interchange) -> dict:
        return {
            'name': interchange.get_segment('BGM').elements[1],
            'partner_id': self._get_partner(interchange.get_segment('NAD').elements[1][0]),
            'journal_id': self.account_move_model.env['account.journal'].search([], limit=1).id,
            'invoice_line_ids': [self._get_invoice_lines(interchange)],
            'amount_total': interchange.get_segment('MOA').elements[0][1],
        }

    def _get_partner(self, partner_name: str) -> Optional[int]:
        partner = self.account_move_model.env['res.partner'].search(
            [('name', '=', partner_name)],
            limit=1
        )

        if not partner:
            partner = self.account_move_model.env['res.partner'].create({
                'name': partner_name
            })

        return partner[0].id

    def _get_invoice_lines(self, interchange):
        lines = interchange.get_segment('LIN')
        quantities = interchange.get_segment('QTY')
        prices = interchange.get_segment('PRI')

        return (0, 0, {
            'name': lines[2][0],
            'quantity': quantities[0][0],
            'price_unit': prices[0][1],
            'account_id': self.account_move_model.env['account.account'].search([], limit=1).id,
            'product_id': self._get_or_create_product(product=lines[2][0]),
        })

    def _get_or_create_product(self, product: str) -> Optional[int]:
        product = self.account_move_model.env['product.product'].search(
            [('name', '=', product)],
            limit=1
        )

        if not product:
            product = self.account_move_model.env['product.product'].create({
                'name': product
            })

        return product[0].id
