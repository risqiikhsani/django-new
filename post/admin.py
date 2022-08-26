from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)