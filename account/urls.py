from django.urls import path

from account import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
]