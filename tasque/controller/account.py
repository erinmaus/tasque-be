from datetime import datetime, timedelta
import re
from tasque.logging import get_logger
from jose import JWTError, jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..model.account import AccountEntity
from ..constants import TASQUE_JWT_EXPIRATION_MINUTES, TASQUE_SECRET_KEY

MIN_PASSWORD_LENGTH = 8
MIN_USERNAME_LENGTH = 4

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = get_logger(__name__)


def verify_username(username):
    if len(username) < MIN_USERNAME_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Username must be at least {MIN_USERNAME_LENGTH} characters long.",
        )
    if not re.compile("[\\w\\d]*", flags=re.ASCII).match(username):
        raise HTTPException(
            status_code=400, detail=f"Username can only contain letters and numbers."
        )


def verify_email(email):
    if not "@" in email:
        raise HTTPException(status_code=400, detail="Invalid email; must contain '@'")


def verify_password(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.",
        )


def hash_account_password(password):
    return password_context.hash(password)


def create_account(
    db: Session, username: str, password: str, email: str, organization_id: int
):
    transformed_username = username.lower()
    transformed_email = email.lower()

    verify_username(transformed_username)
    verify_password(password)
    verify_email(transformed_email)

    password_hash = hash_account_password(password)
    db.add(
        AccountEntity(
            username=transformed_username,
            email=transformed_email,
            password_hash=password_hash,
            organization_id=organization_id,
        )
    )


def verify_account(db: Session, username: str, password: str):
    try:
        account = get_account_by_username(db, username)
        if not password_context.verify(password, account.password_hash):
            logger.debug(f"Password does not match for account '{username}''.")
            raise HTTPException(status_code=401, detail="Password does not match.")
        return account
    except HTTPException:
        logger.debug("Could not verify user.", exc_info=True)
        raise HTTPException(status_code=401, detail="Username or password invalid.")


def get_account_by_username(db: Session, username: str):
    account = (
        db.query(AccountEntity).filter(AccountEntity.username.ilike(username)).first()
    )
    if account == None:
        logger.debug(f"Account '{username}' does not exist.")
        raise HTTPException(status_code=404, detail=f"Account '{username}' not found.")
    return account


def create_auth_token(user: AccountEntity):
    expires = datetime.utcnow() + TASQUE_JWT_EXPIRATION_MINUTES

    data = {
        "username": user.username,
        "email": user.email,
        "expires": int(expires.timestamp()),
    }

    return jwt.encode(data, TASQUE_SECRET_KEY, algorithm="HS256")


def get_account_from_auth_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, TASQUE_SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        expires = payload.get("expires")
        if datetime.utcnow().timestamp() > expires:
            raise HTTPException(status_code=401, detail="Token expired.")
        return get_account_by_username(db, username)
    except JWTError:
        logger.debug(f"Could not validate credentials.", exc_info=True)
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials (is token expired?).",
        )


def get_account_by_email(db: Session, email: str):
    account = db.query(AccountEntity).filter(AccountEntity.email.ilike(email)).first()
    if account == None:
        logger.debug(f"Account with email '{email}' does not exist.")
        raise HTTPException(
            status_code=404, detail=f"Account with email '{email}' not found."
        )
    return account
