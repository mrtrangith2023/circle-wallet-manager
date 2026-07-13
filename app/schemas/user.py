from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

class UserBase(BaseModel):

    username: str

    email: EmailStr

    full_name: str | None = None

class UserCreate(UserBase):

    password: str

class UserLogin(BaseModel):

    username: str

    password: str

class UserResponse(UserBase):

    id: int

    is_active: bool

    is_superuser: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )