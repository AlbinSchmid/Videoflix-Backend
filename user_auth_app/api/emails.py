from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django_rq import job
from rq import Retry
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator


@job('default', retry=Retry(max=3, interval=[10, 30, 60]))
def send_welcome_email(user):
    """
    Send a welcome email to the user after registration.
    The email contains an activation link for the user's account.
    """
    subject = 'Welcome to Videoflix!'
    from_email = 'noreply@videoflix.de'
    to = [user.email]

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"https://videoflix.albin-schmid.com/activate/{uid}/{token}"

    html_content = render_to_string('emails/confirm_email.html', {
        'activation_link': activation_link
    })
    text_content = 'Hello and welcome!, Thank you for registering with Videoflix.'

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

@job('default', retry=Retry(max=3, interval=[10, 30, 60]))
def send_password_reset_email(user):
    """
    Send a password reset email to the user.
    The email contains a link to reset the user's password.
    """
    subject = 'Reset your Videoflix password'
    from_email = 'noreply@videoflix.de'
    to = [user.email]

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"https://videoflix.albin-schmid.com/reset-password/{uid}/{token}"

    html_content = render_to_string('emails/reset_password.html', {
        'reset_link': reset_link
    })
    text_content = 'Hello, to reset your password pleace contact our Support'

    email = EmailMultiAlternatives(
        subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
