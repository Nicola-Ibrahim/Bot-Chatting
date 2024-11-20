from apps.core.notifications.email.content import HtmlEmailContent
from apps.core.notifications.email.sender import DjangoEmailSender
from apps.core.notifications.email.services import EmailService
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _

