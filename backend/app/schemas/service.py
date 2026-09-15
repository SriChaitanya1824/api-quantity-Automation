from pydantic import BaseModel


class ServiceRead(BaseModel):
    id: int
    name: str
    category: str
    description: str
    active: bool
