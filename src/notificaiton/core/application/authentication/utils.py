from apps.core.notifications.email.content import HtmlEmailContent
from apps.core.notifications.email.sender import DjangoEmailSender
from apps.core.notifications.email.services import EmailService
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _


def construct_otp_login_url(request: HttpRequest, user_id: int | str) -> str:
    """
    Constructs a fully qualified OTP login URL based on the current request scheme and site.

    Args:
        request (HttpRequest): The HTTP request object.
        otp_token (str): The OTP token to include in the URL.

    Returns:
        str: The fully qualified OTP login URL.
    """
    current_site = get_current_site(request)
    otp_login_path = reverse("accounts:otp_login_user", kwargs={"pk": user_id})
    scheme = request.scheme
    return f"{scheme}://{current_site.domain}{otp_login_path}"


def construct_website_url(request: HttpRequest) -> str:
    """
    Constructs a fully qualified website URL based on the current request scheme and site.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        str: The fully qualified website URL.
    """
    current_site = get_current_site(request)
    homepage_path = reverse("pages:start")
    scheme = request.scheme
    return f"{scheme}://{current_site.domain}{homepage_path}"


def send_otp_login_email(
    request: HttpRequest, otp_token: str, recipient_id: int | str, recipient_full_name: str, recipient_email: str
) -> None:
    """
    Sends an OTP email to the specified recipient for easy login.

    Args:
        request (HttpRequest): The HTTP request object.
        otp_token (str): The OTP token to include in the email.
        recipient_full_name (str): The full name of the email recipient.
        recipient_email (str): The recipient's email address.
    """

    otp_login_url = construct_otp_login_url(request, recipient_id)
    website_url = construct_website_url(request)

    # Define the context for the email template
    email_context = {
        "token": otp_token,
        "full_name": recipient_full_name,
        "user_email": recipient_email,
        "otp_login_url": otp_login_url,
        "website_url": website_url,
    }

    # Create the HTML email content
    email_content = HtmlEmailContent(
        subject=_("Your OTP for Easy Login"),
        template_name="accounts/emails/email_otp_login.html",
        context=email_context,
    )

    # Initialize and send the email using EmailService
    email_service = EmailService(content=email_content, sender=DjangoEmailSender(), to_emails=[recipient_email])
    email_service.send()
