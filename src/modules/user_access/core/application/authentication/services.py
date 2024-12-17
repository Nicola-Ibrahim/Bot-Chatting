from abc import ABC, abstractmethod

from django.http import HttpRequest

from apps.core.otp.services import AbstractTOTPService

from .utils import send_otp_login_email


class AbstractAuthService(ABC):
    @abstractmethod
    def initiate_otp_login(
        self, request: HttpRequest, user_id: int | str, user_email: str, user_full_name: str
    ) -> None:
        raise NotImplementedError("The generate method must be implemented in subclasses.")


class AuthService(AbstractAuthService):
    def __init__(self, otp_service: AbstractTOTPService) -> None:
        self.otp_service = otp_service

    def initiate_otp_login(
        self, request: HttpRequest, user_id: int | str, user_email: str, user_full_name: str
    ) -> None:
        """
        Generates an OTP token and sends an email to the user with the login URL.

        Args:
            request (HttpRequest): The current HTTP request.
            user_id (int | str): The ID of the user for whom the OTP is generated.
            user_email (str): The email address of the user.
            user_full_name (str): The full name of the user.
        """
        # Generate OTP token for the user
        otp_token = self.otp_service.generate_totp_token(request=request, user_id=user_id)

        # Send OTP email
        send_otp_login_email(
            request=request,
            otp_token=otp_token,
            recipient_id=user_id,
            recipient_full_name=user_full_name,
            recipient_email=user_email,
        )
