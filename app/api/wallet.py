from fastapi import APIRouter, Depends, Response, status
from app.schemas.wallet import WalletCreate, WalletResponse, WalletUpdate
from app.services.wallet_service import WalletService
from app.models.user import User

from app.core.dependencies import (
    get_current_user,
)
from app.core.services import get_wallet_service

router = APIRouter(
    prefix="/wallets",
    tags=["Wallet"],
)

@router.get(
    "",
    response_model=list[WalletResponse]
)

def list_wallets(
    
    service: WalletService = Depends(
        get_wallet_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):

    return service.list_wallets(
        current_user
    )


@router.post(
    "",
    response_model=WalletResponse,
    status_code=201,
)

def create_wallet(
    wallet: WalletCreate,

    service: WalletService = Depends(
        get_wallet_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):

    return service.create_wallet(
        wallet,
        current_user,
    )

@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
)

def get_wallet(

    wallet_id: int,

    service: WalletService = Depends(
        get_wallet_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):

    return service.get_wallet(
        wallet_id,
        current_user,
    )

@router.put(
    "/{wallet_id}",
    response_model=WalletResponse,
)

def update_wallet(

    wallet_id: int,

    wallet: WalletUpdate,

    service: WalletService = Depends(
        get_wallet_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):

    return service.update_wallet(
        wallet_id,
        wallet,
        current_user
    )

@router.delete(
    "/{wallet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_wallet(

    wallet_id: int,

    service: WalletService = Depends(
        get_wallet_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):

    service.delete_wallet(
        wallet_id,
        current_user,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)