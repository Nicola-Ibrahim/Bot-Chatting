"""HTTP endpoints for accounts management."""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.accounts.domain.aggregates.account.account import Account as DomainAccount
from src.modules.accounts.infrastructure.configuration.startup import AccountsStartUp

from ..security import jwt
from .account_response import AccountResponse
from .login_request import LoginRequest
from .login_response import LoginResponse
from .register_account_request import RegisterAccountRequest
from .update_account_request import UpdateAccountRequest
from .verify_account_request import VerifyAccountRequest

router = APIRouter(prefix="/accounts", tags=["accounts"])


def _service():
    AccountsStartUp.initialize()
    service = AccountsStartUp.service
    if not service:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Accounts service unavailable")
    return service


def _get_account_or_404(account_id: str) -> DomainAccount:
    service = _service()
    account = service.get_user(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponse,
    summary="Register a new account",
)
def register_account(payload: RegisterAccountRequest) -> AccountResponse:
    try:
        service = _service()
        account = service.register_user(email=payload.email, password=payload.password)
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
        service = _service()
        account = service.verify_user(payload.account_id)
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
        service = _service()
        account, dto = service.authenticate(email=payload.email, password=payload.password)
        access_token = jwt.create_access_token(
            {"sub": str(account.id.value)}, expires_delta=timedelta(minutes=30)
        )
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
    current_user: DomainAccount = Depends(jwt.get_current_user),
) -> AccountResponse:
    account = _get_account_or_404(account_id)
    return AccountResponse.from_domain(account)


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="List all accounts",
)
def list_accounts(current_user: DomainAccount = Depends(jwt.get_current_user)) -> list[AccountResponse]:
    service = _service()
    accounts = service.list_users()
    return [AccountResponse.from_domain(account) for account in accounts]


@router.get(
    "/me",
    response_model=AccountResponse,
    summary="Retrieve the authenticated account",
)
def get_current_account(current_user: DomainAccount = Depends(jwt.get_current_user)) -> AccountResponse:
    return AccountResponse.from_domain(current_user)


@router.patch(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Update an account",
)
def update_account(
    account_id: str,
    payload: UpdateAccountRequest,
    current_user: DomainAccount = Depends(jwt.get_current_user),
) -> AccountResponse:
    try:
        service = _service()
        account = service.update_user(
            account_id,
            email=payload.email,
            password=payload.password,
            is_active=payload.is_active,
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
    current_user: DomainAccount = Depends(jwt.get_current_user),
) -> None:
    try:
        service = _service()
        service.remove_user(account_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


__all__ = ["router"]
