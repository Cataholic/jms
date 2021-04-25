from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('add/', views.user_add, name='user_add'),
    path('<int:user_id>/', include([
        path('update/', views.user_update, name='user_update'),
        path('detail/', views.user_detail, name='user_detail'),
        path('del/', views.user_del, name='user_del'),
    ])),
]
