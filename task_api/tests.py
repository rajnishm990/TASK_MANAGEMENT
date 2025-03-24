from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Task, TaskAssignment


class TaskAPITestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            name='Test User 1',
            mobile='1234567890'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123',
            name='Test User 2',
            mobile='0987654321'
        )
        
        # Create client
        self.client = APIClient()
        
        # Create a task
        self.task_data = {
            'name': 'Test Task',
            'description': 'This is a test task',
            'task_type': 'FEATURE',
            'status': 'PENDING',
            
        }
        
        response = self.client.post(
            reverse('task-list'),
            self.task_data,
            format='json'
        )
        
        self.task = Task.objects.get(id=response.data['id'])

    def test_create_task(self):
        """Test creating a new task"""
        task_data = {
            'name': 'Another Test Task',
            'description': 'This is another test task',
            'task_type': 'BUG',
            'status': 'IN_PROGRESS'
        }
        
        response = self.client.post(
            reverse('task-list'),
            task_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Another Test Task')

    def test_assign_task_to_users(self):
        """Test assigning a task to users"""
        url = reverse('task-assign-users', args=[self.task.id])
        data = {'user_ids': [self.user1.id, self.user2.id]}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            TaskAssignment.objects.filter(task=self.task).count(), 
            2
        )
        
        # Test user tasks
        user_tasks_url = reverse('user-tasks', args=[self.user1.id])
        response = self.client.get(user_tasks_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.task.id)

    def test_unassign_task_from_users(self):
        """Test removing task assignments"""
        # First assign
        TaskAssignment.objects.create(task=self.task, user=self.user1)
        TaskAssignment.objects.create(task=self.task, user=self.user2)
        
        # Then unassign user1
        url = reverse('task-unassign-users', args=[self.task.id])
        data = {'user_ids': [self.user1.id]}
        
        response = self.client.delete(url, data, format='json')
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            TaskAssignment.objects.filter(task=self.task).count(), 
            1
        )
        
        # Check user1 doesn't have the task anymore
        user_tasks_url = reverse('user-tasks', args=[self.user1.id])
        response = self.client.get(user_tasks_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_task_details(self):
        """Test retrieving task details"""
        # Assign task
        TaskAssignment.objects.create(task=self.task, user=self.user1)
        
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.task.name)
        self.assertEqual(len(response.data['assigned_users']), 1)
        self.assertEqual(response.data['assigned_users'][0]['id'], self.user1.id)

    def test_validation_errors(self):
        """Test validation errors"""
        # Test missing required field
        task_data = {
            'description': 'This task has no name',
        }
        
        response = self.client.post(
            reverse('task-list'),
            task_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        
        # Test invalid enum value
        task_data = {
            'name': 'Invalid Task',
            'task_type': 'INVALID_TYPE'
        }
        
        response = self.client.post(
            reverse('task-list'),
            task_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('task_type', response.data)
