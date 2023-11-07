from odoo import fields, models


class SetPriceWizard(models.TransientModel):
    _name = "pc.set.price.wizard"
    _description = "Set Layer Wizard"

    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        related="company_id.currency_id",
        readonly=True,
        required=True,
    )
    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )

    quantity = fields.Float(
        "Quantity", readonly=False, digits="Product Unit of Measure", default=0.0
    )
    uom_id = fields.Many2one(comodel_name="uom.uom", readonly=False, required=False)
    unit_cost = fields.Monetary("Unit Value", readonly=False, default=0.0)
    value = fields.Monetary("Total Value", readonly=False, default=0.0)
    remaining_qty = fields.Float(
        readonly=False, digits="Product Unit of Measure", default=0.0
    )

    def action_set_layer(self):
        self.ensure_one()
        vals = {}
        layer_id = self.env["stock.valuation.layer"].browse(
            self._context.get("layer_id")
        )
        if self.unit_cost:
            vals["unit_cost"] = self.unit_cost
        if self.uom_id:
            vals["uom_id"] = self.uom_id.id
        if self.quantity:
            vals["quantity"] = self.quantity
        if self.value:
            vals["value"] = self.value
        if self.remaining_qty:
            vals["remaining_qty"] = self.remaining_qty

        layer_id.write(vals)
        return {"type": "ir.actions.act_window_close"}
