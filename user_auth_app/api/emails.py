from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

def send_welcome_email(user):
    subject = 'Willkommen bei Videoflix!'
    from_email = 'noreply@videoflix.de'
    to = [user.email]

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://localhost:4200/activate/{uid}/{token}"

    html_content = render_to_string('emails/confirm_email.html', {
        'user': user,
        'activation_link': activation_link
    })
    text_content = 'Hallo {}, danke für deine Registrierung bei Videoflix.'.format(user.email)

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()