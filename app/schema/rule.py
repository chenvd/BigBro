from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class RuleBase(BaseModel):
    name: str
    url: str
    favicon: str = ''

    user_agent: Optional[str] = None
    cookies: Optional[str] = None
    cron: str

    is_list: bool = False
    xpath: Optional[str] = None
    regex: Optional[str] = None
    status: bool = True

    notify_ids: Optional[List[int]] = []


class RuleCreate(RuleBase):
    user_id: int = 0


class RuleUpdate(RuleBase):
    id: int


class Rule(RuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    has_new: bool
