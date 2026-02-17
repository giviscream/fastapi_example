from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt

from exceptions.custom_exceptions.invalid_token import InvalidTokenException


class SecurityService:
    def __init__(
        self,
        access_token_expire_minutes: int,
        sign_algorithm: str,
        secret_key: str,
        encoding: str = "utf-8",
    ):
        self.access_token_expire_minutes = access_token_expire_minutes
        self.sign_algorithm = sign_algorithm
        self.secret_key = secret_key
        self.encoding = encoding

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(
            password=bytes(
                password,
                encoding=self.encoding,
            ),
            salt=bcrypt.gensalt(),
        ).decode(encoding=self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=bytes(
                plain_password,
                encoding=self.encoding,
            ),
            hashed_password=bytes(
                hashed_password,
                encoding=self.encoding,
            ),
        )

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta:
            expire = datetime.now(tz=timezone.utc) + expires_delta
        else:
            expire = datetime.now(tz=timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )

        claims = data.copy()
        claims.update({"exp": expire})

        encoded_jwt = jwt.encode(
            claims=claims,
            key=self.secret_key,
            algorithm=self.sign_algorithm,
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token=token,
                key=self.secret_key,
                algorithms=[self.sign_algorithm],
            )
            return payload
        except JWTError:
            raise InvalidTokenException()
