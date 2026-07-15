from sqlalchemy.orm import Session
from app.models.user import User
from app.core.exceptions import UserNotFoundException
from app.repositories.base_repository import BaseRepository

class UserRepository(
    BaseRepository[User]
):

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(
            db,
            User,
        )

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        return self.get_by(
            username=username
        )

    def get_by_email(
            self,
            email: str,
        ) -> User | None:
    
            return self.get_by(
                email=email
            )

    def username_exists(
        self,
        username: str,
    ) -> bool:

        return self.exists(
            username=username
        )

    def email_exists(
        self,
        email: str,
    ) -> bool:

        return self.exists(
            email=email
        )

    def get_user_or_404(
        self,
        user_id: int,
    ) -> User:

        user = self.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException(user_id)

        return user

    def list_users(self) -> list[User]:

        return (
            self.db.query(self.model)
            .order_by(self.model.id.asc())
            .all()
        )