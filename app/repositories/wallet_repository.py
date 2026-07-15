from sqlalchemy.orm import Session

from app.models.wallet import Wallet

from app.repositories.base_repository import (
    BaseRepository,
)

from app.core.exceptions import (
    WalletNotFoundException,
)

from app.core.logger import logger


class WalletRepository(BaseRepository[Wallet]):

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(
            db,
            Wallet,
        )

    def wallet_exists(
        self,
        wallet_id: str,
    ) -> bool:

        return self.exists(
            wallet_id=wallet_id,
        )

    def list_wallets(
        self,
        owner_id: int,
    ) -> list[Wallet]:

        return (
            self.db.query(self.model)
            .filter(
                self.model.owner_id == owner_id,
            )
            .order_by(
                self.model.id.desc(),
            )
            .all()
        )

    def get_wallet_by_owner(
        self,
        wallet_id: int,
        owner_id: int,
    ) -> Wallet:

        wallet = (
            self.db.query(self.model)
            .filter(
                self.model.id == wallet_id,
                self.model.owner_id == owner_id,
            )
            .first()
        )

        if wallet is None:

            logger.warning(
                "event=wallet_not_found "
                "wallet_id=%s "
                "owner_id=%s",
                wallet_id,
                owner_id,
            )

            raise WalletNotFoundException(
                wallet_id
            )

        return wallet