from django.urls import path
from mainapp.views import user_list, user_list2, user_list3, add_user
from mainapp.views import update_user, delete_user

urlpatterns = [
    path('list', user_list3),
    path('add', add_user),
    path('update', update_user),
    path('del', delete_user),
]
