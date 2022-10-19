from django.contrib import admin

from .models import Account, Post, Comment, Reply, Like



from django.contrib.auth.admin import UserAdmin
from .models import User
admin.site.register(User, UserAdmin)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'public_username',
        'profile_picture',
        'poster_picture',
    )
    list_filter = ('user',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'time_creation')
    list_filter = ('time_creation',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text', 'time_creation')
    list_filter = ('post', 'user', 'time_creation')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'text', 'time_creation')
    list_filter = ('comment', 'user', 'time_creation')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'comment',
        'reply',
        'time_creation',
    )
    list_filter = ('user', 'post', 'comment', 'reply', 'time_creation')