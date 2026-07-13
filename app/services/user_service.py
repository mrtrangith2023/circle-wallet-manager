from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository

from app.core.logger import logger
from app.core.exceptions import AppException
from app.core.security import hash_password

class UserService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.repository = UserRepository(db)

    def get_user(
        self,
        user_id: int,
    ) -> User:

        user = self.repository.get_by_id(user_id)

        if user is None:

            logger.warning(
                "event=user_not_found "
                "id=%s",
                user_id,
            )

            raise AppException(
                status_code=404,
                detail="User not found."
            )

        logger.info(
            "event=get_user "
            "id=%s",
            user.id,
        )

        return user

    def create_user(
        self,
        user: UserCreate,
    ) -> User:

        logger.info(
            "event=create_user_start "
            "username=%s "
            "email=%s",
            user.username,
            user.email,
        )

        if self.repository.username_exists(
            user.username
        ):

            logger.warning(
                "event=create_user_duplicate_username "
                "username=%s",
                user.username,
            )

            raise AppException(
                status_code=409,
                detail="Username already exists."
            )

        if self.repository.email_exists(
            user.email
        ):

            logger.warning(
                "event=create_user_duplicate_email "
                "email=%s",
                user.email,
            )

            raise AppException(
                status_code=409,
                detail="Email already exists."
            )

        try:

            db_user = User(

                username=user.username,

                email=user.email,

                hashed_password=hash_password(
                    user.password
                ),

                full_name=user.full_name,
            )

            created_user = self.repository.create(
                db_user
            )

            logger.info(
                "event=create_user_success "
                "id=%s "
                "username=%s "
                "email=%s",
                created_user.id,
                created_user.username,
                created_user.email,
            )

            return created_user

        except IntegrityError:

            logger.exception(
                "event=create_user_integrity_error "
                "username=%s",
                user.username,
            )

            self.db.rollback()

            raise AppException(
                status_code=409,
                detail="User already exists."
            )