from http import HTTPMethod

from rest_framework import status as st
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(
                data={"message": f"{task.title}"},
                status=st.HTTP_204_NO_CONTENT,
            )
        except:
            return Response(
                data={"message": "Object not founded"},
                status=st.HTTP_404_NOT_FOUND,
            )

    @action(methods=[HTTPMethod.PATCH], detail=True)
    def mark_done(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.done = True
            task.save()
            return Response(
                data=TaskSerializer(task).data,
                status=st.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Object not founded"},
                status=st.HTTP_404_NOT_FOUND,
            )
