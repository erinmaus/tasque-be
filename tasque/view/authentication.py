from tasque.model.account import AccountEntity, AccountModel
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..model import get_db
from ..model.token import Token
from ..controller.account import (
    create_auth_token,
    get_account_from_auth_token,
    verify_account,
)

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_account(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return get_account_from_auth_token(db, token)


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    account = verify_account(db, form_data.username, form_data.password)
    token = create_auth_token(account)

    return Token(access_token=token, token_type="bearer")


@router.post("/refresh", response_model=Token)
def refresh(current_account: AccountEntity = Depends(get_current_account)):
    token = create_auth_token(current_account)
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=AccountModel)
def refresh(current_account: AccountEntity = Depends(get_current_account)):
    return current_account.to_model()
