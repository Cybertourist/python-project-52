from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from statuses.models import Status

from .models import Task


class TestTaskCRUD(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='author', password='password123'
        )
        self.other_user = User.objects.create_user(
            username='other', password='password123'
        )
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.author
        )

    def test_filter_by_status(self):
        self.client.login(username='author', password='password123')
        other_status = Status.objects.create(name='В работе')
        Task.objects.create(
            name='Другая задача',
            status=other_status,
            author=self.author,
        )

        response = self.client.get(reverse('tasks'), {'status': self.status.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)

    def test_filter_only_my_tasks(self):
        Task.objects.create(
            name='Чужая задача',
            status=self.status,
            author=self.other_user,
        )

        self.client.login(username='author', password='password123')
        response = self.client.get(reverse('tasks'), {'only_my_tasks': 'on'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Тестовая задача')

    def test_task_list(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_task_create(self):
        self.client.login(username='author', password='password123')
        data = {
            'name': 'Новая уникальная задача',
            'description': 'Описание',
            'status': self.status.pk,
        }
        response = self.client.post(reverse('create_task'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.filter(name='Новая уникальная задача').exists()
        )
        task = Task.objects.get(name='Новая уникальная задача')
        self.assertEqual(task.author, self.author)

    def test_task_delete_by_author(self):
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('delete_task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        self.client.login(username='other', password='password123')
        response = self.client.post(reverse('delete_task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())