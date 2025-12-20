from . import views
from django.urls import path

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.main, name='main'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/',  views.user_logout, name="logout")
]