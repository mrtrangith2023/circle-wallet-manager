from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from app.enums.wallet import WalletState, Blockchain
class WalletCreate(BaseModel):

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    wallet_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique Wallet ID",
        examples=["wallet_demo_001"],
    )
    address: str = Field(
        ...,
        min_length=4,
        max_length=100,
        pattern=r"^0x",
        description="Blockchain wallet address",
        examples=["0x123456789abcdef"],
    )
    blockchain: Blockchain
    wallet_set_id: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Circle Wallet Set ID",
        examples=["wallet_set_demo"],
    )
    state: WalletState

from typing import Optional

class WalletResponse(WalletCreate):

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class WalletUpdate(BaseModel):

    address: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=100,
        pattern=r"^0x",
    )

    blockchain: Optional[Blockchain] = None

    wallet_set_id: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    state: Optional[WalletState] = None