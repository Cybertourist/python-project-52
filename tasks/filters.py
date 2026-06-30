from django import forms
from django.contrib.auth.models import User
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    executor = ModelChoiceFilter(
        queryset=User.objects.all(), label='Исполнитель'
    )
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label='Метка')

    only_my_tasks = BooleanFilter(
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
        label='Только свои задачи'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_my_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset