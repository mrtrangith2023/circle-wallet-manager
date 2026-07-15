from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import (
    UserService,
)
from app.core.dependencies import (
    require_admin,
    require_admin_or_user,
)
from app.core.services import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    user: UserCreate,

    service: UserService = Depends(
        get_user_service
    ),

    current_user: User = Depends(
            require_admin()
        ),
):

    return service.create_user(user)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(

    current_user: User = Depends(
        require_admin_or_user()
    ),
):

    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,

    service: UserService = Depends(
        get_user_service
    ),

    current_user: User = Depends(
        require_admin()
    ),
):

    return service.get_user(user_id)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(

    user_id: int,

    user_update: UserUpdate,

    service: UserService = Depends(
        get_user_service
    ),

    current_user: User = Depends(
        require_admin()
    ),

):

    return service.update_user(
        user_id,
        user_update,
    )

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(

    user_id: int,

    service: UserService = Depends(
        get_user_service
    ),

    current_user: User = Depends(
        require_admin()
    ),

):

    service.delete_user(
        user_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(

    service: UserService = Depends(
        get_user_service
    ),

    current_user: User = Depends(
        require_admin()
    ),
):

    return service.list_users()