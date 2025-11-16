"""
Simple chat endpoint for the chats module.

This module defines a minimal chat interface which accepts a plain
text message from the client and returns a corresponding response.
It serves as a placeholder implementation demonstrating how a chat
endpoint might be integrated into the wider API.  In a real system
this would forward the request to a backend service capable of
generating conversational replies, such as an LLM or rule‑based
engine.

The chat endpoint supports both authenticated and unauthenticated
requests.  When called without a bearer token the request will be
treated as coming from a guest user.  When a token is supplied the
``current_user`` parameter will be populated by the
``get_current_user_optional`` dependency.
"""

from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src.api.routers.accounts.v1.security.jwt import get_current_user_optional
from src.modules.accounts.domain.aggregates.account.account import Account as DomainUser


router = APIRouter(prefix="/accounts", tags=["accounts"])


class ChatRequest(BaseModel):
    """Request schema for the chat endpoint."""

    message: str


class ChatResponse(BaseModel):
    """Response schema for the chat endpoint."""

    response: str


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a chat message",
    responses={status.HTTP_200_OK: {"description": "Chat response"}},
)
def chat(
    req: ChatRequest,
    current_user: Optional[DomainUser] = Depends(get_current_user_optional),
) -> ChatResponse:
    """Echo the incoming message back to the client.

    If a valid bearer token is provided the ``current_user`` parameter will
    contain the authenticated user.  When called without a token this
    parameter will be ``None`` and the request is treated as a guest
    chat.  In the future this function could delegate to a
    conversational service such as an LLM or rule‑based engine.  For
    now it simply replies with the user's message prefixed to indicate
    whether the request was authenticated or not.
    """
    # Prefix the reply to differentiate between authenticated and guest chats
    if current_user is not None:
        reply = f"[user:{current_user.email}] You said: {req.message}"
    else:
        reply = f"[guest] You said: {req.message}"
    return ChatResponse(response=reply)


__all__ = ["router"]
