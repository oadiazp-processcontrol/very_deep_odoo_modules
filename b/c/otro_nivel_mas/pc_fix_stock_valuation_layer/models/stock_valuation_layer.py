from odoo import _, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    def action_set_price(self):
        self.ensure_one()
        wzd = self.env.ref("pc_fix_stock_valuation_layer.pc_set_price_view_form")

        context = self.env.context.copy()
        context.update({"layer_id": self.id})

        return {
            "name": _("Set Price"),
            "view_mode": "form",
            "view_id": wzd.id,
            "res_model": "pc.set.price.wizard",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": context,
            "res_id": False,
        }
