from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import *

from .helpers import get_random_alphanumeric_string

from django.conf import settings

from django.core.mail import send_mail

def set_user(sender,instance,created,**kwargs):
    if created:
        account = Account.objects.create(
            user=instance,
            public_username=str(get_random_alphanumeric_string(5)) + str(instance.id) + str(get_random_alphanumeric_string(5)),
        )

        print("signal of set_user was called")

        #send email
        app_name = "Testing"
        name = "Bruh"
        subject = f'Welcome to {app_name} App'
        message = f'Hi {name} ,thankyou for registering in {app_name}.'
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [instance.email,]
        send_mail(subject,message,email_from,recepient_list)

                
post_save.connect(set_user,sender=User,dispatch_uid="unique")
