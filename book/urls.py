from . import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
]