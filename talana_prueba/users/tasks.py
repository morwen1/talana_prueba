from django.contrib.auth import get_user_model



from config import celery_app


# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


# Celery
from celery.decorators import task, periodic_task

# Utilities
import jwt
import time
from datetime import timedelta


User = get_user_model()




def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.email,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return token


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk , none:None):
    """Send account verification link to given user."""
    user_pk= user_pk['user_pk']
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! Verify your account '.format(user.username)
    from_email = 'Comparte Ride <noreply@prueba.com>'
    content = render_to_string(
        'users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()

