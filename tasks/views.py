from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, TaskReorderSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'order']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        last = Task.objects.filter(user=self.request.user).order_by('-order').first()
        order = (last.order + 1) if last else 0
        serializer.save(user=self.request.user, order=order)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        total = tasks.count()
        todo = tasks.filter(status='todo').count()
        inprogress = tasks.filter(status='inprogress').count()
        done = tasks.filter(status='done').count()
        high = tasks.filter(priority='high').count()
        return Response({
            'total': total,
            'todo': todo,
            'inprogress': inprogress,
            'done': done,
            'high_priority': high,
        })


class TaskReorderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ordered_ids = serializer.validated_data['ordered_ids']
        tasks = Task.objects.filter(user=request.user, id__in=ordered_ids)
        task_map = {t.id: t for t in tasks}
        for idx, task_id in enumerate(ordered_ids):
            if task_id in task_map:
                task_map[task_id].order = idx
        Task.objects.bulk_update(list(task_map.values()), ['order'])
        return Response({'message': 'Reordered successfully.'})
