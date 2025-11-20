from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from src.building_blocks.domain.result import Result
from ......modules.accounts.domain.account import Account
from ......modules.accounts.infrastructure.accounts_module import AccountsModule
from ..security import jwt
from .account_response import AccountResponse
from .get_account import GetAccountRequest
from .list_accounts import ListAccountsRequest
from .login_request import LoginRequest
from .login_response import LoginResponse
from .delete_account_request import DeleteAccountRequest
from .register_account_request import RegisterAccountRequest
from .update_account_request import UpdateAccountRequest
from .verify_account_request import VerifyAccountRequest

router = APIRouter(prefix="/accounts", tags=["accounts"])


def _raise_http(status_code: int):
    def _inner(error: Exception):
        raise HTTPException(status_code=status_code, detail=str(error))

    return _inner


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponse,
    summary="Register a new account",
)
async def register_account(
    payload: RegisterAccountRequest,
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> AccountResponse:
    result: Result = await accounts_module.execute_command_async(
        command=RegisterAccountRequest(email=payload.email, password=payload.password),
    )
    return result.match(
        on_success=lambda account: AccountResponse.from_domain(account),
        on_failure=_raise_http(status.HTTP_400_BAD_REQUEST),
    )


@router.post(
    "/verify",
    response_model=AccountResponse,
    summary="Verify an account",
)
async def verify_account(
    payload: VerifyAccountRequest,
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> AccountResponse:
    result: Result = await accounts_module.execute_command_async(
        command=VerifyAccountRequest(account_id=payload.account_id),
    )
    return result.match(
        on_success=lambda account: AccountResponse.from_domain(account),
        on_failure=_raise_http(status.HTTP_404_NOT_FOUND),
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate an account",
)
async def login(
    payload: LoginRequest,
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> LoginResponse:
    result: Result = await accounts_module.execute_command_async(
        command=LoginRequest(email=payload.email, password=payload.password),
    )
    return result.match(
        on_success=lambda data: LoginResponse(
            user=AccountResponse.from_domain(data[0]),
            access_token=jwt.create_access_token({"sub": str(data[0].id.value)}, expires_delta=timedelta(minutes=30)),
            refresh_token=data[1].refresh_token,
            session_id=data[1].session_id,
        ),
        on_failure=_raise_http(status.HTTP_400_BAD_REQUEST),
    )


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Retrieve a single account",
)
async def get_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> AccountResponse:
    result: Result = await accounts_module.execute_query_async(command=GetAccountRequest(account_id=account_id))
    return result.match(
        on_success=lambda account: AccountResponse.from_domain(account),
        on_failure=_raise_http(status.HTTP_404_NOT_FOUND),
    )


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="List all accounts",
)
async def list_accounts(
    current_user: Account = Depends(jwt.get_current_user),
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> list[AccountResponse]:
    result: Result = await accounts_module.execute_query_async(command=ListAccountsRequest())
    return result.match(
        on_success=lambda accounts: [AccountResponse.from_domain(account) for account in accounts],
        on_failure=_raise_http(status.HTTP_400_BAD_REQUEST),
    )


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
async def update_account(
    account_id: str,
    payload: UpdateAccountRequest,
    current_user: Account = Depends(jwt.get_current_user),
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> AccountResponse:
    result: Result = await accounts_module.execute_command_async(
        command=UpdateAccountRequest(
            account_id=account_id,
            email=payload.email,
            password=payload.password,
            is_active=payload.is_active,
        )
    )
    return result.match(
        on_success=lambda account: AccountResponse.from_domain(account),
        on_failure=_raise_http(status.HTTP_400_BAD_REQUEST),
    )


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an account",
)
async def delete_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
    accounts_module: AccountsModule = Depends(AccountsModule),
) -> None:
    result: Result = await accounts_module.execute_command_async(command=DeleteAccountRequest(account_id=account_id))
    result.match(
        on_success=lambda _: None,
        on_failure=_raise_http(status.HTTP_404_NOT_FOUND),
    )
