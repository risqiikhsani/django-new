from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import *

from .helpers import get_random_alphanumeric_string

def set_user(sender,instance,created,**kwargs):
    if created:
        account = Account.objects.create(
            user=instance,
            public_username=str(get_random_alphanumeric_string(5)) + str(instance.id) + str(get_random_alphanumeric_string(5)),
        )

        print("signal of set_user was called")
post_save.connect(set_user,sender=User,dispatch_uid="unique")
