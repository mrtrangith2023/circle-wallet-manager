from pydantic import BaseModel


class WalletCreate(BaseModel):

    wallet_id: str

    address: str

    blockchain: str

    wallet_set_id: str

    state: str