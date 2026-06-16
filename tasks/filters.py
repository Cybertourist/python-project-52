from django import forms
import django_filters
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from .models import Task
from statuses.models import Status
from django.contrib.auth.models import User
from labels.models import Label

class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    executor = ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
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