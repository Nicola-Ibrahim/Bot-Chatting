from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from ......modules.accounts.domain.account import Account
from ......modules.accounts.infrastructure.accounts_module import AccountsModule
from ..security import jwt
from .account_response import AccountResponse
from .get_account import GetAccountRequest
from .list_accounts import ListAccountsRequest
from .login_request import LoginRequest
from .login_response import LoginResponse
from .register_account_request import RegisterAccountRequest
from .update_account_request import UpdateAccountRequest
from .verify_account_request import VerifyAccountRequest

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponse,
    summary="Register a new account",
)
def register_account(payload: RegisterAccountRequest) -> AccountResponse:
    try:
        account = AccountsModule.execute_command_async(
            command=RegisterAccountRequest(email=payload.email, password=payload.password)
        )
        return AccountResponse.from_domain(account)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post(
    "/verify",
    response_model=AccountResponse,
    summary="Verify an account",
)
def verify_account(payload: VerifyAccountRequest) -> AccountResponse:
    try:
        account = AccountsModule.execute_command_async(command=VerifyAccountRequest(account_id=payload.account_id))
        return AccountResponse.from_domain(account)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate an account",
)
def login(payload: LoginRequest) -> LoginResponse:
    try:
        account, dto = AccountsModule.execute_command_async(
            command=LoginRequest(email=payload.email, password=payload.password)
        )
        access_token = jwt.create_access_token({"sub": str(account.id.value)}, expires_delta=timedelta(minutes=30))
        return LoginResponse(
            user=AccountResponse.from_domain(account),
            access_token=access_token,
            refresh_token=dto.refresh_token,
            session_id=dto.session_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Retrieve a single account",
)
def get_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
) -> AccountResponse:
    account = AccountsModule.execute_query_async(command=GetAccountRequest(account_id=account_id))
    return AccountResponse.from_domain(account)


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="List all accounts",
)
def list_accounts(current_user: Account = Depends(jwt.get_current_user)) -> list[AccountResponse]:
    accounts = AccountsModule.execute_query_async(command=ListAccountsRequest())
    return [AccountResponse.from_domain(account) for account in accounts]


@router.get(
    "/me",
    response_model=AccountResponse,
    summary="Retrieve the authenticated account",
)
def get_current_account(current_user: Account = Depends(jwt.get_current_user)) -> AccountResponse:
    return AccountResponse.from_domain(current_user)


@router.patch(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Update an account",
)
def update_account(
    account_id: str,
    payload: UpdateAccountRequest,
    current_user: Account = Depends(jwt.get_current_user),
) -> AccountResponse:
    try:
        account = AccountsModule.execute_command_async(
            command=UpdateAccountRequest(
                account_id=account_id,
                email=payload.email,
                password=payload.password,
                is_active=payload.is_active,
            )
        )
        return AccountResponse.from_domain(account)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail == "Account not found" else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail)


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an account",
)
def delete_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
) -> None:
    try:
        AccountsModule.execute_command_async(command=DeleteAccountRequest(account_id=account_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
