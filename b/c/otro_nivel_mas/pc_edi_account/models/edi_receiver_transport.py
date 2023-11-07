from dataclasses import dataclass
from typing import List

EdiDocument = str


@dataclass
class EdiReceiverTransport:
    settings: dict
    files: list

    def receive(self) -> List[EdiDocument]:
        raise NotImplementedError()
