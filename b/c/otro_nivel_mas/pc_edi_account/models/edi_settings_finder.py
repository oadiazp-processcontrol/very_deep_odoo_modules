from dataclasses import dataclass

from odoo.addons.pc_edi_account.models.settings_finder import SettingsFinder
from odoo.exceptions import UserError
from odoo.models import Model


@dataclass
class EdiSettingsFinder(SettingsFinder):
    partner_id: object
    env: object

    def find(self) -> Model:
        partner_settings = self.env['edi.settings'].search([
            ('partner_id', '=', self.partner_id.id)
        ])

        if partner_settings:
            return partner_settings

        default_settings = self.env['edi.settings'].search([
            ('default', '=', True)
        ])

        if not default_settings:
            raise UserError(f'There is no settings for {self.partner_id.name}')

        return default_settings
