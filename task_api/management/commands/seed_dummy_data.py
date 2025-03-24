import random 
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from task_api.models import User, Task, TaskAssignment


class Command(BaseCommand):
    help = 'Seed dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding dummy data..."))

        
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f"user{i+1}",
                email=f"user{i+1}@example.com",
                password="password123",
                mobile=f"98765432{i+1}"
            )
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS("5 Users created"))

        
        task_types = ['FEATURE', 'BUG', 'IMPROVEMENT', 'MAINTENANCE']
        statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']

        tasks = []
        for i in range(10):
            task = Task.objects.create(
                name=f"Task {i+1}",
                description=f"This is a description for Task {i+1}.",
                task_type=random.choice(task_types),
                status=random.choice(statuses),
                completed_at=now() if random.choice([True, False]) else None
            )
            tasks.append(task)

        self.stdout.write(self.style.SUCCESS("10 Tasks created"))
