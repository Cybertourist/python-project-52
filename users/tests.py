from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestUserViewSet(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.user.set_password('admin')
        self.user.save()

    def test_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_user_create(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'VeryComplexPassword123!',
            'password2': 'VeryComplexPassword123!',
        }
        response = self.client.post(reverse('create_user'), data)
        
        if response.status_code == 200:
            self.fail(
                "Form submission failed: "
                f"{response.context['form'].errors}"
            )
            
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_success(self):
        self.client.login(username='admin', password='admin')
        self.user.username = 'old_admin'
        self.user.save()
        
        data = {
            'username': 'admin',
            'first_name': 'Updated',
            'last_name': 'Adminov',
            'password1': 'VeryComplexPassword123!',
            'password2': 'VeryComplexPassword123!',
        }
        response = self.client.post(
            reverse('update_user', args=[self.user.pk]), data
        )
        
        if response.status_code == 200:
            self.fail(f"Update failed: {response.context['form'].errors}")
            
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.username, 'admin')

    def test_user_update_other_user(self):
        other_user = User.objects.create_user(username='other')
        self.client.login(username='admin', password='admin')
        
        data = {'username': 'other', 'first_name': 'Hacked'}
        response = self.client.post(
            reverse('update_user', args=[other_user.pk]), data
        )
        
        self.assertEqual(response.status_code, 302)
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.first_name, 'Hacked')

    def test_user_delete(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('delete_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())