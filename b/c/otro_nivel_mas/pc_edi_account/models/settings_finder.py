from odoo.models import Model


class SettingsFinder:
    def find(self) -> Model:
        raise NotImplementedError()
