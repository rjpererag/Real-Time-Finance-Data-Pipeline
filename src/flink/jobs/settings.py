from dataclasses import dataclass
from typing import Optional


@dataclass
class JobSettings:
    table_name: str = None
    watermark: int = 5
    event_mode: str = "proc_time"
    schema: Optional[str] = None
    sqls: Optional[dict] = None
    sink: bool = False
