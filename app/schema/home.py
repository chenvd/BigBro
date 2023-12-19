from datetime import datetime

from pydantic import BaseModel


class HomeSchedule(BaseModel):
    id: int
    title: str
    next_time: datetime
    favicon: str
