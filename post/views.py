from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import generics, mixins,response, decorators, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsOwnerOrReadOnly
from .models import *


from django_filters.rest_framework import DjangoFilterBackend

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('post-list', request=request, format=format)
	})

# Using mixins
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from .serializers import User_Serializer
class UserList(mixins.ListModelMixin,generics.GenericAPIView):
	serializer_class = User_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = User.objects.all()

	def get(self, request, *args, **kwargs):
		return self.list(request,*args,**kwargs)



from .serializers import PostList_Serializer
from .filters import PostFilter
class PostList(mixins.ListModelMixin,
				  mixins.CreateModelMixin,
				  generics.GenericAPIView):
	serializer_class = PostList_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Post.objects.all()
	filter_backends = {DjangoFilterBackend,}
	filterset_class = PostFilter

	
	# def get_queryset(self):
	# 	if 'user_id' in self.kwargs:
	# 		return Post.objects.all().filter(user=self.kwargs['user_id'])
	# 	elif 'search' in self.request.query_params:
	# 		return Post.objects.all().filter(
	# 			Q(text__icontains=self.request.query_params['search'])  
	# 		)
	# 	else:
	# 		return Post.objects.all()


	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


from .serializers import PostDetail_Serializer
class PostDetail(mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin,
					generics.GenericAPIView):
	queryset = Post.objects.all()				
	serializer_class = PostDetail_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


# Using generic class-based views 
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from .serializers import CommentList_Serializer
class CommentList(generics.ListCreateAPIView):
	serializer_class = CommentList_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def get_queryset(self):
		if 'post_id' in self.kwargs:
			return Comment.objects.all().filter(post=self.kwargs['post_id'])
		else:
			return Comment.objects.all()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user,post=Post.objects.get(id=self.kwargs['post_id']))


from .serializers import CommentDetail_Serializer
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Comment.objects.all()				
	serializer_class = CommentDetail_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


from .serializers import ReplyList_Serializer
class ReplyList(generics.ListCreateAPIView):
	serializer_class = ReplyList_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def get_queryset(self):
		if 'comment_id' in self.kwargs:
			return Reply.objects.all().filter(comment=self.kwargs['comment_id'])
		else:
			return Reply.objects.all()


	def perform_create(self, serializer):
		serializer.save(user=self.request.user,comment=Comment.objects.get(id=self.kwargs['comment_id']))


from .serializers import ReplyDetail_Serializer
class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Reply.objects.all()				
	serializer_class = ReplyDetail_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


