from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.user import UserLogin
from app.schemas.token import Token

from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/login",
    response_model=Token,
)

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    service = UserService(db)

    token = service.authenticate(
        form_data.username,
        form_data.password,
    )

    return Token(
        access_token=token,
        token_type="bearer",
    )