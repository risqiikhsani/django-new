import profile
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer



class Account_Serializer(serializers.ModelSerializer):
	profile_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
            ('small', 'thumbnail__200x200'),
            ('medium', 'thumbnail__400x400'),
		]
	)
	poster_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
            ('small', 'thumbnail__200x200'),
            ('medium', 'thumbnail__400x400'),
		]
	)
	class Meta:
		model = Account
		fields = ['name','public_username','profile_picture','profile_picture','poster_picture']

class User_Serializer(serializers.ModelSerializer):
	account = Account_Serializer()
	
	class Meta:
		model = User
		fields = ['id','account']

class PostList_Serializer(serializers.ModelSerializer):
	user = User_Serializer()
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['user']

class PostDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['user']

class CommentList_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['user','post']

class CommentDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['user','post']

class ReplyList_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Reply
		fields = '__all__'
		read_only_fields = ['user','comment']

class ReplyDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Reply
		fields = '__all__'
		read_only_fields = ['user','comment']
	