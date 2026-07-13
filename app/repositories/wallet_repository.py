from sqlalchemy.orm import Session

from app.models.wallet import Wallet

class WalletRepository:

    def __init__(self, db: Session):

        self.db = db

    def wallet_exists(self, wallet_id: str) -> bool:
        
        return (
            self.db.query(Wallet)
            .filter(Wallet.wallet_id == wallet_id)
            .first()
            is not None
        )

    def list_wallets(self):

        return (
            self.db.query(Wallet)
            .order_by(
                Wallet.id.desc()
            )
            .all()
        )