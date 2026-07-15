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

class UserNotFoundException(
    AppException
):

    def __init__(
        self,
        user_id: int,
    ):

        super().__init__(
            status_code=404,
            detail=f"User {user_id} not found.",
        )

class UsernameAlreadyExistsException(
    AppException
):

    def __init__(
        self,
        username: str,
    ):

        super().__init__(
            status_code=409,
            detail=f"Username '{username}' already exists.",
        )

class EmailAlreadyExistsException(
    AppException
):

    def __init__(
        self,
        email: str,
    ):

        super().__init__(
            status_code=409,
            detail=f"Email '{email}' already exists.",
        )

class InvalidCredentialsException(
    AppException
):

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Invalid username or password.",
        )