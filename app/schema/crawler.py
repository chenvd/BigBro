from typing import List, Optional

from pydantic import BaseModel


class CrawlerResult(BaseModel):
    content: Optional[str] = None
    groups: Optional[str] = None
