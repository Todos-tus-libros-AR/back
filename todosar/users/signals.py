from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from utils.email import Emailing


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            f"{settings.FRONTEND_URL}/recuperar-password",
            reset_password_token.key,
        ),
    }

    emailing = Emailing()
    emailing.regenerate_password_email(context)
