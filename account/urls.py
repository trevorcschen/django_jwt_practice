from django.urls import path,include
from account import views

urlpatterns = [
    path('', views.article_list ),
]