from django.urls import path
from . import views

urlpatterns = [
    path('', views.StatusListView.as_class_view() if hasattr(views.StatusListView, 'as_class_view') else views.StatusListView.as_view(), name='statuses'),
    path('create/', views.StatusCreateView.as_view(), name='create_status'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='update_status'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete_status'),
]