from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('add_category/', views.add_category, name="add_category"),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_link/<int:category_id>/', views.add_link, name='add_link'),
    path('edit_link/<int:link_id>/', views.edit_link, name='edit_link'),
    path('delete_link/<int:link_id>/', views.delete_link, name='delete_link'),
    path('task/new/', views.create_task, name='create_task'),
    path('task/read/<int:task_id>', views.read_task, name='read_task'),
    path('task/update/<int:task_id>', views.update_task, name="update_task"),
    path('task/delete/<int:task_id>', views.delete_task, name="delete_task"),
    path('task/delete/finished/all', views.delete_finished_tasks, name="delete_finished_tasks"),
    path('task/update/status/<int:task_id>', views.finish_unfinish_task, name="finish_unfinish_task")
]