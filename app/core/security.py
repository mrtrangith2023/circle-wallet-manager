from pwdlib import PasswordHash
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.logger import logger

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def hash_password(
    password: str,
) -> str:

    return password_hash.hash(password)

def verify_password(
    password: str,
    hashed_password: str,
) -> bool:

    return password_hash.verify(
        password,
        hashed_password,
    )

def create_access_token(
    data: dict,
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
        }
    )
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt

def decode_access_token(
    token: str,
) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ],
        )

        return payload

    # except JWTError:
    #     return {}

    except JWTError:

        logger.warning(
            "event=invalid_token"
        )

        return {}

    # except JWTError as exc:

    #     raise InvalidTokenException() from exc