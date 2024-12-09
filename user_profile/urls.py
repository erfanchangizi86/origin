from django.urls import path
from . import views
urlpatterns = [
    path('', views.order_cart.as_view(), name='cart'),
    path('min-mix/', views.change_min_mix, name='change'),
    path('remove/', views.remove_to, name='remove'),
    path('my-profile/', views.UserPanelDashboardPage.as_view(), name='profile'),
    path('my-profile/edite', views.my_form_edit.as_view(), name='edit_profile'),
    ]