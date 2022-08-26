from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import generics, mixins,response, decorators, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsOwnerOrReadOnly
from .models import *


from .serializers_auth import Register_Serializer
class Register(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny,]
	serializer_class = Register_Serializer

	def post(self,request, *args, **kwargs):
		serializer =self.get_serializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		user = serializer.save()
		return Response("Account registered successfully!",status.HTTP_201_CREATED)

from .serializers_auth import Login_Serializer
class Login(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny, ]
	serializer_class = Login_Serializer

	def get_tokens_for_user(self,user):
		return RefreshToken.for_user(user)

	def post(self,request,*args,**kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			username=serializer.validated_data['username']
			password=serializer.validated_data['password']
			if username is None or password is None:
				return Response({'error':'Should provide username and password'}, status=status.HTTP_400_BAD_REQUEST)
			user = authenticate(username=username,password=password)
			if not user:
				return Response({'error':'invalid credentials'},status=status.HTTP_404_NOT_FOUND)

			refresh = self.get_tokens_for_user(user)

			data = {
				'id':str(user.id),
				'name':str(user.account.name),
				'refresh_token':str(refresh),
				'access_token':str(refresh.access_token),
			}

			return Response(data,status=status.HTTP_201_CREATED)
