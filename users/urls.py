from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add/', views.user_add, name='add'),
    path('<int:pk>/', include([
        path('update/', views.user_update, name='update'),
        path('detail/', views.user_detail, name='detail'),
        path('del/', views.user_del, name='del'),
    ])),
]
