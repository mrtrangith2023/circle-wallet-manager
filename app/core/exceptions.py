from fastapi import HTTPException

class AppException(HTTPException):

    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

class WalletNotFoundException(AppException):

    def __init__(self, wallet_id: int):

        super().__init__(
            status_code=404,
            detail=f"Wallet {wallet_id} not found."
        )

class WalletAlreadyExistsException(AppException):

    def __init__(self, wallet_id: str):

        super().__init__(
            status_code=409,
            detail=f"Wallet '{wallet_id}' already exists."
        )