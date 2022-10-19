from typing_extensions import Required
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

from versatileimagefield.fields import VersatileImageField

User = get_user_model()

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# when creating custom user model
# dont forget to add AUTH_USER_MODEL in settings.py
# also register the model in app's admin.py
# it's recommended that you set it before there's a database 
# run migrate afterwards 
class User(AbstractUser):
	phone_number = PhoneNumberField(required=False)




class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	public_username = models.CharField(max_length=100, null=True, blank=True)


	profile_picture = VersatileImageField(
		upload_to='images/profile_picture/',
		null=True, 
		blank=True
	)

	poster_picture = VersatileImageField(
		upload_to='images/poster_picture/',
		null=True, 
		blank=True
	)

	def __str__(self):
		return str(self.id)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)


class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)

class Reply(models.Model):
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)



	