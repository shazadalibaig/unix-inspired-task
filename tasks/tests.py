from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITests(APITestCase):

    def setUp(self):
        self.task_create_url = reverse('task_list_create')  # URL name in urls.py
        self.task1 = Task.objects.create(name='Sample Task', status='running')
        self.task2 = Task.objects.create(name='Finished Task', status='completed')

    def test_lists_tasks(self):
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task_success(self):
        data = {"name": "New Task", "status": "running"}
        response = self.client.post(self.task_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_create_task_duplicate_name_fails(self):
        data = {"name": "Sample Task", "status": "running"}
        response = self.client.post(self.task_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_task_same_name_allowed_if_previous_deleted(self):
        data = {"name": "Finished Task", "status": "running"}
        response = self.client.post(self.task_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task_success(self):
        url = reverse('task_update_del', kwargs={'pk': self.task1.id})
        data = {"name": "Updated Task", "status": "completed"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, "Updated Task")
        self.assertEqual(self.task1.status, "completed")

    def test_delete_task_success(self):
        url = reverse('task_update_del', kwargs={'pk': self.task2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task2.id).exists())

    def test_create_task_with_empty_name_fails(self):
        data = {"name": "   ", "status": "running"}
        response = self.client.post(self.task_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(Task.objects.count(), 2)  # No new task created

    def test_create_task_with_invalid_status_fails(self):
        data = {"name": "Another Task", "status": "pending"}
        response = self.client.post(self.task_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_update_task_with_empty_name_fails(self):
        url = reverse('task_update_del', kwargs={'pk': self.task1.id})
        data = {"name": "", "status": "running"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_update_task_with_invalid_status_fails(self):
        url = reverse('task_update_del', kwargs={'pk': self.task1.id})
        data = {"name": "New Name", "status": "unknown"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_get_nonexistent_task_returns_404(self):
        url = reverse('task_update_del', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_task_returns_404(self):
        url = reverse('task_update_del', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

