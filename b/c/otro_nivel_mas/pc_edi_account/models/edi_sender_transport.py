from dataclasses import dataclass

EdiDocument = str


@dataclass
class EdiSenderTransport:
    edi_document: EdiDocument
    settings: dict

    def send(self):
        raise NotImplementedError()


