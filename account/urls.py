from django.urls import path

from account import views

urlpatterns = [
    path('', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),

]