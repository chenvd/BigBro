from pydantic import BaseModel


class NotifyBase(BaseModel):
    name: str
    type: str
    payload: str


class NotifyCreate(NotifyBase):
    pass


class Notify(NotifyBase):
    id: int
