from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.user_service import UserService
from app.services.wallet_service import WalletService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:

    return UserService(db)


def get_wallet_service(
    db: Session = Depends(get_db),
) -> WalletService:

    return WalletService(db)