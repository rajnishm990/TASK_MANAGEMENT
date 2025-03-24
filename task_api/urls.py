from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserListView, TaskListView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserListView)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/tasks/', TaskListView.as_view(), name='user-tasks'),
]