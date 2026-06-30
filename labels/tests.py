from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class TestLabelCRUD(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.label = Label.objects.create(name='Баг')

    def test_label_list(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)

    def test_label_create(self):
        self.client.login(username='testuser', password='password123')
        data = {'name': 'Фича'}
        response = self.client.post(reverse('create_label'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Фича').exists())

    def test_label_delete_unused(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('delete_label', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_used_in_task(self):
        self.client.login(username='testuser', password='password123')
        status = Status.objects.create(name='Новый')
        task = Task.objects.create(
            name='Задача с меткой', status=status, author=self.user
        )
        task.labels.add(self.label)

        response = self.client.post(
            reverse('delete_label', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())