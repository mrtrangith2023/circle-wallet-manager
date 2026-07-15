from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.auth import get_current_user
from app.core.enums import UserRole


def require_roles(*roles: UserRole):

    def dependency(
        current_user=Depends(get_current_user),
    ):

        if current_user.role not in roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return dependency