from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, Task, TaskAssignment
from .serializers import (
    UserSerializer,
    TaskSerializer,
    TaskAssignmentSerializer,
    TaskDetailSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    ''' 
    ViewSet for tasks with CRUD actions and some additional task related features
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer


    @action(detail=True , methods=['post'])
    def assign_users(self,request, pk=None):
        ''' function for assigning tasks to one user or multiple user 
            POST /api/tasks/{id}/assign_users/
        '''
        task = self.get_object()
        user_ids = request.data.get('user_ids' , [])

        if not user_ids:
            return Response(
                {"error": "No user IDs provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
         
        users = []
        invalid_ids = []
        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
                users.append(user)
            except User.DoesNotExist:
                invalid_ids.append(user_id)
        
        if invalid_ids:
            return Response(
                {"error": f"Invalid user IDs: {invalid_ids}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignments = []
        for user in users:
            assignment, created = TaskAssignment.objects.get_or_create(
                task=task,
                user=user
            )
            assignments.append(assignment)
        
        serializer = TaskAssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unassign_users(self, request, pk=None):
        '''
        Remove task assignments for specified users
        DELETE /api/tasks/{id}/unassign_users/
        '''
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        if not user_ids:
            return Response(
                {"error": "No user IDs provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the specified assignments
        deleted_count = TaskAssignment.objects.filter(
            task=task,
            user_id__in=user_ids
        ).delete()[0]

        return Response(
            {"message": f"Removed {deleted_count} task assignments"},
            status=status.HTTP_200_OK
        )


class TaskListView(generics.ListAPIView):
    ''' 
    For getting all tasks related to a specific user
    GET /api/users/{id}/tasks/
    '''
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return user.assigned_tasks.all()

class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

