from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class Login_Serializer(serializers.Serializer):
	username = serializers.CharField(max_length=300,required=True)
	password = serializers.CharField(required=True,write_only=True)



class Register_Serializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True,required=True,style={"input_type":"password"})
	password2 = serializers.CharField(write_only=True,style={"input_type":"password"},label="Confirm password")
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"password",
			"password2",
		]
		extra_kwargs = {"password":{"write_only":True}}

	def validate_username(self,value):
		if User.objects.all().filter(username=value).exists():
			raise serializers.ValidationError("Username is already used !")
		return value

	def validate_email(self,value):
		if User.objects.all().filter(email=value).exists():
			raise serializers.ValidationError("Email is already used !")
		return value


	def create(self,validated_data):
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]
		password2 = validated_data["password2"]
		if password != password2:
			raise serializers.ValidationError("The two passwords differ")
		user = User(username=username, email=email)
		user.set_password(password)
		user.save()
		return user