from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)

    wallet_id = Column(String, unique=True)

    address = Column(String)

    blockchain = Column(String)

    wallet_set_id = Column(String)

    state = Column(String)