from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class TestStatusCRUD(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.status = Status.objects.create(name='Новый')

    def test_status_list_unauthorized(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_status_list_authorized(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        self.client.login(username='testuser', password='password123')
        data = {'name': 'В работе'}
        response = self.client.post(reverse('create_status'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='password123')
        data = {'name': 'На тестировании'}
        response = self.client.post(
            reverse('update_status', args=[self.status.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'На тестировании')

    def test_status_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('delete_status', args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())