from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class RuleHistoryValue(BaseModel):
    id: int
    content: str
    groups: Optional[str]


class RuleHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rule_id: int
    status: int
    content: str
    values: Optional[List[RuleHistoryValue]] = None
    create_time: datetime
