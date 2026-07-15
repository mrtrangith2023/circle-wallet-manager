from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base

from app.enums.wallet import (
    Blockchain,
    WalletState,
)


class Wallet(Base):

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    wallet_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    blockchain: Mapped[Blockchain] = mapped_column(
        Enum(
            Blockchain,
            values_callable=lambda enum: [
                item.value
                for item in enum
            ],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )

    network: Mapped[str] = mapped_column(
        String(100),
        default="ETH-SEPOLIA",
        nullable=False,
    )

    wallet_set_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    state: Mapped[WalletState] = mapped_column(
        Enum(
            WalletState,
            values_callable=lambda enum: [
                item.value
                for item in enum
            ],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="wallets",
    )