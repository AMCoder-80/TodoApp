from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


app_name = 'base'

urlpatterns = [
    path('first/', first),
    path('tasks/', TaskList.as_view(), name='task_list'),
    path('detail/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('create/', TaskCreate.as_view(), name='task_create'),
    path('update/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
    path('', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base:login')), name='logout'),
    path('register/', UserCreation.as_view(), name='register'),
]