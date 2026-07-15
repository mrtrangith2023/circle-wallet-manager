from datetime import datetime

from pydantic import BaseModel
from app.core.enums import UserRole
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

    role: UserRole

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UserUpdate(BaseModel):

    username: str | None = None

    email: EmailStr | None = None

    full_name: str | None = None

    is_active: bool | None = None

    role: UserRole | None = None