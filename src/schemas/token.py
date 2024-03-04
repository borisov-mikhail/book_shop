from pydantic import BaseModel

__all__ = ["IncomingData"]


class IncomingData(BaseModel):
    e_mail: str
    password: str