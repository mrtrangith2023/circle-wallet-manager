import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.logger import logger
from app.core.exceptions import (
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)
from app.core.enums import UserRole

class UserService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.repository: UserRepository = UserRepository(db)

    def get_user(
        self,
        user_id: int,
    ) -> User:

        user = self.repository.get_user_or_404(
            user_id
        )

        logger.info(
            "event=get_user "
            "user_id=%s",
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

        start = time.perf_counter()

        if self.repository.username_exists(
            user.username
        ):

            logger.warning(
                "event=create_user_duplicate_username "
                "username=%s",
                user.username,
            )

            raise UsernameAlreadyExistsException(
                user.username
            )

        if self.repository.email_exists(
            user.email
        ):

            logger.warning(
                "event=create_user_duplicate_email "
                "email=%s",
                user.email,
            )

            raise EmailAlreadyExistsException(
                user.email
            )

        try:

            db_user = self._build_user(
                user
            )

            created_user = self.repository.create(
                db_user
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            logger.info(
                "event=create_user_success "
                "user_id=%s "
                "username=%s "
                "email=%s "
                "duration_ms=%.2f",
                created_user.id,
                created_user.username,
                created_user.email,
                elapsed,
            )

            return created_user

        except IntegrityError:

            self.db.rollback()

            logger.exception(
                "event=create_user_integrity_error "
                "username=%s",
                user.username,
            )

            raise UsernameAlreadyExistsException(
                user.username
            )

    def update_user(
            self,
            user_id: int,
            user_update: UserUpdate,
        ) -> User:
    
            logger.info(
                "event=update_user_start "
                "user_id=%s",
                user_id,
            )
    
            user = self.repository.get_user_or_404(
                user_id
            )
    
            update_data = user_update.model_dump(
                exclude_unset=True
            )

            user = self._apply_user_updates(
                user,
                user_update,
            )

            user = self.repository.update(
                user
            )

            logger.info(
                "event=update_user_success "
                "user_id=%s "
                "updated_fields=%s",
                user.id,
                list(update_data.keys()),
            )
    
            return user
    
    def delete_user(
            self,
            user_id: int,
        ) -> None:
    
            user = self.repository.get_user_or_404(
                user_id
            )
    
            logger.info(
                "event=delete_user_start "
                "user_id=%s",
                user.id,
            )
    
            self.repository.delete(
                user
            )
    
            logger.info(
                "event=delete_user_success "
                "user_id=%s",
                user.id,
            )    

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> str:

        logger.info(
            "event=login_start "
            "username=%s",
            username,
        )

        user = self.repository.get_by_username(
            username
        )

        if user is None:

            logger.warning(
                "event=login_user_not_found "
                "username=%s",
                username,
            )

            raise InvalidCredentialsException()

        if not verify_password(
            password,
            user.hashed_password,
        ):

            logger.warning(
                "event=login_invalid_password "
                "username=%s",
                username,
            )

            raise InvalidCredentialsException()
        
        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
                "username": user.username
            }
        )
        
        logger.info(
            "event=login_success "
            "user_id=%s "
            "username=%s",
            user.id,
            user.username,
        )

        return token

    def list_users(self) -> list[User]:

        users = self.repository.list_users()

        logger.info(
            "event=list_users count=%s",
            len(users),
        )

        return users

    def _build_user(
        self,
        user: UserCreate,
    ) -> User:

        return User(

            username=user.username,

            email=user.email,

            hashed_password=hash_password(
                user.password
            ),

            full_name=user.full_name,

            role=UserRole.USER,
        )

    def _apply_user_updates(
        self,
        user: User,
        user_update: UserUpdate,
    ) -> User:

        for field, value in user_update.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                user,
                field,
                value,
            )

        return user