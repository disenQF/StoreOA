from django.urls import path
from mainapp.views import user_list, user_list2, user_list3, add_user, all_store, count_fruit
from mainapp.views import update_user, delete_user, find_fruit, find_store
from mainapp import user_v


urlpatterns = [
    path('list', user_list3),
    path('add', add_user),
    path('update', update_user),
    path('del', delete_user),
    path('find', find_fruit),
    path('store', find_store),
    path('store_all', all_store),
    path('count', count_fruit),
    path('login', user_v.login)
]
