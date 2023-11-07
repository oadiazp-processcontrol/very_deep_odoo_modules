import json

from odoo.addons.pc_edi_account.models.edi_settings_finder import EdiSettingsFinder
from odoo.tests import TransactionCase


class TestEdiSettingsFinder(TransactionCase):
    settings_dict: dict

    def setUp(self):
        self.settings_dict = {
            'format': 'raw',
            'transport': 'sftp',
            'parameters': json.dumps({
                'default_setting': True
            }),
        }

        self.partner = self.env['res.partner'].create({
            'name': 'Lucky partner'
        })

    def test_returns_partner_settings_even_if_there_is_a_default_one(self):
        self.settings_dict.update({
            'partner_id': self.partner.id,
            'default': False,
        })

        self.env['edi.settings'].create(self.settings_dict)

        found_settings = EdiSettingsFinder(
            partner_id=self.partner,
            env=self.env
        ).find()

        self.assertEqual(
            found_settings.partner_id, self.partner
        )

    def test_return_default_settings(self):
        self.settings_dict.update({
            'default': True
        })
        self.env['edi.settings'].create(self.settings_dict)

        found_settings = EdiSettingsFinder(
            partner_id=self.partner,
            env=self.env
        ).find()

        self.assertEqual(found_settings.default, True)
        self.assertFalse(found_settings.partner_id, False)
