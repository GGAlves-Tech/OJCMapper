from dataclasses import dataclass
from typing import Optional

@dataclass
class Setting:
    id: Optional[int]
    key: str
    value: str
