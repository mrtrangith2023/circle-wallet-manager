import time
from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.schemas.wallet import (
    WalletCreate,
    WalletUpdate,
)
from sqlalchemy.exc import IntegrityError
from app.core.logger import logger
from app.core.exceptions import (
    WalletAlreadyExistsException,
)
from app.repositories.wallet_repository import (
    WalletRepository
)
from app.models.user import User

class WalletService:

    def __init__(self, db: Session):
        self.db = db

        self.repository: WalletRepository = WalletRepository(db)

    def create_wallet(
        self,
        wallet: WalletCreate,
        current_user: User,
    ) -> Wallet:

        logger.info(
            "event=create_wallet_start "
            "wallet_id=%s "
            "blockchain=%s",
            wallet.wallet_id,
            wallet.blockchain,
        )

        start = time.perf_counter()

        if self.repository.wallet_exists(wallet.wallet_id):

            logger.warning(
                "event=create_wallet_duplicate "
                "wallet_id=%s",
                wallet.wallet_id,
            )

            raise WalletAlreadyExistsException(
                wallet.wallet_id
            )
               
        db_wallet = self._build_wallet(
            wallet,
            current_user,
        )

        try:

            db_wallet = self.repository.create(
                db_wallet
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            logger.info(
                "event=create_wallet_success "
                "wallet_db_id=%s "
                "wallet_id=%s "
                "blockchain=%s "
                "duration_ms=%.2f",
                db_wallet.id,
                db_wallet.wallet_id,
                db_wallet.blockchain,
                elapsed,
            )

        except IntegrityError:

            logger.exception(
                "event=create_wallet_integrity_error "
                "wallet_id=%s",
                wallet.wallet_id,
            )

            self.db.rollback()

            raise WalletAlreadyExistsException(
                wallet.wallet_id
            )

        return db_wallet

    def list_wallets(
        self,
        current_user: User,
    ) -> list[Wallet]:

        wallets = self.repository.list_wallets(
            current_user.id
        )

        logger.info(
            "event=list_wallets "
            "owner_id=%s "
            "count=%s",
            current_user.id,
            len(wallets),
        )

        return wallets

    def get_wallet(
        self,
        wallet_id: int,
        current_user: User,
    ):

        wallet = self.repository.get_wallet_by_owner(
            wallet_id,
            current_user.id,
        )

        logger.info(
            "event=get_wallet "
            "wallet_db_id=%s "
            "owner_id=%s "
            "wallet_id=%s",
            wallet.id,
            current_user.id,
            wallet.wallet_id,
        )

        return wallet

    def delete_wallet(
        self,
        wallet_id: int,
        current_user: User,
    ) -> None:

        wallet = self.repository.get_wallet_by_owner(
            wallet_id,
            current_user.id,
        )

        logger.info(
            "event=delete_wallet_start "
            "owner_id=%s "
            "wallet_db_id=%s",
            current_user.id,
            wallet.id,
        )

        self.repository.delete(wallet)

        logger.info(
            "event=delete_wallet_success "
            "owner_id=%s "
            "wallet_db_id=%s",
            current_user.id,
            wallet.id,
        )

    def update_wallet(
        self,
        wallet_id: int,
        wallet_update: WalletUpdate,
        current_user: User,
    ) -> Wallet:

        wallet = self.repository.get_wallet_by_owner(
            wallet_id,
            current_user.id,
        )

        logger.info(
            "event=update_wallet_start "
            "wallet_db_id=%s",
            wallet_id,
        )

        update_data = wallet_update.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(
                wallet,
                field,
                value,
            )

        wallet = self.repository.update(wallet)

        logger.info(
            "event=update_wallet_success "
            "owner_id=%s "
            "wallet_id=%s "
            "updated_fields=%s",
            current_user.id,
            wallet.id,
            list(update_data.keys()),
        )

        return wallet

    def _build_wallet(
        self,
        wallet: WalletCreate,
        current_user: User,
    ) -> Wallet:

        return Wallet(

            owner_id=current_user.id,

            wallet_id=wallet.wallet_id,

            address=wallet.address,

            blockchain=wallet.blockchain,

            wallet_set_id=wallet.wallet_set_id,

            state=wallet.state,
        )