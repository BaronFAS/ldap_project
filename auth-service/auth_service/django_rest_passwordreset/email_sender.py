from pathlib import Path
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from auth_service.config import settings
from auth_service.settings import BASE_DIR


def password_reset_token_created(reset_password_token, invite=False):
    """
    :param reset_password_token: Token Model Object
    :param invite: bool
    :return:
    """
    # send an e-mail to the user

    if reset_password_token.user.company and reset_password_token.user.company.password_reset_uri:
        password_reset_uri = reset_password_token.user.company.password_reset_uri
        company_name = reset_password_token.user.company.name
    else:
        password_reset_uri = settings.password_reset_uri
        company_name = "Cyngn"

    context = {
        "current_user": reset_password_token.user,
        "user_name": reset_password_token.user.first_name,
        "email": reset_password_token.user.email,
        "reset_password_url": f"{password_reset_uri}?token={reset_password_token.key}"
    }

    # render email text
    if invite:
        email_html_message = render_to_string("user_set_password.html", context)
        header_title = f"You have been invited to join {company_name}'s Insight team!"
    else:
        email_html_message = render_to_string("user_reset_password.html", context)
        header_title = "Password Reset for Cyngn"

    msg = EmailMultiAlternatives(
        # title:
        header_title,
        # message:
        email_html_message,
        # from:
        f"{settings.email_sender_display_name} <{settings.email_host_user}>",
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    img_path = Path(BASE_DIR, "django_rest_passwordreset/img/logo.png")
    with open(img_path, "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<logo>")
        img.add_header("Content-Disposition", "inline", filename="logo")
        msg.attach(img)
    msg.send()
