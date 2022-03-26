from django.core import mail
from django.template.loader import render_to_string
from django.shortcuts import reverse
from django.conf import settings


def send_mail_to_user(user_email):
    html_message = render_to_string('mainapp/templates/greetings_first_pattern.html',
                                    context={'user_email': user_email})
    mail.send_mail('Greetings', 'Hello, Our Greetings!', 'testuser@mail.ru', [user_email],
                   html_message=html_message)
