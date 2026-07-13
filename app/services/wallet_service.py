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

class WalletService:

    def __init__(self, db: Session):
        self.db = db

        self.repository = WalletRepository(
            db
        )

    def create_wallet(self, wallet: WalletCreate):

        logger.info(
            "event=create_wallet_start "
            "wallet_id=%s "
            "blockchain=%s",
            wallet.wallet_id,
            wallet.blockchain,
        )

        if self.repository.wallet_exists(wallet.wallet_id):

            logger.warning(
                "event=create_wallet_duplicate "
                "wallet_id=%s",
                wallet.wallet_id,
            )

            raise WalletAlreadyExistsException(
                wallet.wallet_id
            )
               
        db_wallet = Wallet(
            wallet_id=wallet.wallet_id,
            address=wallet.address,
            blockchain=wallet.blockchain,
            wallet_set_id=wallet.wallet_set_id,
            state=wallet.state,
        )

        try:
            self.db.add(db_wallet)
            self.db.commit()
            
            self.db.refresh(db_wallet)

            logger.info(
                "event=create_wallet_success "
                "id=%s "
                "wallet_id=%s "
                "blockchain=%s",
                db_wallet.id,
                db_wallet.wallet_id,
                db_wallet.blockchain,
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

    def list_wallets(self):

        wallets = self.repository.list_wallets()

        logger.info(
            "event=list_wallets "
            "count=%s",
            len(wallets),
        )

        return wallets

    def get_wallet(self, wallet_id: int):

        wallet = self.repository.get_wallet_or_404(
            wallet_id
        )

        logger.info(
            "event=get_wallet "
            "id=%s "
            "wallet_id=%s",
            wallet.id,
            wallet.wallet_id,
        )

        return wallet

    def delete_wallet(self, wallet_id: int) -> None:
        
        wallet = self.repository.get_wallet_or_404(wallet_id)

        logger.info(
            "event=delete_wallet_start "
            "id=%s",
            wallet.id,
        )

        self.db.delete(wallet)

        self.db.commit()

        logger.info(
            "event=delete_wallet_success "
            "id=%s",
            wallet.id,
        )

    def update_wallet(
        self,
        wallet_id: int,
        wallet_update: WalletUpdate,
    ) -> Wallet:

        wallet = self.repository.get_wallet_or_404(wallet_id)

        logger.info(
            "event=update_wallet_start "
            "id=%s",
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

        self.db.commit()

        self.db.refresh(wallet)

        logger.info(
            "event=update_wallet_success "
            "id=%s "
            "updated_fields=%s",
            wallet.id,
            len(update_data),
        )

        return wallet