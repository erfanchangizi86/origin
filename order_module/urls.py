from django.urls import path

from order_module import views

urlpatterns = [
    path('add/', views.add_to_products.as_view(), name='add_product'),
]