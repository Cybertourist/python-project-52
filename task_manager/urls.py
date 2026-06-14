from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('users/', include('users.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]