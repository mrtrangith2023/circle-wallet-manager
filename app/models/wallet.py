from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    wallet_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(String)

    blockchain: Mapped[str] = mapped_column(String)

    network: Mapped[str] = mapped_column(
        String,
        default="ETH-SEPOLIA",
    )

    wallet_set_id: Mapped[str] = mapped_column(String)

    state: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )