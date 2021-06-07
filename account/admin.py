from django.contrib import admin
from .models import Article, User,Token
# Register your models here.

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Token)
