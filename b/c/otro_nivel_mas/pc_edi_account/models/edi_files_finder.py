from dataclasses import dataclass
from typing import List


@dataclass
class EdiFilesFinder:
    settings: dict

    def find(self) -> List[str]:
        raise NotImplementedError()