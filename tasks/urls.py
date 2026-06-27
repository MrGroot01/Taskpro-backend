from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskStatsView, TaskReorderView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('stats/', TaskStatsView.as_view(), name='task-stats'),
    path('reorder/', TaskReorderView.as_view(), name='task-reorder'),
]
