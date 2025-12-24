from . import views
from django.urls import path

urlpatterns = [
    path('main/', views.main),
    path('set-task/', views.set_task),
    path('edit-task/', views.edit_task),
    path("get-task/", views.get_task),
    path("summary/", views.summary),
    path("delete-task/", views.delete_task)
]