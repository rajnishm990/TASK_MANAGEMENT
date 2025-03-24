from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ''' User model with additional fields '''
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    ''' Models for Task  '''
    class TaskStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class TaskType(models.TextChoices):
        FEATURE = 'FEATURE', 'Feature'
        BUG = 'BUG', 'Bug'
        IMPROVEMENT = 'IMPROVEMENT', 'Improvement'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.FEATURE
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    assigned_users = models.ManyToManyField(
        User,
        through='TaskAssignment',
        related_name='assigned_tasks'
    )

    def __str__(self):
        return self.name

class TaskAssignment(models.Model):
    '''
    Intermediary model for the many-to-many relationship between tasks and users
    Allows tracking assignment metadata such as assignment date
    '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'user')

    def __str__(self):
        return f"{self.task.name} assigned to {self.user.username}"

