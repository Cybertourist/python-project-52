from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm

User = get_user_model()

class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('У вас нет прав для изменения другого пользователя.'),
        )
        return redirect('users')

class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')

class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно изменен')

class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно удален')

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/form.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('index')
    success_message = _('Вы залогинены')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)