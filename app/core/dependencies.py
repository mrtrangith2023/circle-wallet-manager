from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import (
    UserRepository,
)
from app.core.security import (
    oauth2_scheme,
    decode_access_token,
)
from app.core.exceptions import (
    InvalidCredentialsException,
)
from fastapi import HTTPException
from fastapi import status
from app.core.enums import UserRole

def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(
        get_db
    ),
) -> User:

    payload = decode_access_token(
        token
    )

    try:

        user_id = int(
            payload["sub"]
        )

    except (KeyError, ValueError, TypeError):

        raise InvalidCredentialsException()

    if user_id is None:

        raise InvalidCredentialsException()

    repository = UserRepository(
        db
    )

    user = repository.get_by_id(
        int(user_id)
    )

    if user is None:

        raise InvalidCredentialsException()

    return user

def require_roles(
    *roles: UserRole,
):

    def dependency(

        current_user: User = Depends(
            get_current_user
        ),

    ):

        if current_user.role not in roles:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Not enough permissions.",

            )

        return current_user

    return dependency

def require_admin():

    return require_roles(
        UserRole.ADMIN
    )


def require_user():

    return require_roles(
        UserRole.USER
    )


def require_admin_or_user():

    return require_roles(
        UserRole.ADMIN,
        UserRole.USER,
    )