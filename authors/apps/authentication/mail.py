import os
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import User


class MailSender:
    """Creates a mail and sends it to the receipient"""

    @staticmethod
    def send_email_message(recipient, token, request):
        """Recieve the user's request and sends back a response"""
        title = "Authors Heaven.Password reset"
        mail_sender = os.getenv('MAIL_SENDER')
        full_mail = render_to_string(
            'verify_mail.html',
            {
                'content': 'You are receiving this email because we received a'
                           ' password reset request for your account',
                'title': title,
                'username': User.objects.get(email=recipient).get_short_name(),
                'verification_link': "https://the-phoenix-frontend-staging.herokuapp.com" +      # noqa 501
                                     "/update-password/" +
                                     token.decode(),
            })
        send_mail(title, full_mail, mail_sender, [
            recipient], html_message=full_mail)
        response = {
            'message': 'A password reset link has been sent to your email'
        }
        return response
