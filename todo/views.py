from rest_framework import viewsets
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from todo.models import Task
from todo.model_utils import TaskContext
from todo.serializers import TaskSerializer, ChildTaskSerializer


class StateFullTasksResource(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_task_with_context(self):
        """
        retrive a Task model instance and return a TaskContext
        instead.
        """
        instance = super().get_object()
        return TaskContext(instance)

    def update(self, request, *args, **kwargs):
        """
        Update a task based on it's current state.
        """
        task = self.get_task_with_context()
        instance = task.update(**request.data)

        serializer = TaskSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)   

    @action(detail=True, methods=['post'])
    def link(self, request, pk):
        """
        Link two tasks togther based on the parent task state.
        """
        task = self.get_task_with_context()
        input_serializer = ChildTaskSerializer(data=request.data)

        if input_serializer.is_valid(raise_exception=True):
            child = input_serializer.validated_data['child']
            task = task.link(child)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def change_state(self, request, pk):
        """
        Froward change the state of a task based on it's current state.
        """
        task = self.get_task_with_context()
        task.change_state()

        return Response({'state': task._task.state}, status=status.HTTP_200_OK)