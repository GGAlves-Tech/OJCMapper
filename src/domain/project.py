from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: Optional[int]
    name: str
    type: str  # ONLINE or GAVETA
    path: str
