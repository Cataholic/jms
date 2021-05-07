from django.urls import path, include
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetListView.as_view(), name='list'),
    path('create/', views.AssetCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('detail/', views.AssetDetailView.as_view(), name='detail'),
        path('update/', views.AssetUpdateView.as_view(), name='update'),
        path('delete/', views.AssetDeleteView.as_view(), name='del'),
    ])),
]