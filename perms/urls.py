from django.urls import path, include
from . import views

app_name = 'perms'

urlpatterns = [
    path('', views.PermListView.as_view(), name='list'),
    path('create/', views.PermCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('detail/', views.PermDetailView.as_view(), name='detail'),
        path('delete/', views.PermDeleteView.as_view(), name='del'),
    ])),
]