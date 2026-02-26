from datetime import timedelta

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException, status

from ......modules.accounts.application.account.service import AccountService
from ......modules.accounts.application.authentication.service import AuthenticationService
from ......modules.accounts.application.registration.service import RegistrationService
from ......modules.accounts.domain.account import Account
from ......modules.accounts.infrastructure.configuration.containers import AccountsDIContainer
from ..security import jwt
from .account_response import AccountResponse
from .delete_account_request import DeleteAccountRequest
from .get_account import GetAccountRequest
from .list_accounts import ListAccountsRequest
from .login_request import LoginRequest
from .login_response import LoginResponse
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
    registration_service: RegistrationService = Depends(Provide[AccountsDIContainer.registration_service]),
) -> AccountResponse:
    try:
        command = RegisterAccountRequest(email=payload.email, password=payload.password)
        account = registration_service.register(command)
        return AccountResponse.from_domain(account)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post(
    "/verify",
    response_model=AccountResponse,
    summary="Verify an account",
)
async def verify_account(
    payload: VerifyAccountRequest,
    account_service: AccountService = Depends(Provide[AccountsDIContainer.account_service]),
) -> AccountResponse:
    try:
        command = VerifyAccountRequest(account_id=payload.account_id)
        account = account_service.verify(command)
        return AccountResponse.from_domain(account)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate an account",
)
async def login(
    payload: LoginRequest,
    authentication_service: AuthenticationService = Depends(Provide[AccountsDIContainer.authentication_service]),
) -> LoginResponse:
    try:
        command = LoginRequest(email=payload.email, password=payload.password)
        data = authentication_service.login(command)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    # 3. THE "SENIOR" WAY: SET HTTPONLY COOKIE
    # The browser handles "saving" this automatically.

    access_token = jwt.create_access_token({"sub": str(data[0].id.value)}, expires_delta=timedelta(minutes=30))
    refresh_token = data[1].refresh_token
    session_id = data[1].session_id

    # We also set a Refresh Token (usually in a separate cookie or DB)

    # 4. DATA FOR FRONTEND
    # Return non-sensitive UI data so the frontend knows who is logged in

    return LoginResponse(
        user=AccountResponse.from_domain(data[0]),
        access_token=access_token,
        refresh_token=refresh_token,
        session_id=session_id,
    )


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Retrieve a single account",
)
async def get_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
    account_service: AccountService = Depends(Provide[AccountsDIContainer.account_service]),
) -> AccountResponse:
    try:
        command = GetAccountRequest(account_id=account_id)
        account = account_service.get(command)
        return AccountResponse.from_domain(account)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="List all accounts",
)
async def list_accounts(
    current_user: Account = Depends(jwt.get_current_user),
    account_service: AccountService = Depends(Provide[AccountsDIContainer.account_service]),
) -> list[AccountResponse]:
    try:
        command = ListAccountsRequest()
        accounts = account_service.list(command)
        return [AccountResponse.from_domain(account) for account in accounts]
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


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
    account_service: AccountService = Depends(Provide[AccountsDIContainer.account_service]),
) -> AccountResponse:
    try:
        command = UpdateAccountRequest(
            account_id=account_id,
            email=payload.email,
            password=payload.password,
            is_active=payload.is_active,
        )
        account = account_service.update(command)
        return AccountResponse.from_domain(account)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an account",
)
async def delete_account(
    account_id: str,
    current_user: Account = Depends(jwt.get_current_user),
    account_service: AccountService = Depends(Provide[AccountsDIContainer.account_service]),
) -> None:
    try:
        command = DeleteAccountRequest(account_id=account_id)
        account_service.remove(command)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
