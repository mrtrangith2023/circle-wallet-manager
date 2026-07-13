from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.wallet import WalletCreate, WalletResponse, WalletUpdate
from app.services.wallet_service import WalletService
from typing import List

router = APIRouter(
    prefix="/wallets",
    tags=["Wallet"],
)

@router.get(
    "",
    response_model=List[WalletResponse]
)
def list_wallets(
    db: Session = Depends(get_db),
):
    service = WalletService(db)

    return service.list_wallets()


@router.post(
    "",
    response_model=WalletResponse,
    status_code=201,
)

def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db),
):
    service = WalletService(db)
    return service.create_wallet(wallet)

@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
)
def get_wallet(
    wallet_id: int,
    db: Session = Depends(get_db),
):
    service = WalletService(db)

    return service.get_wallet(wallet_id)

@router.delete(
    "/{wallet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_wallet(
    wallet_id: int,
    db: Session = Depends(get_db),
):
    service = WalletService(db)

    service.delete_wallet(wallet_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put(
    "/{wallet_id}",
    response_model=WalletResponse,
)
def update_wallet(
    wallet_id: int,
    wallet: WalletUpdate,
    db: Session = Depends(get_db),
):
    service = WalletService(db)

    return service.update_wallet(
        wallet_id,
        wallet,
    )