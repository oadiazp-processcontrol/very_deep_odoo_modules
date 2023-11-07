import uuid
from os import unlink
from tempfile import NamedTemporaryFile

from pysftp import Connection, CnOpts

from odoo.addons.pc_edi_account.models.edi_sender_transport import EdiSenderTransport


class SftpEdiSenderTransport(EdiSenderTransport):
    def send(self):
        connection = self._get_connection()
        temporal_file = self._create_temporal_file()
        self._save_file_into_sftp_server(connection, temporal_file)

    def _save_file_into_sftp_server(self, connection, temporal_file):
        target_path = f'{self.settings["sent_invoices_path"]}/{uuid.uuid4()}.edi'
        connection.put(temporal_file.name, target_path)
        connection.close()
        unlink(temporal_file.name)

    def _create_temporal_file(self):
        temporal_file = NamedTemporaryFile(mode='w+', delete=False)
        temporal_file.write(self.edi_document)
        temporal_file.close()
        return temporal_file

    def _get_connection(self):
        cn_opts = CnOpts()
        cn_opts.hostkeys = None
        connection = Connection(
            host=self.settings['host'],
            username=self.settings['username'],
            password=self.settings['password'],
            port=self.settings['port'],
            cnopts=cn_opts
        )
        return connection