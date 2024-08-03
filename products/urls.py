from django.urls import path

from . import views

urlpatterns = [
    path('',views.productListView.as_view(),name='products'),
    path('category/<str:cate_gory>',views.productListView.as_view(),name='products_category'),
    path('detail/<slug:slug>/<int:pk>',views.productDetailView.as_view(),name='detail'),
    ]