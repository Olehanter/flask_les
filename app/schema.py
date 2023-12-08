import pydantic
from typing import Optional, Type



class AbstractUser(pydantic.BaseModel):
    name: str
    password: str

    @pydantic.functional_validators('name')
    @classmethod
    def name_length(cls, v:str) -> str:
        if len(v) > 100:
            raise  ValueError('Max len of name is 100')
        return v


    @pydantic.functional_validators('password')
    @classmethod
    def secure_password(cls, v:str) -> str:
        if len(v) < 8:
            raise  ValueError('Min len of password is 8')
        return v

class CreateUser(AbstractUser):
    name: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str]
    password: Optional[str]


SCHEMA_CLASS = Type[CreateUser | UpdateUser]
SCHEMA = CreateUser | UpdateUser
