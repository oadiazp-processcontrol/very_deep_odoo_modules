from typing import List

import paramiko
from paramiko.sftp_client import SFTPClient

from odoo.addons.pc_edi_account.models.edi_files_finder import EdiFilesFinder


class SftpEdiFilesFinder(EdiFilesFinder):
    def find(self) -> List[str]:
        sftp = self._connect()
        return [
            file.filename
            for file in sftp.listdir_attr(self.settings['received_invoices_path'])
        ]

    def _connect(self) -> SFTPClient:
        transport = paramiko.Transport((self.settings['host'], self.settings['port']))
        transport.connect(username=self.settings['username'], password=self.settings['password'])
        return SFTPClient.from_transport(transport)
