from typing import List

import paramiko

from odoo.addons.pc_edi_account.models.edi_receiver_transport import EdiReceiverTransport

EdiDocument = str


class SftpEdiReceiverTransport(EdiReceiverTransport):
    sftp_client: paramiko.SFTPClient = None

    def connect(self):
        transport = paramiko.Transport((self.settings['host'], self.settings['port']))
        transport.connect(username=self.settings['username'], password=self.settings['password'])
        self.sftp_client = paramiko.SFTPClient.from_transport(transport)

    def disconnect(self):
        self.sftp_client.close()

    def receive(self) -> List[EdiDocument]:
        self.connect()
        result = []

        for file in self.files:
            path = f'{self.settings["received_invoices_path"]}/{file}'
            with self.sftp_client.open(path, 'r') as f:
                edi_document = f.read().decode('utf-8')
                result.append(EdiDocument(edi_document))

        self.disconnect()

        return result
