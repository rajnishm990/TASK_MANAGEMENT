from rest_framework import serializers
from .models import User, Task, TaskAssignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                  'completed_at', 'status', 'assigned_users']
        read_only_fields = ['created_at', 'completed_at']
    
    # Custom field for assigned users
    assigned_users = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all(),
        required=False
    )

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        task = Task.objects.create(**validated_data)
        
        # Create TaskAssignment objects for each assigned user
        for user in assigned_users:
            TaskAssignment.objects.create(task=task, user=user)
        
        return task
    
    def update(self, instance, validated_data):
        assigned_users = validated_data.pop('assigned_users', None)
        
        # Update task fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update assigned users if provided
        if assigned_users is not None:
            # Clear existing assignments
            instance.taskassignment_set.all().delete()
            
            # Create new assignments
            for user in assigned_users:
                TaskAssignment.objects.create(task=instance, user=user)
        
        return instance


class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = ['task', 'user', 'assigned_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                  'completed_at', 'status', 'assigned_users']