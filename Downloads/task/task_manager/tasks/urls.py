from django.urls import path
from .views import *
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/create/', create_task, name='create-task'),
    path('tasks/assign/', assign_task, name='assign-task'),
    path('users/list/', get_normal_users, name='normal_users_list'),
    path("tasks/user/<int:user_id>/", get_tasks_for_user, name="get-tasks-for-user"),
    path("tasks/update/<int:task_id>/", update_task, name="task_update"),
    path("tasks/list/", list_tasks, name="list_tasks"),
]
