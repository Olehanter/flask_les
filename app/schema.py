from abc import ABC
import pydantic
from typing import Optional, Type


class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    password: str

    @pydantic.field_validator('name')
    @classmethod
    def name_length(cls, v: str) -> str:
        if len(v) > 100:
            raise  ValueError('Max len of name is 100')
        return v

    @pydantic.field_validator('password')
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Min len of password is 8')
        return v

class CreateUser(AbstractUser):
    name: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    password: Optional[str] = None


SCHEMA_CLASS = Type[CreateUser | UpdateUser]
SCHEMA = CreateUser | UpdateUser
