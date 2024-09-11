from django.urls import path
from . import views
urlpatterns = [
    path('', views.order_cart.as_view(), name='cart'),
    path('min-mix/', views.change_min_mix, name='change'),
    path('remove/', views.remove_to, name='remove'),
    ]