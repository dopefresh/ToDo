from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'), # mainpage
    path('<int:pk>/', views.GroupView.as_view(), name = 'group'), # page of a group
    path('delete_group/<int:pk>/', views.DeleteGroupView.as_view(), name = 'delete_group'),
    path('update_group/<int:pk>/', views.UpdateGroupView.as_view(), name = 'update_group'),
    path('update_task/<int:pk>/', views.UpdateTaskView.as_view(), name = 'update_task'),
    path('delete_task/<int:pk>/', views.DeleteTaskView.as_view(), name = 'delete_task'),
]
