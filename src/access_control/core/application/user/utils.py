from apps.core.notifications.email.content import HtmlEmailContent
from apps.core.notifications.email.sender import DjangoEmailSender
from apps.core.notifications.email.services import EmailService
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _


def construct_otp_verification_url(request: HttpRequest, user_id: int | str) -> str:
    """
    Constructs a fully qualified OTP verification URL using the current request scheme and site.

    Args:
        request (HttpRequest): The HTTP request object.
        otp_token (str): The OTP token to include in the URL.

    Returns:
        str: The fully qualified OTP verification URL.
    """
    current_site = get_current_site(request)
    otp_verification_path = reverse("accounts:account_verification", kwargs={"pk": user_id})
    scheme = request.scheme
    return f"{scheme}://{current_site.domain}{otp_verification_path}"


def construct_website_home_url(request: HttpRequest) -> str:
    """
    Constructs a fully qualified website home URL using the current request scheme and site.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        str: The fully qualified website home URL.
    """
    current_site = get_current_site(request)
    homepage_path = reverse("pages:start")
    scheme = request.scheme
    return f"{scheme}://{current_site.domain}{homepage_path}"


def send_account_verification_otp_email(
    request: HttpRequest, otp_token: str, recipient_id: int | str, recipient_full_name: str, recipient_email: str
) -> None:
    """
    Sends an OTP email for account verification to the specified recipient.

    Args:
        request (HttpRequest): The HTTP request object.
        otp_token (str): The OTP token to include in the email.
        recipient_full_name (str): The full name of the email recipient.
        recipient_email (str): The recipient's email address.
    """
    otp_verification_url = construct_otp_verification_url(request, recipient_id)
    website_home_url = construct_website_home_url(request)

    # Define the context for the email template
    email_context = {
        "token": otp_token,
        "full_name": recipient_full_name,
        "user_email": recipient_email,
        "otp_verification_url": otp_verification_url,
        "website_url": website_home_url,
    }

    # Create the HTML email content
    email_content = HtmlEmailContent(
        subject=_("Your OTP for Account Verification"),
        template_name="accounts/emails/email_otp_verification.html",
        context=email_context,
    )

    # Initialize and send the email using EmailService
    email_service = EmailService(content=email_content, sender=DjangoEmailSender(), to_emails=[recipient_email])
    email_service.send()
